from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from ..utils.types import TaskState
from ..utils.helpers import create_system_prompt
from ..definitions.agent_definitions import agent_definitions

merger_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def merger_with_agent(state: TaskState) -> TaskState:
    """
    Merges partial_results into one coherent output, following word count and formatting requirements.
    Focuses on preserving key content while meeting length constraints.
    """
    plan_keys = list(state["task_plan"]["plan"].keys())

    # Extract word count requirement from instructions
    word_count_limit = 2500  # Default if not found
    instructional_content = state["instructional_content"].lower()
    if "word" in instructional_content and "count" in instructional_content:
        # Look for patterns like "word count: 2000" or "2000 words"
        import re
        word_counts = re.findall(r'(\d+)(?=\s*(?:word|words))|(?:word count:?\s*)(\d+)', instructional_content)
        if word_counts:
            # Use the first number found
            word_count = next(int(num) for nums in word_counts for num in nums if num)
            if word_count > 0:
                word_count_limit = word_count

    # Gather partial results in plan order with section markers
    partials_text = []
    for k in plan_keys:
        sub_res = state["partial_results"].get(k, "")
        partials_text.append(f"=== BEGIN SECTION: {k} ===\n{sub_res}\n=== END SECTION: {k} ===\n")

    combined_subtasks = "\n".join(partials_text)

    # Pass everything to the Merger Agent with clear instructions
    system_prompt = create_system_prompt(agent_definitions["Merger Agent"])
    user_prompt = (
        f"You are merging sections of an academic essay about the environmental history of computing. "
        f"Your task is to create a coherent essay that meets the following requirements:\n\n"
        
        f"CRITICAL REQUIREMENTS:\n"
        f"1. WORD COUNT LIMIT: {word_count_limit} words - This is a strict requirement\n"
        f"2. PRESERVE CORE CONTENT: Keep the most important arguments and evidence from each section\n"
        f"3. MAINTAIN BALANCE: Ensure all subtasks are represented proportionally\n"
        f"4. REMOVE REDUNDANCY: Eliminate repeated information while keeping the strongest examples\n"
        f"5. ADD TRANSITIONS: Include brief transitions between sections\n\n"
        
        f"Original Task Context:\n{state['input_prompt']}\n\n"
        
        f"Instructional Guidelines:\n{state['instructional_content']}\n\n"
        
        f"Essay Sections to Merge:\n{combined_subtasks}\n\n"
        
        f"Create a focused essay that:\n"
        f"1. Stays STRICTLY within {word_count_limit} words\n"
        f"2. Preserves the most important content from each section\n"
        f"3. Maintains academic quality and argumentation\n"
        f"4. Follows all formatting requirements\n"
        f"5. Creates a coherent narrative flow"
    )

    messages = [
        AIMessage(role="system", content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        # Use invoke instead of direct call
        llm_response = merger_llm.invoke(messages)
        merged_text = llm_response.content.strip()
        
        # Verify word count
        word_count = len(merged_text.split())
        if word_count > word_count_limit * 1.1:  # Allow 10% margin
            # Try one more time with stronger emphasis on length
            user_prompt += f"\n\nWARNING: Your previous response was too long ({word_count} words). Please create a new version that is STRICTLY under {word_count_limit} words while preserving the most important content."
            messages = [
                AIMessage(role="system", content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            llm_response = merger_llm.invoke(messages)
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