from prompt_refinement.model import *
from prompt_refinement.agent_definitions import agent_definitions

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

class InstructionalFileAgents(Agent): # Literally for Prompt Generator Agent and Process Creator Agent (or any that take the instructional/full files)
    def __init__(self, name, role, function, model, instructional_files):
        super().__init__(name, role, function, model)
        self.instructional_files = instructional_files
    
    def run_api(self, input_prompt):
        text_prompt = self.query_llm(input_prompt)
        agent_role = self.role
        response = run_gpt_with_file(text_prompt, agent_role, self.instructional_files, self.model)
        return response

class CompletenessAgent(Agent):
    def query_llm(self, input_prompt, original_task):
        """Ensures the final prompt includes all critical components from the original task."""
        system_prompt=f"You are a: {self.name}. Your role: {self.role}. Your function: {self.function}."

        full_prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
        Original Task: {original_task}
        # Final Prompt: {input_prompt}
        # Make sure the final prompt contains all requirements of the original task. Modify the prompt if necessary and return only the final prompt in the specified format.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        return full_prompt
    
    def run_api(self, input_prompt, original_task):
        text_prompt = self.query_llm(input_prompt, original_task)
        agent_role = self.role
        response = run_gpt(text_prompt, agent_role, self.model)
        return response

class SearchAgent(Agent): # one SearchAgent instance will be created per file uploaded
    def __init__(self, name, role, function, model, file_path):
        super().__init__(name, role, function, model)
        self.file_path = file_path

    def query_llm(self, input_prompt):
        """Simulates querying the LLM with a role-specific prompt."""
        system_prompt=f"You are a: {self.name}. Your role: {self.role}. Your function: {self.function}."
        full_prompt=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>Based on your role and function, provide the relevant information from the file that should be added to the new prompt. Do not give me anything else other than what was just specified.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        return full_prompt

    def run_api(self, input_prompt):
        text_prompt = self.query_llm(input_prompt)
        agent_role = self.role
        response = run_gpt_with_rag(text_prompt, agent_role, self.file_path, self.model)
        return response

"""
returns:
{
    [agent name]: [corresponding agent object],
    ...
}
"""
def initialize_prompt_agents(list_of_agents, instructional_files, supplementary_files, model):
    agents_dict = {}
    for file_path in supplementary_files: # one SearchAgent per file uploaded
        name = "Search Agent"
        new_search_agent = SearchAgent(agent_definitions[name]["name"] + f" {file_path}", agent_definitions[name]["role"], agent_definitions[name]["function"], model, file_path)
        agents_dict[new_search_agent.name] = new_search_agent
    for name in list_of_agents:
        if name == "Search Agent": # prevent duplicate Search Agents that don't actually do anything
            continue
        elif name == "Completeness Agent":
            completeness_agent = CompletenessAgent(agent_definitions["Completeness Agent"]["name"], agent_definitions["Completeness Agent"]["role"], agent_definitions["Completeness Agent"]["function"], model)
            agents_dict[completeness_agent.name] = completeness_agent
        elif name == "Prompt Generator Agent" or name == "Process Creator Agent":
            new_agent = InstructionalFileAgents(agent_definitions[name]["name"], agent_definitions[name]["role"], agent_definitions[name]["function"], model, instructional_files)
            agents_dict[new_agent.name] = new_agent
        else:
            new_agent = Agent(agent_definitions[name]["name"], agent_definitions[name]["role"], agent_definitions[name]["function"], model)
            agents_dict[new_agent.name] = new_agent
    return agents_dict

if __name__ == '__main__':
    # list_of_agents = ["Task Determinator Agent", "Prompt Generator Agent", "Process Creator Agent", "Search Agent", "Title Context Agent", "Task Context Agent", "Clarity Agent", "Relevance Agent", "Precision Agent", "Brevity Agent", "Consolidator Agent", "Completeness Agent", "Search Consolidator Agent"]
    # list_of_file_paths = ["./IA_ZhuDi.pdf"]

    # agents_dict = initialize_prompt_agents(list_of_agents, list_of_file_paths, "gpt-4o-mini")

    # print(agents_dict)
    print("nothingness")