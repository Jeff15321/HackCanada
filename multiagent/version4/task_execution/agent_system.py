import os
import json
import ast

from task_execution.agents import * # this would include everything in agent_definitions.py as if they were part of this file
from task_execution.logger import setup_logger


class multiagentTaskExecutionSystem:
    def __init__(self, instructional_files, supplementary_files, model):
        self.instructional_files = instructional_files
        self.supplementary_files = supplementary_files
        self.model = model
        self.agents_dict = initialize_task_execution_agents(self.instructional_files, self.supplementary_files, self.model)
    
    # should probably have some functions to verify for function formats

    def run_subtask(self, subtask, task_execution_plan_formatted, overall_prompt, logger):
        # Run the Task Delegator Agent to get the task delegation plan
        delegation_prompt = (
            f"{overall_prompt}\n"
            f"Here is the overall task execution plan that you are to reference:\n{task_execution_plan_formatted}\n"
            f"This is the specific subtask that you are to create the subtask delegation plan for:\n"
            f"Subtask: {subtask}\n"
            f"Subtask items as formatted from task execution plan:\n{task_execution_plan_formatted[subtask]}"
        )
        subtask_delegation_plan = ""
        subtask_delegation_plan_formatted = [] # listof((subtask step, assigned agent))
        while subtask_delegation_plan == "":
            try:
                subtask_delegation_plan = self.agents_dict["Task Delegator Agent"].run_api(delegation_prompt)
                subtask_delegation_plan = subtask_delegation_plan.replace("""```json""", '').replace("""```""", '') # this one's more of a just in case whereas for task_execution_plan you needed to do it
                subtask_delegation_plan_formatted = ast.literal_eval(subtask_delegation_plan)
                assert isinstance(subtask_delegation_plan_formatted, list) # should probably replace these with a more comprehensive check for formatting
                # assert isinstance(subtask_delegation_plan_formatted[0], tuple)
                # ^oh and pretty sure this test is wrong
                logger.info(f"*****Task Delegator Agent ({subtask})*****\n{subtask_delegation_plan}")
            except Exception as e:
                logger.warning(f"FILE PARSING FAILED (Task Delegator Agent subtask: {subtask}) on:\n{subtask_delegation_plan}")
                logger.error(f"Error details: {str(e)}", exc_info=True)
                subtask_delegation_plan = ""
        
        completed_steps_outputs = [] # listof((step, step output))
        # Do each subtask
        for step, agent in subtask_delegation_plan_formatted:
            # add to the prompt: overall list of steps, your step to do, previous outputs,
            step_prompt = (
                f"{delegation_prompt}\n"
                f"The specific step of the subtask that you are responsible for is: {step}"
                "Your output is to draw from and build upon the steps that came before you in the subtask. Here are the steps in the subtask that came before you:\n"
            )
            for i, (prev_step, prev_output) in enumerate(completed_steps_outputs): # adding output from previous steps
                step_prompt = step_prompt + f"Step {i+1}: {prev_step}\n{prev_output}\n"
            if agent not in self.agents_dict.keys():  # default to writing agent :monkey:
                logger.warning(f"Wrong agent name: {agent}")
                agent = "Writing Agent"
            step_output = self.agents_dict[agent].run_api(step_prompt)
            completed_steps_outputs.append((step, step_output))
            logger.info(f"*****Subtask step: {step} (agent: {agent})*****\n{step_output}")
       
        return completed_steps_outputs[-1][1]

    def run_full_task(self, task, context, refined_prompt, logger):
        # logger = setup_logger()

        initial_prompt = f"Task: {task}\nContext:{context}\n{refined_prompt}"

        # Starts off with the refined prompt from the multiagent prompt refinement
        prompt = initial_prompt
        logger.info(f"*****Initial Prompt*****\n{prompt}")

        # Put it through Task Planner Agent, output: formatted task execution plan: {subtask: [step1, step2, ..., step n], ...}
        task_execution_plan = ""
        task_execution_plan_formatted = {}
        while task_execution_plan == "":
            try:
                task_execution_plan = self.agents_dict["Task Planner Agent"].run_api(prompt)
                task_execution_plan = task_execution_plan.replace("""```json""", '').replace("""```""", '')
                task_execution_plan_formatted = json.loads(task_execution_plan)
                assert isinstance(task_execution_plan_formatted, dict) # should probably replace these with a more comprehensive check for formatting
                # assert isinstance(list(task_execution_plan_formatted.items())[0], list) 
                # ^smtg wrong about the code for this one
                logger.info(f"*****Task Planner Agent*****\n{task_execution_plan_formatted}")
            except Exception as e: # most likely errors: format issues, duplicate keys
                logger.warning(f"FILE PARSING FAILED (Task Planner Agent) on:\n{task_execution_plan}")
                logger.error(f"Error details: {str(e)}", exc_info=True)
                task_execution_plan = ""
        
        # Now do the task delegation into subtasks and task executon for each subtask
        subtask_outputs = [] # listof((subtask name, subtask output))
        for subtask in task_execution_plan_formatted.keys():
            # Run each subtask through the Task Delegator Agent, and then the execution agents for each step of the subtask
            subtask_output = self.run_subtask(subtask, task_execution_plan_formatted, prompt, logger)
            subtask_outputs.append((subtask, subtask_output))
        
        # ***********VERY IMPORTANT NOTICE***********
        # So the Merger Agent has a tendency to remove over half the content from each subtask output during the merging process which is not good, so we are going to both the merger agent result, and just hard concatenating everything together
        # Both will go into the logs, but the hard concatenated one will be the return value

        # Now merge the work from the subtasks together with the merger agent
        merging_prompt = (
            f"Here is the task execution file for the overall task: {task_execution_plan}\n"
            f"Below are the outputs for each subtask for the overall task (the subtasks: {task_execution_plan_formatted.keys()}):\n"
        )
        for i, (subtask, subtask_output) in enumerate(subtask_outputs): # feed it all the subtask outputs
            merging_prompt = merging_prompt + f"Subtask {i+1}: {subtask}\n{subtask_output}\n"
        merged_output = self.agents_dict["Merger Agent"].run_api(merging_prompt)
        logger.info(f"*****Merger Agent*****\n{merged_output}")
        
        final_output = ""
        for (subtask, subtask_output) in subtask_outputs:
            final_output = final_output + f"{subtask}:\n{subtask_output}\n\n\n"
        logger.info(f"*****Hard Concatenation of Subtask Outputs*****\n{final_output}")

        return final_output
    
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


    ##### THIS ENCOMPASSES EVERYTHING THAT IS HAPPENING #####
    def run(self, task, context, refined_prompt, max_rounds=3):
        logger = setup_logger("multiagent_task_execution")
        result_logger = setup_logger("task_output_result")

        final_result = ""
        metrics_formatted = self.create_list_of_metrics(task, context, refined_prompt, logger) # Come with with a list of metrics       
        feedback = ""

        for i in range(1, max_rounds+1):
            refined_prompt_with_feedback  = refined_prompt + feedback
            logger.info(f"###############################")
            logger.info(f"########### Round {i} ###########")
            logger.info(f"###############################\n\n")

            # Get a final output of the entire task execution
            final_result = self.run_full_task(task, context, refined_prompt_with_feedback, logger)

            # Verify the final output using the list of metrics
            verification_results = self.do_verification(task, context, refined_prompt_with_feedback, final_result, metrics_formatted, logger)

            # Log the output and verfication result in a separate log
            self.log_round_results(i, final_result, verification_results, result_logger)

            # Generate the feedback (var feedback should equal "NULL" if all the metrics passed)
            feedback = self.generate_feedback(i, final_result, verification_results, logger)

            # If the loop didn't break then it'll keep going with the feedback appended to the prompt
            if feedback == "NULL":
                break

        return final_result




