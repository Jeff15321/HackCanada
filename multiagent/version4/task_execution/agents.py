from task_execution.model import *
from task_execution.agent_definitions import *

import logging
import asyncio

# Setup logging
logger = logging.getLogger("AgentsLogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    # Prevent adding multiple handlers in interactive environments
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class BaseAgent:
    def __init__(self, name, role, function, model):
        self.name = name
        self.role = role
        self.function = function
        self.model = model

    def query_llm(self, input_content):
        system_prompt = (
            f"You are: {self.name}.\n"
            f"Your role: {self.role}\n"
            f"Your function: {self.function}\n"
        )
        user_prompt = input_content
        return system_prompt, user_prompt
    
    async def run_api(self, input_content: str) -> str:
        """Default agent uses run_gpt (no PDF)."""
        system_msg, user_msg = self.query_llm(input_content)
        logger.info(f"Running API for agent: {self.name}")
        return await run_gpt(system_msg, user_msg, self.model)

class InstructionalFileAgent(BaseAgent):
    def __init__(self, name, role, function, model, instructional_files):
        super().__init__(name, role, function, model)
        self.instructional_files = instructional_files
    
    async def run_api(self, input_content: str) -> str:
        system_msg, user_msg = self.query_llm(input_content)
        logger.info(f"{self.name}: accessing full PDF.")
        response = await run_gpt_with_file(system_msg, user_msg, self.instructional_files, self.model)
        return response

class TaskExecutorAgent(BaseAgent):
    def __init__(self, name, role, function, model, instructional_files, supplementary_files, uses_rag):
        super().__init__(name, role, function, model)
        self.instructional_files = instructional_files
        self.supplementary_files = supplementary_files
        self.uses_rag = uses_rag
        self._semaphore = asyncio.Semaphore(5)

    async def run_api(self, input_content: str) -> str:
        system_msg, user_msg = self.query_llm(input_content)
        async with self._semaphore:
            if not self.uses_rag:
                return await run_gpt(system_msg, user_msg, self.model)
            logger.info(f"{self.name}: Performing semantic retrieval with prompt: '{user_msg}'")
            rag_output = await run_gpt_with_rag(
                system_msg,
                user_msg,
                self.instructional_files,
                self.supplementary_files,
                self.model
            )
            logger.info(f"{self.name}: Retrieved content:\n{rag_output}")
            return rag_output

"""
returns:
{
    [agent name]: [corresponding agent object],
    ...
}
"""
def initialize_task_execution_agents(instructional_files, supplementary_files, model):
    agents_dict = {}

    # Initialize the overall agents
    for key,val in overall_task_agent_definitions.items():
        if key == "Task Planner Agent" or key == "Task Delegator Agent":
            new_agent = InstructionalFileAgent(val["name"], val["role"], val["function"], model, instructional_files)
            agents_dict[key] = new_agent
        elif key == "Merger Agent" or key == "Verification Agent" or key == "Standards Agent":
            new_agent = BaseAgent(val["name"], val["role"], val["function"], model)
            agents_dict[key] = new_agent
    for key,val in subtask_executor_agent_definitions.items():
        new_agent = TaskExecutorAgent(val["name"], val["role"], val["function"], model, instructional_files, supplementary_files, val["uses_rag"])
        agents_dict[key] = new_agent
    
    return agents_dict

if __name__ == '__main__':
    print("hehe none of this works in this file cuz the way dependencies are :) you have to run in main")