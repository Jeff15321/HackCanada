from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from ..utils.types import TaskState
from ..utils.helpers import create_system_prompt
from ..definitions.agent_definitions import agent_definitions
from ..rag.retriever import get_relevant_context

executor_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def make_executor(subtask_name: str):
    """
    Creates a node function that uses the subtask instructions + overall prompt +
    the global instructional content. Also fetches relevant RAG context.
    """
    def executor_fn(state: TaskState) -> TaskState:
        # Get the subtask data from the plan
        subtask_data = state["task_plan"]["plan"][subtask_name]
        instructions = subtask_data["subtask_steps"]
        semantic_query = subtask_data["semantic_query"]
        
        # Format instructions as a numbered list
        formatted_instructions = "\n".join(f"{i+1}. {step}" for i, step in enumerate(instructions))
        
        # ONLY the executor uses RAG to fetch relevant context
        rag_context = ""
        if state["has_rag"]:
            # Use the semantic query for RAG
            rag_context = get_relevant_context(semantic_query, k=3)

        # Build final prompt for the subtask
        full_prompt = f"""You are a grad student writing a critical essay on the environmental history of computing.

For the subtask "{subtask_name}", follow these instructions in order:

{formatted_instructions}

Use the following relevant context from source materials to support your response:
{rag_context}

Your response should:
- Address each instruction point thoroughly
- Use specific examples and evidence from the provided context
- Maintain an academic writing style
- Be detailed and well-structured
"""

        system_text = create_system_prompt(agent_definitions['Task Executor Agent'])
        msgs = [
            AIMessage(role="system", content=system_text),
            HumanMessage(content=full_prompt)
        ]
        
        try:
            # Use invoke instead of direct call
            response = executor_llm.invoke(msgs)
            output_text = response.content.strip()
        except Exception as e:
            print(f"ERROR - Executor {subtask_name} error: {e}")
            output_text = f"Error occurred in {subtask_name}."

        return {
            "partial_results": {subtask_name: output_text}
        }
    return executor_fn 