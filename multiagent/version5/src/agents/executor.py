from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from ..utils.types import TaskState
from ..utils.helpers import create_system_prompt
from ..definitions.agent_definitions import agent_definitions
from ..rag.retriever import get_relevant_context

executor_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def make_executor(subtask_name: str):
    """
    Creates a node function that uses the subtask instructions + overall prompt +
    the global instructional content. Also fetches relevant RAG context.
    """
    def executor_fn(state: TaskState) -> TaskState:
        instructions = state["task_plan"]["plan"][subtask_name]
        
        # ONLY the executor uses RAG to fetch relevant context
        rag_context = ""
        if state["has_rag"]:
            # Construct a retrieval query from the instructions
            rag_query = (
                f"Find relevant info about subtask: {subtask_name}\n"
                f"For the overall user task: {state['input_prompt']}\n"
                f"Instructions: {'. '.join(instructions)}"
            )
            rag_context = get_relevant_context(rag_query)

        # Build final prompt for the subtask
        full_prompt = f"""Subtask: {subtask_name}
Overall Task: {state['input_prompt']}

Instructions for this subtask:
{instructions}

Instructional Guidelines (always visible to you):
{state['instructional_content']}

Relevant Context from Supplementary Files (only for this subtask):
{rag_context}
"""
        # print(f"\n=== Executor {subtask_name} running ===")
        # print("Prompt:\n", full_prompt)

        system_text = create_system_prompt(agent_definitions['Task Executor Agent'])
        msgs = [
            AIMessage(role="system", content=system_text),
            HumanMessage(content=full_prompt)
        ]
        
        try:
            response = executor_llm(msgs)
            output_text = response.content.strip()
        except Exception as e:
            print(f"ERROR - Executor {subtask_name} error: {e}")
            output_text = f"Error occurred in {subtask_name}."

        # Write the executor output to partial_results
        return {
            "partial_results": {subtask_name: output_text}
        }
    return executor_fn 