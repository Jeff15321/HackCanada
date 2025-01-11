import os
import json

from task_execution.agents import *
from task_execution.logger import setup_logger


class multiagentTaskExecutionSystem:
    def __init__(self, instructional_files, supplementary_files, model):
        self.instructional_files = instructional_files
        self.supplementary_files = supplementary_files
        self.model = model
        self.agents_dict = initialize_task_execution_agents(self.instructional_files, self.supplementary_files, self.model)
        self.format_explanation = (
            "The task execution plan is formatted as follows: \n\n1. Sequential tasks (where each action buils upon the previous one) will be represented as arrays [] with the order of actions clearly defined. \n2. Parallel tasks (where actions can happen simultaneously) will be represented as tuples () where the order of execution doesn't matter. \n3. A combination of both parallel and sequential actions can be included, using tuples inside arrays or arrays inside tuples as needed."
        )

    # This function literally only exists in case llm gives messed up agent nameing in task delegation
    # the subtask_dict type is supposed to be a dict, but since the llm was the one who generated all this then who knows if it followed formatting instructions
    def run_executor_agent(self, subtask_dict, prompt: str) -> str:
        executor_agent = self.agents_dict["Writing Agent"] # default agent
        try:
            # since format is {subtask: agent to use}
            subtask = subtask_dict.keys()[0]
            executor_agent = self.agents_dict[subtask_dict.items()[0]]
        except:
            logger.warning(f"FORMATTING ISSUE (run_executor_agent): {subtask_dict}")
            subtask_dict = str(subtask_dict)
        prompt = (
            f"{prompt}"
            f"The specific subtask you are to execute is:\n{subtask}"
            "This is the only thing you are to do, do not return anything other than the output for you exact subtask you have been assigned that is a part of the greater picture outlined in the task execution plan."
            f"While you must take into account how your assigned subtask fits into the task execution plan, you must only output the exact output for the subtask you have been assigned: {subtask}"
        )
        return executor_agent.run_api(prompt)

    def execute_subtasks(self, subtask, common_prompt, specific_prompt) -> str:
        if type(subtask) != list and type(subtask) != tuple:
            return self.run_executor_agent(self, subtask, common_prompt)
        
        

    def run(self, task, context, refined_prompt, max_rounds=3):
        logger = setup_logger()

        initial_prompt = f"Task: {task}\nContext:{context}\n{refined_prompt}"

        # Starts off with the refined prompt from the multiagent prompt refinement
        prompt = initial_prompt
        logger.info(f"*****Initial Prompt*****\n{prompt}")

        # Put it through Task Planner Agent, output: formatted task execution plan with the []'s and {}'s
        task_execution_plan = ""
        task_execution_plan_formatted = {}
        while task_execution_plan == "":
            try:
                task_execution_plan = self.agents_dict["Task Planner Agent"].run_api(prompt)
                task_execution_plan = task_execution_plan.replace("""```json""", '').replace("""```""", '')
                task_execution_plan_formatted = json.loads(task_execution_plan)
                logger.info(f"*****Task Planner Agent*****\n{task_execution_plan_formatted['task_plan']}")
            except:
                logger.warning(f"FILE PARSING FAILED (Task Planner Agent) on:\n{task_execution_plan}")
                task_execution_plan = ""
    
        # Put it through Task Delegator Agent, output: the execution plan from above but each thing is a dict where it's {subtask: executor agent to use}
        prompt = (
            f"{prompt}"
            "\nHere is the task execution plan that you are to reference (make sure to keep the same structure of lists and tuples, except this time each string will be replaced with a dictionary that has is in the format of {original subtask string, task executor agent name}):\n"
            f"{task_execution_plan}"
        )
        task_delegation_plan = ""
        task_delegation_plan_formatted = {}
        while task_delegation_plan == "":
            try:
                task_delegation_plan = self.agents_dict["Task Delegator Agent"].run_api(prompt)
                task_delegation_plan = task_delegation_plan.replace("""```json""", '').replace("""```""", '')
                task_delegation_plan_formatted = json.loads(task_delegation_plan)
                logger.info(f"*****Task Delegator Agent*****\n{task_delegation_plan_formatted['task_plan']}")
            except:
                logger.warning(f"FILE PARSING FAILED (Task Delegator Agent) on:\n{task_delegation_plan}")
                task_delegation_plan = ""
        
        # Now do task exection
        prompt = (
            f"You are to properly execute a subtask that is part of completing the overall task, the subtask is a part of the Task Execution Plan and {self.format}\n"
            f"This is the prompt for the overall task that you are given: \n {initial_prompt}"
            f"This is the task execution plan that you are to follow: \n{task_execution_plan}"
        )

        task_output = self.execute_subtasks(task_delegation_plan_formatted, prompt, "")

        # INSERT STANDARDS AGENTS AND VERIFICATION AGENT HERE
        # (Which also means everything above probably has to be put in a loop)

        return task_output