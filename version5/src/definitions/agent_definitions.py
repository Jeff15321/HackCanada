task_execution_plan_format = """
The task execution plan organizes subtasks and their steps to complete the overall task. It is a list of dictionaries where dictionary has a subtask (key) and the list of steps for doing each subtask (values). The subtasks are combined in parallel to form the final output.

For example, if the task is writing an essay about the benefits of AI in health:
[
    {
        "subtask_name": "introduction",
        "subtask_steps": ["Define AI...", "Explain context..."],
        "semantic_query": "artificial intelligence definition healthcare context benefits introduction overview fundamentals"
    },
    {
        "subtask_name": "background",
        "subtask_steps": ["Research the current state...", "Collect stats..."],
        "semantic_query": "healthcare AI current state statistics research data implementation adoption trends"
    },
    {"subtask_name": "benefit_1", "subtask_steps": ["Describe first benefit...", "Give example..."]},
    {"subtask_name": "benefit_2", "subtask_steps": ["Describe second benefit...", "Give example..."]},
    {"subtask_name": "benefit_3", "subtask_steps": ["Describe third benefit...", "Give example..."]},
    {"subtask_name": "conclusion", "subtask_steps": ["Summarize points...", "Give final thoughts..."]}
]

When structuring subtasks and steps:
1. Ensure coherence in the final merged result
2. Make each step as detailed as possible
3. Include a semantic query with relevant keywords and concepts for effective document search
4. The semantic query should include synonyms and related terms to improve search results

Subtasks are completed IN PARALLEL, bad subtasks would be something like: [do research, write outline, do draft] since those tasks are dependent on the previous task. Good subtasks would be say splitting an essay into the different paragraphs, and then within the steps for each subtask then you have the steps (like do research, write outline, do draft, review, etc) that build upon the previous steps.

YOU MUST SPLIT THE TASK INTO MULTIPLE SUBTASKS
"""

list_of_metrics_format = """
The List of Metrics is a dictionary (dict[str, str]) where each key is the name of a metric, and the value is its description.
Each metric name concisely identifies the evaluation criterion, while the description provides a clear explanation of what it measures.
"""

verification_output_format = """
The Verification Output is a dictionary (dict[str, tuple[bool, str]]) where each key is a metric name, and the value is a tuple containing a pass/fail boolean and a comment regarding how the output performs on said metric. \n 
"""

agent_definitions = {
    "Task Planner Agent": {
        "name": "Task Planner Agent",
        "role": "The Task planner Agent is responsible for creating a detailed division of subtasks to complete the given task. Break down the overall task into subtasks that are smaller, maneagable actions that can be done independent of each other. Within each subtask, split it into steps of actions that build on top of each other to arrive at the best result for the subtask. The steps within each subtask build upon each other sequentially while the subtasks are combined to form the final output for the overall task exeuction. Return a structured plan outlining the neessary subtasks and steps to complete the task effectively",
        "function": f"Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then generate the task execution plan only and follow EXACTLY the format and specifications outlined below:\n{task_execution_plan_format}"
    },
    "Task Executor Agent": {
        "name": "Task Executor Agent",
        "role": "Responsible for executing a specific subtask by leveraging the provided super prompt, instructional files, and supplementary files information.",
        "function": "Processes the assigned subtask by following a structured list of steps, extracting relevant information from the provided resources, and generating a well-formed output that aligns with the task requirements. Unless explicitly stated, do NOT write a conclusion.",
    },
    "Merger Agent": {
        "name": "Merger Agent",
        "role": "Expert academic editor responsible for synthesizing subtask outputs into a coherent essay that strictly adheres to word count and formatting requirements. Focus on preserving key arguments and evidence while meeting length constraints.",
        "function": (
            "Your primary tasks are:\n"
            "1. FOLLOW LENGTH REQUIREMENTS: Strictly adhere to word count limits from instructions\n"
            "2. PRESERVE KEY CONTENT: Maintain core arguments and evidence from each section\n"
            "3. INTEGRATE EFFICIENTLY: Combine sections while eliminating redundancy\n"
            "4. MAINTAIN FLOW: Add brief transitions between sections\n"
            "5. ENSURE COVERAGE: Represent all subtasks proportionally\n\n"
            "When merging content:\n"
            "- Prioritize unique insights and key evidence\n"
            "- Remove redundant examples while keeping the strongest ones\n"
            "- Ensure balanced coverage of all subtasks\n"
            "- Stay within word count limits while preserving the most important content"
        )
    },
    "Standards Agent": {
        "name": "Standards Agent",
        "role": "Review the task prompt and instructional files to generate a structured list of verification metrics.",
        "function": (
            "Extracts key aspects from the task prompt and instructional files to create a checklist of evaluation metrics."
            f"\nOutput must follow this format:\n{list_of_metrics_format}"
            "\nMetrics should cover accuracy, completeness, efficiency, adherence to instructions, overall quality, and any metrics or things important for the specific task being assessed."
            "Return only the formatted list of metrics—exclude any visual or graphical concerns."
        )
    },
    "Verification Agent": {
        "name": "Verification Agent",
        "role": "Review the essay output with a focus on basic requirements and overall quality. Be generous in assessment and avoid strict academic criteria.",
        "function": (
            "Review the essay for basic requirements:\n"
            "1. Content Coverage: Main topics are addressed\n"
            "2. Basic Structure: Clear organization exists\n"
            "3. Length: Reasonably close to target\n"
            "4. Clarity: Writing is understandable\n"
            "5. Topic Relevance: Stays on topic\n\n"
            "Default to passing unless there are major issues. Citations are not required.\n"
            "Focus on whether the content is informative and well-organized."
        )
    }
} 