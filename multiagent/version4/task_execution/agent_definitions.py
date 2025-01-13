task_plan_format = """
"""

task_planner_agent_example = """
[
    [
        "research climate change's effect on agriculture",
        "research climate change's effect on coastal regions",
        "research climate change's impact on weather patterns",
        "research potential solutions to mitigate climate change"
    ],
    (
        [
            "write introduction to climate change and its global impacts",
            "write definition of climate change and its causes"
        ],
        [
            "write section on agriculture's vulnerability to climate change",
            "write section on the impact of climate change on coastal regions",
            "write section on the relationship between climate change and extreme weather patterns"
        ],
        [
            "write section on mitigation strategies in agriculture",
            "write section on coastal defense mechanisms",
            "write section on technological innovations to combat climate change"
        ]
    ),
    [
        "synthesize all sections into a coherent draft",
        "write conclusion summarizing key findings and recommendations",
        "review report for clarity and cohesiveness",
        "edit report for grammar and spelling errors"
    ]
]
"""


task_delegator_agent_example = """
[
    [
        {"research climate change's effect on agriculture": "Search Agent"},
        {"research climate change's effect on coastal regions": "Search Agent"},
        {"research climate change's impact on weather patterns": "Search Agent"},
        {"research potential solutions to mitigate climate change": "Search Agent"}
    ],
    (
        [
            {"write introduction to climate change and its global impacts": "Writing Agent"},
            {"write definition of climate change and its causes": "Writing Agent"}
        ],
        [
            {"write section on agriculture's vulnerability to climate change": "Writing Agent"},
            {"write section on the impact of climate change on coastal regions": "Writing Agent"},
            {"write section on the relationship between climate change and extreme weather patterns": "Writing Agent"}
        ],
        [
            {"write section on mitigation strategies in agriculture": "Writing Agent"},
            {"write section on coastal defense mechanisms": "Writing Agent"},
            {"write section on technological innovations to combat climate change": "Writing Agent"}
        ]
    ),
    [
        {"synthesize all sections into a coherent draft": "Writing Agent"},
        {"write conclusion summarizing key findings and recommendations": "Writing Agent"},
        {"review report for clarity and cohesiveness": "Review Agent"},
        {"edit report for grammar and spelling errors": "Review Agent"}
    ]
]
"""


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




overall_task_agent_definitions = {
##### agents during the pre-work/process creating stage #####
    "Summarizer Agent": {
        "name": "Summarizer Agent",
        "role": "Analyze and process the content of a file, providing a concise summary of its key themes, main points, and critical details.",
        "function": "Generate a clear and structured summary in a short paragraph, highlighting the primary subject matter, key insights, and any significant information or takeaways from the file."
    },
    "Task Planner Agent": {
        "name": "Task Planner Agent",
        "role": "The Task Planner Agent is responsible for creating a detailed, step-by-step plan to complete a given task. It should break down the task into smaller, manageable actions or sub-tasks and determine their sequence and dependencies. Some actions may need to be performed sequentially, while others can be done in parallel. The agent will also identify dependencies, meaning some actions can’t begin until others are finished, and will return a structured plan outlining the necessary steps to complete the task efficiently.",
        "function": f"Based on the input task from the prompt, look through the instrutional files and the supplementary file summaries. Then generate a plan in JSON format, where the key is 'task_plan' and its value consisting of a list of actions that need to be taken. Actions are grouped as follows: \n\n1. Sequential tasks (where each action depends on the previous one) will be represented as arrays [] with the order of actions clearly defined. \n2. Parallel tasks (where actions can happen simultaneously) will be represented as tuples () where the order of execution doesn't matter. \n3. A combination of both parallel and sequential actions can be included, using tuples inside arrays or arrays inside tuples as needed. \n\nExample: \nFor a task of writing a report on climate change, the plan could be broken down as follows:\n\n {task_planner_agent_example} \n\nThe Task Planner Agent will consider how parts of the task can be performed in parallel while also considering when certain steps must come before others."
    },
    # (this is the version of the delegator agent that does everything at once)
    "Task Delegator Agent": {
        "name": "Task Delegator Agent",
        "role": "Given the prompt which details the entire task, the instructional files, and the supplementary file summaries, formatted task plan: for each task select a task executor agent that is best suited for the task",
        "function": (
            f"Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then examine the formatted task plan where each part is a subtask that goes into the bigger picture. For each one, determine what task executor agent is best for completing that subtask. \n\n"
            f"The only valid executor agents are as follows:\n\n {subtask_executor_agent_definitions} \n Only pick from the names specified in the executor agents above, do not change the spelling or make up any new agents."
            f"The format of the task plan you will be given is as follows: a plan in JSON format, with a single item where the key is 'task_plan' and its value consisting of a list of actions that need to be taken. Actions are grouped as follows: \n\n1. Sequential tasks (where each action depends on the previous one) will be represented as arrays [] with the order of actions clearly defined. \n2. Parallel tasks (where actions can happen simultaneously) will be represented as tuples () where the order of execution doesn't matter. \n3. A combination of both parallel and sequential actions can be included, using tuples inside arrays or arrays inside tuples as needed. \n\nExample: \nFor a task of writing a report on climate change, the plan could be broken down as follows:\n\n {task_planner_agent_example}. \n\n"
            f"When you are returning, return in exactly the same format and structure as the task plan that you were given, except this time each string will be replaced with a dictionary that has is in the format of {{original subtask string, task executor agent name}}. So for the example of writing a task of writing a report on climate change it would turn out as follows:\n\n {task_delegator_agent_example}"
        )
    },
##### agents to make sure the work is legit (save these for later :monkey:)#####
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
    print(overall_task_agent_definitions["Task Delegator Agent"]["function"])