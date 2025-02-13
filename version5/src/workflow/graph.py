from langgraph.graph import Graph, StateGraph, END

from ..utils.types import TaskState
from ..agents.planner import task_planner
from ..agents.executor import make_executor
from ..agents.merger import merger_with_agent
from ..agents.verification import verification_agent

def router(state: TaskState) -> dict:
    """
    Routes to parallel executor nodes. All executors will run simultaneously.
    Returns a dict with 'next' key containing all executor nodes to run in parallel.
    """
    subtask_keys = list(state["task_plan"]["plan"].keys())
    if not subtask_keys:
        return {"next": ["merger_with_agent"]}
    
    # Return all executor nodes to be run in parallel
    next_nodes = [f"exec_{k}" for k in subtask_keys]
    return {"next": next_nodes}

def verification_router(state: TaskState) -> str:
    """Routes to END if verification passes or max retries reached."""
    retry_count = state.get("retry_count", 0)
    verification_report = state.get("verification_report", {})
    
    # End if max retries reached
    if retry_count >= 2:
        return "end"
        
    # Check verification results
    failed_metrics = []
    for metric in verification_report.get('metrics', []):
        if not metric.get('rating', False):
            failed_metrics.append(metric.get('metric', 'unknown metric'))
    
    # If everything passed, end
    if not failed_metrics:
        return "end"
        
    # Update state and retry
    state["retry_count"] = retry_count + 1
    state["input_prompt"] += f"\n\nPrevious attempt failed on: {', '.join(failed_metrics)}. Please address these issues specifically."
    return "planner"

def create_parallel_workflow(task_execution_plan) -> Graph:
    """Creates a workflow with parallel execution of subtasks."""
    workflow = StateGraph(TaskState)

    # Add core nodes
    workflow.add_node("planner", task_planner)
    workflow.add_node("router", router)
    workflow.add_node("merger_with_agent", merger_with_agent)
    workflow.add_node("verification", verification_agent)

    # Create executor nodes - these will run in parallel
    subtask_names = list(task_execution_plan.keys())
    exec_nodes = []
    for st in subtask_names:
        node_name = f"exec_{st}"
        workflow.add_node(node_name, make_executor(st))
        workflow.add_edge("router", node_name)  # Connect router to each executor
        exec_nodes.append(node_name)

    # Wire up the workflow
    workflow.add_edge("planner", "router")  # Planner -> Router
    workflow.add_edge(exec_nodes, "merger_with_agent")  # All executors -> Merger
    workflow.add_edge("merger_with_agent", "verification")  # Merger -> Verification
    workflow.add_conditional_edges(
        "verification",
        verification_router,
        {
            "planner": "planner",
            "end": END
        }
    )

    # Set entry point
    workflow.set_entry_point("planner")
    
    return workflow.compile() 