task_execution_plan_format = f"""
The task execution plan organizes subtasks and their steps to complete the overall task. It is a JSON dictionary where each subtask (key) has a list of steps (values), with each step building on the previous one. Subtasks are sequentially combined to form the final output.

When structuring subtasks and steps, ensure coherence in the final merged result. Each step should be as detailed as possible to provide maximum clarity and completeness.
"""

list_of_metrics_format = f"""
The List of Metrics is a dictionary (dict[str, str]) where each key is the name of a metric, and the value is its description.
Each metric name concisely identifies the evaluation criterion, while the description provides a clear explanation of what it measures.
"""

verification_output_format = f"""
The Verification Output is a dictionary (dict[str, tuple[bool, str]]) where each key is a metric name, and the value is a tuple containing a pass/fail boolean and a comment regarding how the output performs on said metric.
"""


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################


agent_definitions = {
    "Task Planner Agent": {
        "name": "Task Planner Agent",
        "role": "The Task planner Agent is responsible for creating a detailed plan to complete the given task. Break down the overall task into subtasks that are smaller, maneagable actions. Within each subtask, split it into steps of actions that build on top of each other to arrive at the best result for the subtask. The steps within each subtask build upon each other sequentially while the subtasks are combined to form the final output for the overall task exeuction. Return a structured plan outlining the neessary subtasks and steps to complete the task effectively",
        "function": f"Based on the input task from the prompt, look through the instructional files and the supplementary file summaries. Then generate the task execution plan only and follow EXACTLY the format and specifications outlined below:\n{task_execution_plan_format}"
    },
    "Task Executor Agent": {
        "name": "Task Executor Agent",
        "role": "Responsible for executing a specific subtask by leveraging the provided super prompt, instructional files, and supplementary retrieval-augmented generation (RAG) files.",
        "function": "Processes the assigned subtask by following a structured list of steps, extracting relevant information from the provided resources, and generating a well-formed output that aligns with the task requirements."
    },
    "Merger Agent": {
        "name": " Agent",
        "role": "Combine the outputs from the subtasks together in a coherent and organzied way to create the final output for the task execution.",
        "function": (
            "Analyze the provided super prompt, instructional files, and task execution breakdown. Each subtask contributes to the overall task, and all outputs must be merged into a coherent final product."
            f"\nTask execution plan format:\n{task_execution_plan_format}"
            "\nYou will receive the task execution plan, ordered subtasks, and their outputs. Your role is to merge these outputs seamlessly without altering content. You can add transitions may be added only if necessary. Return only the final merged output."
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
        "role": "Evaluate the task output against the given metrics based on the task prompt and instructional files.",
        "function": (
            "Analyze the task prompt and instructional files to understand requirements. Carefully review the task output and assess it using the provided metrics, determining whether it meets expectations with detailed reasoning."
            f"\nFollow this exact format:\n{verification_output_format}"
            "\nReturn only the formatted verification output—nothing else. Be specific in comments, referencing exact parts of the task output with as much relevant detail as possible."
            "\n(Formatting Note: Precede apostrophes with a backslash (\\) to prevent parsing errors, e.g., use that\\'s instead of that's.)"
        )
    }
}

if __name__ == '__main__':
    print(list_of_metrics_format)