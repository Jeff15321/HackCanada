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
Complete Question 1 of Professional Development Course Assignment on Professional Responsibility in Computing (response between 200-300 words). Follow exactly the format specified in the a1-question1-format.pdf file and the assignment instructions:
Question 1
As mentioned in the lectures, the Canadian Copyright Act normally bconfers on your Employer only the copyright in creations that you make as part of your job. It does not extend to creations that you make outside of your job. Thus, by default, you hold a copyright on any creation that you make outside of work, on your own time and using your own resources. That said, when you sign an employment contract, you might be agreeing to assign to your Employer the IP rights to all creations that you make inside and outside of your job. If so, this contract supersedes the Canadian Copyright Act.

Part i. Provide a concrete example of a hypothetical product or creation you might make as a side project outside of the course of work (e.g., at home at night). If you are currently working outside of Canada, assume that you are working in Canada for this assignment. Provide enough details so that you can refer back to this example as you're answering the next set of questions below. What resources (e.g. time, equipment) are you using in your side project?”

Part ii. Explain what bearing each of the following would have on whether you or your Employer would have IP rights on this product or creation:

The Canadian Copyright Act, Section 13 (other sections are not directly applicable; see Unit 2 Key Terms for definitions).
Your current employment contract, or this Partial Employment Contract.
Your job description, the nature of your work for your Employer, and the current business interests of your Employer. If you are not currently employed, assume that your job responsibilities are related to your example product, and your example product falls within the realm of the business interests of that company.
"""


task_input = {
    "Input Information": {
        'task': pd_prompt, 
        'context': 'Academic Writing',
        'audience': 'LLM',
        'tone': 'Clear',
        'output_format': 'Structured Text'
    },
    "Instructional Files": ["./documents/pd10_a1/assignment-1.pdf", "./documents/pd10_a1/a1-question1-format.pdf"],
    "Supplementary Files": ["./documents/pd10_a1/Onboarding_Documents.pdf", "./documents/pd10_a1/Rubric_Assignment_1_Who_Owns_the_Copyright_to_Your_Work_Question_1.pdf", "./documents/pd10_a1/PD10_Unit1_Professional_Responsibility_In_Computing.pdf", "./documents/pd10_a1/PD10_Unit2_Intellectual_Property_Creators.pdf", "./documents/pd10_a1/Waterloo_Policy_73_Numbered.pdf"]
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