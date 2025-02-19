import prompt_refinement.dspy_prompt_refiner
import prompt_refinement.agent_system 
import task_execution.agent_system 

import time

model = "gpt-4o-mini"

# prompt system
list_of_agents = ["Prompt Generator Agent", "Process Creator Agent", "Task Context Agent", "Clarity Agent", "Relevance Agent", "Precision Agent", "Brevity Agent", "Consolidator Agent", "Search Agent", "Search Consolidator Agent", "Completeness Agent"]
refinement_rounds = 2
search_rounds = 2

# task execution system
task_execution_rounds = 3

####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################

pd_prompt = """
Refine and enhance the language, structure, and clarity of Critical Essay 3 about Ensmenger's and Dhar's work to align with the expectations outlined in the Critical Essay Rubric. Preserve the original content and main arguments of the essay, focusing only on improving its coherence, organization, grammar, and adherence to rubric criteria. Do not alter the essay’s key points or central message.
"""


task_input = {
    "Input Information": {
        'task': pd_prompt, 
        'context': 'Academic Writing',
        'audience': 'LLM',
        'tone': 'Clear',
        'output_format': 'Structured Text'
    },
    "Instructional Files": ["./documents/Critical Essay Rubric.pdf"],
    "Supplementary Files": ["./documents/Critical Essay 3.pdf"]
}

####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################

if __name__ == '__main__':
    info = task_input["Input Information"]

    #### Prompt Refinement: dspy #####
    t1 = time.time()
    refined_prompt = prompt_refinement.dspy_prompt_refiner.get_refined_prompt(info["task"], info["context"], info["audience"], info["tone"], info["output_format"], prompt_refinement.dspy_prompt_refiner.compiled_generator)
    t2 = time.time()

    print(f"############### DSpY Refined Prompt (Time Taken: {t2-t1}) ###############")
    print(refined_prompt)

    ##### Prompt Refinement: multiagent #####
    promptSystem = prompt_refinement.agent_system.multiagentSystem(list_of_agents, task_input["Instructional Files"], task_input["Supplementary Files"], model)
    t1 = time.time()
    refined_prompt = promptSystem.run(info["task"], info["context"], refined_prompt, refinement_rounds, search_rounds)
    t2 = time.time()

    print(f"############### Multiagent (further) Refined Prompt (Time Taken: {t2-t1}) ###############")
    print(refined_prompt)

    ##### Task Execution: multiagent #####
    executionSystem = task_execution.agent_system.multiagentTaskExecutionSystem(task_input["Instructional Files"], task_input["Supplementary Files"], model)
    t1 = time.time()
    task_output = executionSystem.run(info["task"], info["context"], refined_prompt, task_execution_rounds)
    t2 = time.time()

    print(f"############### Multiagent Task Execution (Time Taken: {t2-t1}) ###############")
    print(task_output)