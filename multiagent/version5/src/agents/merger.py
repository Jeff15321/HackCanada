from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from ..utils.types import TaskState
from ..utils.helpers import create_system_prompt
from ..definitions.agent_definitions import agent_definitions

merger_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def merger_with_agent(state: TaskState) -> TaskState:
    """
    Merges partial_results into one coherent output, in subtask order.
    Then calls the Merger Agent for final formatting/organization.
    """
    plan_keys = list(state["task_plan"]["plan"].keys())

    # Gather partial results in plan order
    partials_text = []
    for k in plan_keys:
        sub_res = state["partial_results"].get(k, "")
        partials_text.append(f"--- {k} ---\n{sub_res}\n")

    combined_subtasks = "\n".join(partials_text)

    # Pass everything to the Merger Agent
    system_prompt = create_system_prompt(agent_definitions["Merger Agent"])
    user_prompt = (
        f"Original Task:\n{state['input_prompt']}\n\n"
        f"Here are the subtask outputs (in order):\n{combined_subtasks}\n\n"
        "Please merge these into a coherent final product."
        "\nYou also have access to the same instructional guidelines below:\n"
        f"{state['instructional_content']}"
    )

    messages = [
        AIMessage(role="system", content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        llm_response = merger_llm(messages)
        merged_text = llm_response.content.strip()
    except Exception as e:
        print(f"ERROR - Merger Agent error: {e}")
        merged_text = "Error occurred in merger agent."

    # print("\n=== MERGER WITH AGENT ===\nMerged output:\n", merged_text)
    return {
        **state,
        "merged_result_with_agent": merged_text,
        "merged_result": merged_text
    } 