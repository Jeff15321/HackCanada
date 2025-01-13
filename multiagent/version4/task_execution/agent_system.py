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

    # # This function literally only exists in case llm gives messed up agent nameing in task delegation
    # # the subtask_dict type is supposed to be a dict, but since the llm was the one who generated all this then who knows if it followed formatting instructions
    # def run_executor_agent(self, subtask_dict, common_prompt, specific_prompt) -> str:
    #     executor_agent = self.agents_dict["Writing Agent"] # default agent
    #     try:
    #         # since format is {subtask: agent to use}
    #         subtask = subtask_dict.keys()[0]
    #         executor_agent = self.agents_dict[subtask_dict.items()[0]]
    #     except:
    #         logger.warning(f"FORMATTING ISSUE (run_executor_agent): {subtask_dict}")
    #         subtask_dict = str(subtask_dict)
    #     prompt = (
    #         f"{prompt}\n"
    #         f"{specific_prompt}"
    #         f"Your specific subtask is: {subtask}\n"
    #         # f"The specific subtask you are to execute is:\n{subtask}"
    #         # "This is the only thing you are to do, do not return anything other than the output for you exact subtask you have been assigned that is a part of the greater picture outlined in the task execution plan."
    #         # f"While you must take into account how your assigned subtask fits into the task execution plan, you must only output the exact output for the subtask you have been assigned: {subtask}"
    #     )
    #     return executor_agent.run_api(prompt)

    # def execute_subtasks(self, subtask, common_prompt, specific_prompt) -> str:
    #     if type(subtask) != list and type(subtask) != tuple:
    #         return self.run_executor_agent(self, subtask, common_prompt)
    #     elif type(subtask) == list:
    #         list_prompt = (
    #             "You are to execute a specific subtask in a list of sequential subtasks which then contribute to the overall task execution. This this list of sequential subtasks, each task subtask (including the one you are to execute) builds upon the previous subtask. As such, make sure to incorporate the content from the previous subtasks in the sequence without missing anything\n"
    #             f"The sequence of subtasks that your subtask is a part of is (as well as the name of the corresponding agent which executes each subtask) is: \n {subtask}\n"
    #             f"You are to execute and output the result for your assigned subtask and make sure that the output properly, coherently, and holistically includes the content outputted during the previous subtasks.\n"
    #         )
    #         previous_outputs = []
    #         for i in range(0, len(subtask)):
    #             if len(previous_outputs) != 0:
    #                 list_prompt += "Previous outputs in the series of subtasks that you are to include and upon which your subtask content is built/added:\n"
    #                 for i in range(0, len(previous_outputs)):
    #                     list_prompt = list_prompt + f"Part {i+1} from the series: \n" + f"Subtask(s) involved: {subtask[i]}" + f"Output from part {i+1}:\n{previous_outputs[i]}"
    #             else:
    #                 list_prompt
    #     elif type(subtask) == tuple:
    #         return

    def run_subtask(self, subtask, task_execution_plan_formatted, overall_prompt, specific_prompt):
        return ""

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
                logger.info(f"*****Task Planner Agent*****\n{task_execution_plan_formatted}")
            except Exception as e:
                logger.warning(f"FILE PARSING FAILED (Task Planner Agent) on:\n{task_execution_plan}")
                logger.error(f"Error details: {str(e)}", exc_info=True)
                task_execution_plan = ""


        print("MONKE BRUGA")
        print(task_execution_plan_formatted)

        
        # Now do the task delegation into subtasks and task executon for each subtask
        subtask_outputs = []
        for subtask, steps in task_execution_plan_formatted.items():
            specific_prompt = (
                "\nHere is the task execution plan that you are to reference:\n"
                f"{task_execution_plan}"
            )
            subtask_output = self.run_subtask(subtask, task_execution_plan_formatted, prompt, specific_prompt)
            subtask_outputs.append[(subtask, subtask_output)]
        
        # Now merge the work from the subtasks together with the merger agent
        # INSERT MERGER AGENT WORK HERE

        # Do standards and verification work here
        # INSERT STANDARDS AGENTS AND VERIFICATION AGENT HERE (Which also means everything above probably has to be put in a loop)

        return "WORK IN PROGRESS"



    
        # next steps:
        # - break up task_execution_plan_formatted into its items (which are the subtasks)
        # for each subtask: put through the task delegator agent -> do the tasks step by step
        # merge the work from the subtasks together 
        # put the work up for review agent 
        # go through the standards and verification process (maybe not yet tho)

        # ^up to here should still be good, everything below this needs reworking in accordance with new system :skull:
        ######################################################################################################

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