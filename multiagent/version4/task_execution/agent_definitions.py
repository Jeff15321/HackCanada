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

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

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
Subtask: Write about potential solutions to mitigate climate change
Subtask items as formatted from task execution plan:
[
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
Subtask: Write conclusion summarizing key findings and recommendations
Subtask items as formatted from task execution plan:
[
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

list_of_metrics_example = [
    {"metric": "Clarity and Conciseness", "description": "The report is easy to understand and avoids unnecessary jargon or wordiness.  Information is presented efficiently."},
    {"metric": "Accuracy of Information", "description": "All facts, figures, and data presented are correct and verifiable. Sources are properly cited."},
    {"metric": "Completeness", "description": "The report covers all aspects of the assigned topic comprehensively.  No significant information is missing."},
    {"metric": "Logical Structure and Organization", "description": "The report follows a clear and logical structure with a well-defined introduction, body, and conclusion.  Sections are appropriately organized and flow smoothly."},
    {"metric": "Grammar and Mechanics", "description": "The report is free of grammatical errors, spelling mistakes, and punctuation issues."},
    {"metric": "Style and Tone", "description": "The writing style is appropriate for the intended audience and purpose.  The tone is consistent and professional."},
    {"metric": "Citation and Referencing", "description": "Sources are properly cited using a consistent citation style (e.g., APA, MLA).  A bibliography or works cited page is included."},
    {"metric": "Adherence to Formatting Guidelines", "description": "The report follows all specified formatting guidelines, including font, spacing, margins, and page numbers."},
    {"metric": "Originality", "description": "The report demonstrates original thought and analysis, rather than simply summarizing existing information.  Appropriate attribution is given to sources."},
    {"metric": "Overall Impact", "description": "The report effectively communicates its findings and makes a clear and convincing argument (if applicable)."}
]

verification_input_example = """
Metric: Clarity and Conciseness
Description: The report is easy to understand and avoids unnecessary jargon or wordiness.  Information is presented efficiently.
"""

# note for outputs: the metric itself will be added in code
verification_output_pass_example = {
    "pass": True,
    "comments": "The report is exceptionally clear and concise.  The language used is accessible, and the information flows logically and efficiently. No unnecessary jargon or overly complex sentence structures were observed."
}

verification_output_fail_example = {
    "pass": False,
    "comments": "The report suffers from several instances of unclear writing and excessive jargon.  Several sentences are overly long and complex, hindering readability.  For example, the section on [specific section] could be significantly improved with simpler language and more direct phrasing.  The use of technical terms like [specific jargon term] without sufficient explanation also impacts clarity."
}

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

list_of_metrics_format = f"""
The list of metrics serves as a checklist to evaluate the accuracy, completeness, efficiency, adherence to instructions, style guidelines (if specified), and the overall quality of the task execution output.
The list of metrics format is a list where each item is a dictionary that has a "metric" key and a "description" key. The item "metric" is the specific metric that must be assessed, and the corresponding item in "description" outlines what the metric is about and what is expected.
For example, a list of metrics for a generic report could be:
{list_of_metrics_example}
"""

verification_output_format = f"""
Each verification output takes one metric along with its description and evaluates the expecatations for the task output based on that metric, determing whether it passes the metric or not.
The verification output format is a dictionary with two items: the first item has the exact key "pass" and a boolean value indicating whether it is True or False that the task output passes the metric, the second item has the exact key "comments" and provides comments on specifically what was good or bad about the task output based on that metric.
For example, for a report writing task, with this metric as input:
{verification_input_example}
If it is determined that the task output fullfils the expectations and requirements then a potential output would be in the format:
{verification_output_pass_example}
If it is determined that the task output does not fullfil the expecations and requirements then it would look something like:
{verification_output_fail_example}
"""

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

overall_task_agent_definitions = {
##### agents during the pre-work/process creating stage #####
    "Summarizer Agent": {
        "name": "Summarizer Agent",
        "role": "Analyze and process the content of a file, providing a concise summary of its key themes, main points, and critical details.",
        "function": "Generate a clear and structured summary in a short paragraph, highlighting the primary subject matter, key insights, and any significant information or takeaways from the file."
    },
    "Task Planner Agent": {
        "name": "Task Planner Agent",
        "role": "The Task planner Agent is responsible for creating a detailed plan to complete the given task. Break down the overall task into subtasks that are smaller, maneagable actions. Within each subtask, split it into steps of actions that build on top of each other to arrive at the best result for the subtask. The steps within each subtask build upon each other sequentially while the  subtasks are combined to form the final output for the overall task exeuction. Return a structured plan outlining the neessary subtasks and steps to complete the task effectively",
        "function": f"Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then generate the task execution plan only and follow EXACTLY the format and specifications outlined below:\n{task_execution_plan_format}"
    },
    # (this version of Task Delegator Agent is where there's one for each subtask in the overall task)
    "Task Delegator Agent": {
        "name": "Task Delegator Agent",
        "role": "Given the prompt which includes the prompt for the entire task, the instructional files, the supplementary file summaries, and the formatted task execution plan: for your assgined subtask, choose the best suited task execution agent to delgate each step of the subtask to",
        "function": (
            "Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then examined the formatted task execution plan where each item in it is a subtask that goes into the bigger picture. Then, locate your subtask and steps: identify where it is in the bigger picture of the overall task, what your subtask is about, and determine what task executor agent is best for completing each step that subtask. Only pick names from the specified executor agents.\n"
            f"The format specifications are as follows:\n{subtask_delegation_plan_format}\n"
            "Return exactly in the specified format and structure as defined for the subtask delegation plan."
        )
    },
##### agents to make sure the work is legit (save these for later :monkey:)#####
    "Merger Agent": {
        "name": "Merger Agent",
        "role": "Combine the outputs from the subtasks together in a coherent and organzied way to create the final output for the task execution.",
        "function": (
            "Examine the prompt which includes the prompt for the entire task, the instructional files, and the task execution which shows the subtasks that the task has been broken down into. Each subtask is a part of the overall task to be completed and all its contents must be merged in in a way that makes sense and is coherent."
            f"The task execution plan is formatted as follows:\n{task_execution_plan}"
            "You will be given the specific task execution plan for the task being executed, the list of the subtasks in order, and the outputs for each subtask. You are to combine the outputs from the subtasks into one large output that will be the final product of the task execution. Do not remove or modify any information, you are only to merge them in a coherent manner. You may add minimal transitions between subtask sections if absolutely necessary. Do not return anything other than the final product which consists of the subtasks section merge together."
        )
    },
    "Standards Agent": {
        "name": "Standards Agent",
        "role": "Examine the original task prompt and instructional files for said task, then determine a list of metrics to check for in list format",
        "function": (
            "Analyzes the provided task prompt and any associated instructional files to identify key aspects and generate a structured list of verification metrics. These metrics will serve as a checklist to assess the completeness and correctness of any solution generated for the task.\n"
            f"The output format specifications and instructions are outlined below:\n{list_of_metrics_format}"
            "Consider various aspects, including but not limited to: accuracy, completeness, efficiency, adherence to instructions, style guidelines (if specified), and the overall quality of the solution.\n"
            "Only return the properly formatted list of metrics in the format specified above. Do not return anything else. Do not include anything about visuals or graphcial/display concerns"
        )
    },
    "Verificiation Agent": {
        "name": "Verification Agent",
        "role": "Examine the original task prompt and the instructional files for said task. Then, go through the task output and evaluate it based on the given metric for evaluation.",
        "function": (
            "Examine the original task prompt and the instructional files for the task to understand what the task is about. Then, closely read the entirety of the task output and evaluate it based on a given metric of evaluation. Determine whether the task output fullfils the expectations and write in detail why or why not.\n"
            f"This is the exact format you are to follow:\n{verification_output_format}\n"
            "Only return the properly formatted verification output as specified above. Do not return anything else. Make sure to be specific in your comments and reference exact parts of the task output, include as much relevant information as possible in the comments item."
        )
    },
}




if __name__ == '__main__':
    # print(subtask_delegation_plan_format)
    print("nothingness")