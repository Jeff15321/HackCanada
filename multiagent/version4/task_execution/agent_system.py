import os
import json
import ast
import asyncio
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor

from task_execution.agents import * # this would include everything in agent_definitions.py as if they were part of this file
from task_execution.logger import setup_logger


class multiagentTaskExecutionSystem:
    def __init__(self, instructional_files, supplementary_files, model):
        self.instructional_files = instructional_files
        self.supplementary_files = supplementary_files
        self.model = model
        self.agents_dict = initialize_task_execution_agents(
            self.instructional_files, 
            self.supplementary_files, 
            self.model
        )
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count() * 2)
    
    # should probably have some functions to verify for function formats

    async def run_subtask_step(self, step: str, agent: str, step_prompt: str, logger) -> tuple[str, str]:
        try:
            if agent not in self.agents_dict:
                logger.warning(f"Wrong agent name: {agent}")
                agent = "Writing Agent"
            
            step_output = await self.agents_dict[agent].run_api(step_prompt)
            return step, step_output
        except Exception as e:
            logger.error(f"Error in step {step}: {str(e)}")
            return step, f"Error: {str(e)}"

    async def run_subtask(self, subtask: str, task_execution_plan_formatted: dict, overall_prompt: str, logger) -> str:
        try:
            delegation_prompt = (
                f"{overall_prompt}\n"
                f"Task execution plan: {task_execution_plan_formatted}\n"
                f"Current subtask: {subtask}\n"
                f"Subtask details: {task_execution_plan_formatted[subtask]}"
            )

            steps = task_execution_plan_formatted[subtask]
            if isinstance(steps, list):
                steps = {f"Step {i+1}": step for i, step in enumerate(steps)}

            results = {}
            async with asyncio.TaskGroup() as tg:
                tasks = {
                    step: tg.create_task(
                        self.run_subtask_step(
                            step, 
                            agent, 
                            f"{delegation_prompt}\nCurrent step: {step}",
                            logger
                        )
                    )
                    for step, agent in steps.items()
                }

                for step, task in tasks.items():
                    try:
                        _, output = await task
                        results[step] = output
                    except Exception as e:
                        results[step] = f"Error: {str(e)}"

            return results[list(results.keys())[-1]]
        except Exception as e:
            logger.error(f"Error in subtask {subtask}: {str(e)}")
            return f"Error in subtask: {str(e)}"

    async def run_parallel_subtasks(self, task_execution_plan_formatted: dict, prompt: str, logger) -> list:
        results = []
        async with asyncio.TaskGroup() as tg:
            tasks = {
                subtask: tg.create_task(
                    self.run_subtask(subtask, task_execution_plan_formatted, prompt, logger)
                )
                for subtask in task_execution_plan_formatted.keys()
            }

            for subtask, task in tasks.items():
                try:
                    output = await task
                    results.append((subtask, output))
                except Exception as e:
                    results.append((subtask, f"Error: {str(e)}"))

        return results

    async def run_full_task_async(self, task, context, refined_prompt, logger):
        initial_prompt = f"Task: {task}\nContext:{context}\n{refined_prompt}"
        prompt = initial_prompt
        logger.info(f"*****Initial Prompt*****\n{prompt}")

        task_execution_plan = ""
        task_execution_plan_formatted = {}
        
        # Get task execution plan with retry logic
        for _ in range(3):
            try:
                task_execution_plan = await self.agents_dict["Task Planner Agent"].run_api(prompt)
                task_execution_plan = task_execution_plan.replace("```json", '').replace("```", '')
                task_execution_plan_formatted = json.loads(task_execution_plan)
                
                if isinstance(task_execution_plan_formatted, list):
                    task_execution_plan_formatted = {
                        f"Task {i+1}": steps for i, steps in enumerate(task_execution_plan_formatted)
                    }
                
                logger.info(f"*****Task Planner Agent*****\n{task_execution_plan_formatted}")
                break
            except Exception as e:
                logger.warning(f"FILE PARSING FAILED (Task Planner Agent) on:\n{task_execution_plan}")
                logger.error(f"Error details: {str(e)}", exc_info=True)
                await asyncio.sleep(1)

        if not task_execution_plan_formatted:
            raise Exception("Failed to get valid task execution plan after retries")

        subtask_outputs = await self.run_parallel_subtasks(task_execution_plan_formatted, prompt, logger)

        merging_prompt = (
            f"Here is the task execution file for the overall task: {task_execution_plan}\n"
            f"Below are the outputs for each subtask for the overall task (the subtasks: {task_execution_plan_formatted.keys()}):\n"
        )
        for i, (subtask, subtask_output) in enumerate(subtask_outputs):
            merging_prompt = merging_prompt + f"Subtask {i+1}: {subtask}\n{subtask_output}\n"
        
        merged_output = await self.agents_dict["Merger Agent"].run_api(merging_prompt)
        logger.info(f"*****Merger Agent*****\n{merged_output}")
        
        final_output = ""
        for (subtask, subtask_output) in subtask_outputs:
            final_output = final_output + f"{subtask}:\n{subtask_output}\n\n\n"
        logger.info(f"*****Hard Concatenation of Subtask Outputs*****\n{final_output}")

        return final_output

    def run(self, task: str, context: str, refined_prompt: str, max_rounds: int = 3) -> str:
        logger = setup_logger("multiagent_task_execution")
        return asyncio.run(self.run_full_task_async(task, context, refined_prompt, logger))

    def create_list_of_metrics(self, task, context, refined_prompt, logger):
        metrics = ""
        metrics_formatted = []
        while metrics == "":
            try:
                metrics = self.agents_dict["Standards Agent"].run_api(f"Task: {task}\nContext:{context}\n{refined_prompt}")
                metrics = metrics.replace("""```json""", '').replace("""```""", '') # this one's more of a just in case whereas for task_execution_plan you needed to do it
                metrics_formatted = ast.literal_eval(metrics)
                assert isinstance(metrics_formatted, list) # should probably replace these with a more comprehensive check for formatting
                assert isinstance(metrics_formatted[0], dict)
                logger.info(f"*****Standards Agent*****\n{metrics}")
            except Exception as e:
                logger.warning(f"FILE PARSING FAILED (Standards Agent)) on:\n{metrics}")
                logger.error(f"Error details: {str(e)}", exc_info=True)
                metrics = ""
        return metrics_formatted
    
    def do_verification(self, task, context, refined_prompt, task_output, metrics_formatted, logger):
        prompt_component = (
            "*****This is the task description and prompt for the task:*****\n"
            f"Task: {task}\n"
            f"Context: {context}\n"
            f"Prompt: {refined_prompt}\n"
        )
        output_component = (
            "*****This the output that you are to evaluate based on the metric you are given:*****\n"
            f"{task_output}\n"
        )
       
        all_verification_results = {}

        for metric in metrics_formatted:
            metric_verification_prompt = (
                f"{prompt_component}"
                "*****This is the metric you are judge based on:*****\n"
                f"Metric: {metric['metric']}\n"
                f"Description of Metric: {metric['description']}"
                f"{output_component}"
            )
            metric_result = ""
            metric_result_formatted = {}
            while metric_result == "":
                try:
                    metric_result = self.agents_dict["Verification Agent"].run_api(metric_verification_prompt)
                    metric_result = metric_result.replace("""```json""", '').replace("""```""", '')
                    metric_result_formatted = ast.literal_eval(metric_result)
                    assert isinstance(metric_result_formatted, dict)
                    logger.info(f"*****Verification Agent - metric result\nMetric:\n{metric['metric']}\nVerification Result:\n{metric_result}")
                except Exception as e:
                    logger.warning(f"FILE PARSING FAILED (Verfication Agent) on:\n{metric_result}")
                    logger.error(f"Error details: {str(e)}", exc_info=True)
                    metric_result = ""
            all_verification_results[metric['metric']] = metric_result_formatted

        return all_verification_results
    
    def log_round_results(self, round_number, task_output, verification_results, logger):
        logger.info(f"*****ROUND {round_number}*****")
        for metric_name, metric_outcome in verification_results.items():
            logger.info(f"{metric_name}: {metric_outcome['pass']}")
        logger.info(f"TASK OUTPUT:\n{task_output}")

    # if this returns "NULL" that means there were no problems -> break the loop
    def generate_feedback(self, round_number, task_output, verification_results, logger):
        feedback_result = "In a previous attempt, you completed the task, but there are areas that need improvement. Below, I will provide a list of specific issues along with comments on what was not done well. Additionally, I will include the full output from your previous attempt for reference.\nCarefully review your prior output and examine how the identified issues occurred. Use this feedback to ensure that these problems are addressed and avoided in your next attempt.\n\n"

        have_problems = False
        for metric_name, metric_outcome in verification_results.items():
            if metric_outcome['pass'] == False:
                have_problems = True
                to_add = f"Issue: {metric_name}\nSpecific Problems: {metric_outcome['comments']}\n"
                feedback_result = feedback_result + to_add
        
        if have_problems == False:
            logger.info(F"*****NO PROBLEMS FOR ROUND {round_number}*****")
            return "NULL"
        else:
            logger.info(f"*****PROBLEMS FOR ROUND {round_number}*****\n{feedback_result}")
            feedback_result = feedback_result + "This is the entirety of the previous output for this task which had the problems:\n" + task_output + "\n" # add it AFTER the logging (rather not flood problem logging with repeat of the whole output)
        return feedback_result




