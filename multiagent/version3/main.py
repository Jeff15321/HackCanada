from agent_system import *



list_of_agents = ["Task Determinator Agent", "Prompt Generator Agent", "Process Creator Agent", "Search Agent", "Title Context Agent", "Task Context Agent", "Clarity Agent", "Relevance Agent", "Precision Agent", "Brevity Agent", "Consolidator Agent", "Completeness Agent", "Search Consolidator Agent"]
instructional_files = ["./documents/PsychRubric.pdf"] # files to be read in full
supplementary_files = ["./documents/A_Dolls_House.pdf", "./IA_ZhuDi.pdf"] # files to be rag'd and take exerpts from

# task = "Examine documents to determine degree of risk from factors such as applicant health, financial standing and value, and condition of property."
# role = "Insurance Underwriters"

task = "Write an essay for IB Higher Level English class on the WIT (Works in Translation) book 'A Doll's House' based on the following topic: How does Nora demonstrate strength in the face of conventional morality in A Doll’s House?"
role = "IB HL English Class student"

refine_rounds = 2
search_rounds = 2
model = "gpt-4o-mini"



if __name__ == '__main__':
    monkeSystem = multiagentSystem(list_of_agents, instructional_files, supplementary_files, model)
    monkeSystem.run(task, role, 2, 2)