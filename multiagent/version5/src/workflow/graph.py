from langgraph.graph import Graph, StateGraph, END

from ..utils.types import TaskState
from ..agents.planner import task_planner
from ..agents.executor import make_executor
from ..agents.merger import merger_with_agent
from ..agents.verification import verification_agent

def router(state: TaskState) -> dict:
    """
    Looks at the plan's keys and returns a list of executor node names
    to run in parallel. If no subtasks, jump to merger.
    """
    subtask_keys = list(state["task_plan"]["plan"].keys())
    if not subtask_keys:
        return {"next": ["merger_with_agent"]}

    next_nodes = [f"exec_{k}" for k in subtask_keys]
    return {"next": next_nodes}

def verification_router(state: TaskState) -> str:
    """
    Routes to planner if any verification metrics failed, otherwise to END.
    """
    verification_report = state["verification_report"]
    if not verification_report:
        return "planner"  # Route to planner if verification failed
        
    # Check all pass/fail judgments
    for metric in verification_report['metrics']: 
        if metric['rating'] is False:  # Verification failed
            return "planner"
        
    return "end"  # Verification successful

def create_parallel_workflow(task_execution_plan) -> Graph:
    workflow = StateGraph(TaskState)

    # Add nodes
    workflow.add_node("planner", task_planner)
    workflow.add_node("router", router)
    workflow.add_node("merger_with_agent", merger_with_agent)
    workflow.add_node("verification", verification_agent)

    # Create executor nodes for each subtask
    subtask_names = list(task_execution_plan.keys())
    exec_nodes = []
    for st in subtask_names:
        node_name = f"exec_{st}"
        workflow.add_node(node_name, make_executor(st))
        workflow.add_edge("router", node_name)
        exec_nodes.append(node_name)

    # Wire up edges
    workflow.add_edge("planner", "router")
    workflow.add_edge(exec_nodes, "merger_with_agent")
    workflow.add_edge("merger_with_agent", "verification")
    workflow.add_conditional_edges("verification", 
                                   verification_router, 
                                   {
                                       "planner": "planner", 
                                       "end": END
                                   })
    
    # TODO: Need to add input from the verification agent back to the planner (perhaps add False verification report feedback to the input_prompt?)

    # Planner is the entry point
    workflow.set_entry_point("planner")
    return workflow.compile() 