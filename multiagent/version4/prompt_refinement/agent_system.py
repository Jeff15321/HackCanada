import os

from prompt_refinement.agents import *
from prompt_refinement.logger import setup_logger


class multiagentSystem:
    def __init__(self, list_of_agents, instructional_files, supplementary_files, model):
        self.list_of_agents = list_of_agents
        self.instructional_files = instructional_files
        self.supplementary_files = supplementary_files
        self.model = model
        self.agents_dict = initialize_prompt_agents(self.list_of_agents, self.instructional_files, self.supplementary_files, self.model)
    
    def run(self, task, context, dspy_prompt, refinement_rounds, search_rounds):
        logger = setup_logger()

        original_prompt = f"Task: {task}\nContext:{context}\n{dspy_prompt}"
        prompt = original_prompt
        logger.info(f"*****Original Prompt*****\n{prompt}")

        prompt = self.agents_dict["Prompt Generator Agent"].run_api(prompt)
        logger.info(f"*****Prompt Generator Agent***** \n{prompt}")

        prompt = self.agents_dict["Process Creator Agent"].run_api(prompt)
        logger.info(f"*****Process Creator Agent***** \n{prompt}")
            
        # do the non-search agents
        for i in range(1, refinement_rounds + 1):
            combined_refinements = []
            logger.info("---------------")
            logger.info(f"Intermediate Round {i}")
            logger.info("---------------")
            for agent_name, intermediate_agent in self.agents_dict.items():
                if agent_name in ["Task Determinator Agent", "Prompt Generator Agent", "Process Creator Agent", "Consolidator Agent", "Completeness Agent", "Search Consolidator Agent"]:
                    continue
                elif "Search Agent" in agent_name:
                    continue
                refined_prompt = intermediate_agent.run_api(prompt)
                combined_refinements.append(f"agent name: {intermediate_agent.name}, agent role: {intermediate_agent.role}, prompt generated: {refined_prompt}")
                logger.info(f"***** {intermediate_agent.name} *****")
                logger.info(refined_prompt)
            
            combined_refinements_prompt = f"Original prompt: " + prompt + " |||||| " + " |||||| ".join(combined_refinements) # ok so smtg here is probably wrong, I don't think I used completeness agent correctly :skull:
            prompt = combined_refinements_prompt
        
            prompt = self.agents_dict["Consolidator Agent"].run_api(prompt)
            logger.info(f"*****Consolidator Agent*****\n{prompt}")

        # do search agents
        for i in range(1, search_rounds + 1):
            combined_searches = []
            logger.info("---------------")
            logger.info(f"Search Agents Round {i}")
            logger.info("---------------")
            for agent_name, search_agent in self.agents_dict.items():
                if "Search Agent" not in agent_name:
                    continue
                search_result = search_agent.run_api(prompt)
                combined_searches.append(f"{search_agent.name} content: {search_result}")
                logger.info(f"***** {search_agent.name} *****")
                logger.info(search_result)

            combined_searches_prompt = f"Original prompt: " + prompt + " |||||| " + " |||||| ".join(combined_searches)
            prompt = combined_searches_prompt

            logger.info("MONKE BRUGA BEGIN MONKE BRUGA BEGIN MONKE BRUGA BEGIN MONKE BRUGA BEGIN")
            logger.info(combined_searches_prompt)
            logger.info("MONKE BRUGA END MONKE BRUGA END MONKE BRUGA END MONKE BRUGA END ")

            prompt = self.agents_dict["Search Consolidator Agent"].run_api(prompt)
            logger.info(f"*****Search Consolidator Agent*****\n{prompt}")

        prompt = self.agents_dict["Completeness Agent"].run_api(prompt, original_prompt)
        logger.info(f"*****Completeness Agent*****\n{prompt}")

        return prompt