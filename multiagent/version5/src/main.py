from typing import List

from .utils.types import TaskState
from .utils.helpers import load_instructional_files
from .workflow.graph import create_parallel_workflow
from .agents.planner import generate_task_execution_plan
from .rag.retriever import setup_rag_for_supplementary_files, set_rag_retriever

def process_task(
    prompt: str,
    instructional_pdf_path: str = None,
    supplementary_files: List[str] = None
) -> TaskState:
    """
    Orchestrates:
      1) Loading the instructional PDF (always accessible)
      2) Setting up RAG (only the Task Executors will use it for retrieval)
      3) Generating a plan
      4) Running the parallel execution + merging.
    """
    # 1) Load instructional PDF
    instructional_content = ""
    if instructional_pdf_path:
        instructional_content = load_instructional_files(instructional_pdf_path)
    
    # 2) Setup RAG for supplementary files
    has_rag = False
    if supplementary_files:
        retriever = setup_rag_for_supplementary_files(supplementary_files)
        if retriever:
            set_rag_retriever(retriever)
            has_rag = True
    
    # 3) Generate the plan and convert to expected format
    generated_plan = generate_task_execution_plan(prompt, instructional_content)
    plan_dict = {}
    for st in generated_plan:
        if isinstance(st, dict):
            plan_dict[st['subtask_name']] = {
                "subtask_steps": st['subtask_steps'],
                "semantic_query": st['semantic_query']
            }
        else:
            plan_dict[st.subtask_name] = {
                "subtask_steps": st.subtask_steps,
                "semantic_query": st.semantic_query
            }

    # 4) Build and run the parallel workflow
    graph = create_parallel_workflow(plan_dict)
    init_state: TaskState = {
        "input_prompt": prompt,
        "task_plan": {"plan": plan_dict},
        "partial_results": {},
        "merged_result": "",
        "merged_result_with_agent": "",
        "instructional_content": instructional_content,
        "has_rag": has_rag,
        "verification_report": {}
    }

    final_state = graph.invoke(init_state)
    return final_state 