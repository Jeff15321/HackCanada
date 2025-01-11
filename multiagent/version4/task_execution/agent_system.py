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
        
        return task_delegation_plan






































































def monke():
    instructional_files = []
    supplementary_files = []
    agents_dict = initialize_task_execution_agents(instructional_files, supplementary_files, "gpt-4o-mini")
    print(agents_dict)

