from agent_system import *



list_of_agents = ["Task Determinator Agent", "Prompt Generator Agent", "Process Creator Agent", "Search Agent", "Title Context Agent", "Task Context Agent", "Clarity Agent", "Relevance Agent", "Precision Agent", "Brevity Agent", "Consolidator Agent", "Completeness Agent"]
list_of_file_paths = ["./IA_ZhuDi.pdf"]

task = "Examine documents to determine degree of risk from factors such as applicant health, financial standing and value, and condition of property."
role = "Insurance Underwriters"

rounds = 2
model = "gpt-4o-mini"



if __name__ == '__main__':
    monkeSystem = multiagentSystem(list_of_agents, list_of_file_paths, model)
    monkeSystem.run(task, role, 2)