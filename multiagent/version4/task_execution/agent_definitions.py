##### actual executor agents that do the work each step #####
subtask_executor_agent_definitions = {
    "Writing Agent": {
        "name": "Writing Agent",
        "role": (
            "Focuses on the subtask of generating detailed and coherent written content to fulfill the overall task requirements."
        ),
        "function": (
            "Use the user's prompt or structured content as input to create high-quality written deliverables. "
            "Ensure the output is clear, relevant, and adheres to specified guidelines, with optimized grammar, language, and formatting for readability and professionalism."
        ),
        "uses_rag": False
    },
    "Search Agent": {
        "name": "Search Agent",
        "role": (
            "Concentrates on the subtask of retrieving relevant information to support the overall content creation process."
        ),
        "function": (
            "Conduct targeted searches within specified documents or databases to extract precise and relevant information. "
            "Provide concise and contextually accurate excerpts or summaries to support the Writing Agent or other agents."
        ),
        "uses_rag": True
    },
    "Content Structuring Agent": {
        "name": "Content Structuring Agent",
        "role": (
            "Handles the subtask of organizing and outlining content to ensure logical flow within the overall task."
        ),
        "function": (
            "Transform raw ideas, input data, or drafts into a clear and logical structure. "
            "Develop outlines, headings, or content frameworks that guide the writing process and contribute to cohesive deliverables."
        ),
        "uses_rag": False
    },
    "Review Agent": {
        "name": "Review Agent",
        "role": (
            "Specializes in the subtask of evaluating and refining written content for quality and alignment with the overall objectives."
        ),
        "function": (
            "Review outputs from the Writing Agent or other agents to ensure accuracy, quality, and adherence to task goals. "
            "Improves the quality of work done by the previous agents, addressing both structural and stylistic elements."
        ),
        "uses_rag": False
    },
}


##### task execution plan and task delegation plan: formatting specifications and examples #####
task_execution_plan_example = {
    "Write introduction on the effects of climate change": [
        "Research causes and overall global effects of climate change",
        "Write introduction to climate change and its global impact",
        "Write definition of climate change and its causes",
        "Write section briefly introducing the trends and overall impact of climate change",
        "Write section briefly introducing climate change's impact specifically on agriculture, coastal regions, and weather patterns"
    ],
    "Write about climate change's overall global impact": [
        "Research climate change's trends and patterns over time"
        "Research climate change's overall global impact",
        "Write section on the trends and overall global impact of climate change",
        "Review and edit section as a whole for cohesiveness and clarity"
    ],
    "Write about climate change's effect on agriculture": [
        "Research climate change's effect on agriculture",
        "Research which types of agriculture and which countries' agricultural output is most affected",
        "Write section on climate change's general effect on agriculture"
        "Write section on which types of agriculture are most affected by climate change",
        "Write section on which countries' agricultural output is most affected",
        "Review and edit section as a whole for cohesiveness and clarity"
    ],
    "Write about climate change's impact on weather patterns": [
        "Research climate change's overall impact on weather patterns",
        "Research which particular weather pattern formations are more likely with increased climate change",
        "Write section on climate change's general impact on weather patterns",
        "Write section on the specific weather pattern formations that are more likely with increased climate change",
        "Review and edit section as a whole for cohesiveness and clarity"
    ],
    "Write about potential solutions to mitigate climate change": [
        "Research potential solutions to mitigate climate change, the effectiveness of each solution, and what challenges there are for implementing them",
        "Write section on mitigation strategies in agriculture",
        "Write section on coastal defense mechanisms",
        "Write section on technological innovations to combat climate change",
        "Write section on the potential solutions to mitigate climate change, the effectiveness of each solution, and what challenges there are for implementing them",
        "Review and edit section as a whole for cohesiveness and clarity"
    ],
    "Write conclusion summarizing key findings and recommendations": [
        "Write summary briefly summarzing the key points on climate change's trends and overall impact, impact on agriculture, impact on coastal regions, and impact on weather patterns",
        "Conclude with closing remarks and key recommendations",
        "Review and edit section as a whole for cohesiveness and clarity"
    ]
}

subtask_delegation_plan_input_example_body = """
Overall subtask: Write about potential solutions to mitigate climate change
Subtask item as formatted from task execution plan:
"Write about potential solutions to mitigate climate change": [
    "Research potential solutions to mitigate climate change, the effectiveness of each solution, and what challenges there are for implementing them",
    "Write section on mitigation strategies in agriculture",
    "Write section on coastal defense mechanisms",
    "Write section on technological innovations to combat climate change",
    "Write section on the potential solutions to mitigate climate change, the effectiveness of each solution, and what challenges there are for implementing them",
    "Review and edit section as a whole for cohesiveness and clarity"
]
"""

subtask_delegation_plan_output_example_body = [
    ("Research potential solutions to mitigate climate change, the effectiveness of each solution, and what challenges there are for implementing them", "Search Agent"),
    ("Write section on mitigation strategies in agriculture", "Writing Agent"),
    ("Write section on coastal defense mechanisms", "Writing Agent"),
    ("Write section on technological innovations to combat climate change", "Writing Agent"),
    ("Write section on the potential solutions to mitigate climate change, the effectiveness of each solution, and what challenges there are for implementing them", "Writing Agent"),
    ("Review and edit section as a whole for cohesiveness and clarity", "Review Agent")
]

