from model import *
from agent_definitions import agent_definitions

class Agent:
    def __init__(self, name, role, function, model):
        self.name = name
        self.role = role
        self.function = function
        self.model = model

    def query_llm(self, input_prompt):
        """Simulates querying the LLM with a role-specific prompt."""
        system_prompt=f"You are a: {self.name}. Your role: {self.role}. Your function: {self.function}."
        full_prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>Based on your role and function, give the modified new prompt for the following with a new prompt. Do not give me anything else other than the prompt:{input_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        return full_prompt
    
    def run_api(self, input_prompt):
        text_prompt = self.query_llm(input_prompt)
        agent_role = self.role
        response = run_gpt(text_prompt, agent_role, self.model)
        return response

class CompletenessAgent(Agent):
    def query_llm(self, input_prompt, original_task):
        """Ensures the final prompt includes all critical components from the original task."""
        system_prompt=f"You are a: {self.name}. Your role: {self.role}. Your function: {self.function}."

        full_prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
        Original Task: {original_task}
        # Final Prompt: {input_prompt}
        # Make sure the final prompt contains all requirements of the original task. Modify the prompt if necessary and return only the final prompt.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        return full_prompt



"""
returns:
{
    "Prompt Generator Agent": Prompt Generator Agent,
    "intermediate agents": [Agent, Agent, ...],
    "Consolidator Agent": Consolidator Agent,
    "Completeness Agent": Completeness Agent
}
"""
def initialize_prompt_agents(list_of_intermediate_agents, model):
    prompt_generator_agent = Agent(agent_definitions["Prompt Generator Agent"]["name"], agent_definitions["Prompt Generator Agent"]["role"], agent_definitions["Prompt Generator Agent"]["function"], model)
    consolidator_agent = Agent(agent_definitions["Consolidator Agent"]["name"], agent_definitions["Prompt Generator Agent"]["role"], agent_definitions["Prompt Generator Agent"]["function"], model)
    completeness_agent = Agent(agent_definitions["Completeness Agent"]["name"], agent_definitions["Prompt Generator Agent"]["role"], agent_definitions["Prompt Generator Agent"]["function"], model)

    intermediate_agents = []
    for name in list_of_intermediate_agents:
        if name in agent_definitions and name != "Prompt Generator Agent" and name != "Consolidator Agent" and name != "Completeness Agent":
            new_agent = Agent(agent_definitions[name]["name"], agent_definitions[name]["role"], agent_definitions[name]["function"], model)
            intermediate_agents.append(new_agent)

    agents_dict = {
        "Prompt Generator Agent": prompt_generator_agent,
        "Intermediate Agents": intermediate_agents,
        "Consolidator Agent": consolidator_agent,
        "Completeness Agent": completeness_agent
    }
    
    return agents_dict


if __name__ == '__main__':
    agents_dict = initialize_prompt_agents(["Clarity Agent", "monkeface", "Relevance Agent"], "gpt-4o-mini")

    print(agents_dict)

    monke = agents_dict["Prompt Generator Agent"]

    output = monke.run_api("Give the recipe for frying salmon")
    print(output)

"""
Code:
if __name__ == '__main__':
    agents_dict = initialize_prompt_agents(["Clarity Agent", "monkeface", "Relevance Agent"], "gpt-4o-mini")

    print(agents_dict)

    monke = agents_dict["Prompt Generator Agent"]

    output = monke.run_api("Give the recipe for frying salmon")
    print(output)

Output:
{'Prompt Generator Agent': <__main__.Agent object at 0x7f2d3e45ffd0>, 'Intermediate Agents': [<__main__.Agent object at 0x7f2d3bf99750>, <__main__.Agent object at 0x7f2d3bf99780>], 'Consolidator Agent': <__main__.Agent object at 0x7f2d3e663fd0>, 'Completeness Agent': <__main__.Agent object at 0x7f2d3e663ca0>}
Provide a detailed recipe for frying salmon, including the ingredients, step-by-step cooking instructions, and any tips for achieving the best flavor and texture.
"""