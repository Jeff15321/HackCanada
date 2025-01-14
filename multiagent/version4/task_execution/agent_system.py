import os
import json

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
        while subtask_delegation_plan == ""
            try:
                subtask_delegation_plan = self.agents_dict["Task Delegator Agent"].run_api(delegation_prompt)
                subtask_delegation_plan = subtask_delegation_plan.replace("""```json""", '').replace("""```""", '') # this one's more of a just in case whereas for task_execution_plan you needed to do it
                subtask_delegation_plan_formatted = json.loads(subtask_delegation_plan)
                assert isinstance(subtask_delegation_plan_formatted, list) # should probably replace these with a more comprehensive check for formatting
                assert isinstance(subtask_delegation_plan_formatted[0], tuple)
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
            if agent not in agents_dict.keys():  # default to writing agent :monkey:
                agent = "Writing Agent"
            step_output = agents_dict[agent].run_api(step_prompt)
            completed_steps_outputs.append((step, step_output))
       
        return completed_steps_outputs[-1][1]

    def run(self, task, context, refined_prompt, max_rounds=3):
        logger = setup_logger()

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
                assert isinstance(task_delegation_plan_formatted, dict) # should probably replace these with a more comprehensive check for formatting
                assert isinstance(task_delegation_plan_formatted.items()[0], list)
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
        
        # Now merge the work from the subtasks together with the merger agent
        merging_prompt = (
            f"Here is the task execution file for the overall task: {task_execution_plan}\n"
            f"Below are the outputs for each subtask for the overall task (the subtasks: {task_execution_plan_formatted.keys()}):\n"
        )
        for i, (subtask, subtask_output) in enumerate(subtask_outputs): # feed it all the subtask outputs
            merging_prompt = merging_prompt + f"Subtask {i+1}: {subtask}\n{subtask_output}\n"
        final_output = agents_dict["Merger Agent"].run_api(merging_prompt)

        return final_output

        # Do standards and verification work here
        # INSERT STANDARDS AGENTS AND VERIFICATION AGENT HERE (Which also means everything above probably has to be put in a loop)

        return "WORK IN PROGRESS"