subtask_delegation_plan_input_example_conclusion = """
Overall subtask: Write conclusion summarizing key findings and recommendations
Subtask item as formatted from task execution plan:
"Write conclusion summarizing key findings and recommendations": [
    "Write summary briefly summarzing the key points on climate change's trends and overall impact, impact on agriculture, impact on coastal regions, and impact on weather patterns",
    "Conclude with closing remarks and key recommendations",
    "Review and edit section as a whole for cohesiveness and clarity"
]
"""

subtask_delegation_plan_output_example_conclusion = [
    ("Write summary briefly summarzing the key points on climate change's trends and overall impact, impact on agriculture, impact on coastal regions, and impact on weather patterns", "Writing Agent"),
    ("Conclude with closing remarks and key recommendations", "Writing Agent"),
    ("Review and edit section as a whole for cohesiveness and clarity", "Review Agent")
]

task_execution_plan_format = f"""
The task execution plan outlines the overall organization of the subtasks and steps for each subtask that are to be completed in order to complete the overall task.
The task execution plan is in JSON dictionary format, each item (in order) is a subtask that is to be completed: for each item the key is a string with the subtask and the value is a corresponding list of strings where each string in the list is a step in the subtask to complete. In the list of strings for each subtask, each step builds upon the output in the previous steps. Meanwhile, as a whole the subtasks are combined together to make the final task.
When designing the subtask breakdown and the steps within each subtask, take into acount how coherent the final output will be as a whole once as the subtasks are combined.
For each subtask and their steps, make the strings as detailed as possible to give the most information.
For example, for a task of writing a report on climate change, the plan could be broken down as follows (for your actual outputted task execution plan be more detailed than the example, the example is to give you an idea of the format):
{task_execution_plan_example}
"""

subtask_delegation_plan_format = f"""
The subtask delegation plan takes a subtask from the overall task execution plan and determines which agent to delegate each step of the subtask to. The task execution plan format is as follows:
{task_execution_plan_format}
The subtask delegation plan takes one of the items (which is a subtask from the task execution plan) and for the list of strings (which are the steps of the subtask), it replaces each string with a tuple of two strings, where the first is the original string that is the step in the subtask, and the second string specifies which task execution agent to use. Only choose from the existing task execution agents and make sure to keep the exact spelling and capitalization as the agents are specified here:
{subtask_executor_agent_definitions}

For example, in the task execution plan example mentionned above, the input prompt for a body subtask would look like:
{subtask_delegation_plan_input_example_body}
And its subtask delegation output could be:
{subtask_delegation_plan_output_example_body}

For the same example, the conclusion subtask would look like:
{subtask_delegation_plan_input_example_conclusion}
And its subtask delegation output could be:
{subtask_delegation_plan_output_example_conclusion}
"""




overall_task_agent_definitions = {
##### agents during the pre-work/process creating stage #####
    "Summarizer Agent": {
        "name": "Summarizer Agent",
        "role": "Analyze and process the content of a file, providing a concise summary of its key themes, main points, and critical details.",
        "function": "Generate a clear and structured summary in a short paragraph, highlighting the primary subject matter, key insights, and any significant information or takeaways from the file."
    },
    "Task Planner Agent": {
        "name": "Task Planner Agent",
        "role": "The Task planner Agent is responsible for creating a detailed plan to complete the given task. Break down the overall task into subtasks that are smaller, maneagable actions. Within each subtask, split it into steps of actions that build on top of each other to arrive at the best result for the subtask. The steps within each subtask build upon each other sequentially while the overall subtasks are combined to form the final output for the overall task exeuction. Return a structured plan outlining the neessary subtasks and steps to complete the task effectively",
        "function": f"Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then generate the task execution plan only and follow EXACTLY the format and specifications outlined below:\n{task_execution_plan_format}"
    },
    # (this version of Task Delegator Agent is where there's one for each subtask in the overall task)
    "Task Delegator Agent": {
        "name": "Task Delegator Agent",
        "role": "Given the prompt which includes the prompt entire task, the instructional files, the supplementary file summaries, and the formatted task execution plan: for your assgined subtask, choose the best suited task execution agent to delgate each step of the subtask to",
        "function": (
            "Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then examined the formatted task execution plan where each item in it is a subtask that goes into the bigger picture. Then, locate your subtask and steps: identify where it is in the bigger picture of the overall task, what your subtask is about, and determine what task executor agent is best for completing each step that subtask. Only pick names from the specified executor agents.\n"
            f"The format specifications are as follows:\n{subtask_delegation_plan_format}\n"
            "Return exactly in the specified format and structure as defined for the subtask delegation plan."
        )
    },
##### agents to make sure the work is legit (save these for later :monkey:)#####
    "Merger Agent": {
        "name": "Merger Agent",
        "role": "",
        "function": ""
    },
    "Verification Agent": {
        "name": "Verification Agent",
        "role": "",
        "function": ""
    },
    "Standards Agent": {
        "name": "Standards Agent",
        "role": "",
        "function": ""
    },

}


if __name__ == '__main__':
    # print(subtask_delegation_plan_format)