from typing import Dict, TypedDict, Annotated, List, Any
import json
from dotenv import load_dotenv
import os
import getpass

# Import your graph and LLM classes
from langgraph.graph import Graph, StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function

def dict_merge(old_dict: Dict[str, Any], new_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries by updating the old one with new values."""
    return {**old_dict, **new_dict}

def list_merge(old_list: List[Any], new_list: List[Any]) -> List[Any]:
    """Merge two lists by concatenation."""
    return old_list + new_list


load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

class SubTask(TypedDict):
    name: str
    instructions: List[str]

class TaskPlan(TypedDict):
    subtasks: Dict[str, SubTask]

class TaskState(TypedDict):
    task_plan: TaskPlan
    partial_results: Annotated[List[Dict[str, str]], list_merge]
    input_prompt: str
    merged_result: str


planner = ChatOpenAI(model="gpt-4o-mini", temperature=0)
executor = ChatOpenAI(model="gpt-4o-mini", temperature=0)
merger = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def task_planner(state: TaskState) -> TaskState:
    planning_prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """You are a task planning AI. Your job is to break down the given task into independent subtasks 
that can be executed in parallel. You MUST create multiple subtasks.

For an essay, you should create these subtasks:
1. Introduction – Set up the topic and outline main points
2. Body Paragraphs – Each major point gets its own section
3. Conclusion – Summarize and reinforce key points

Each subtask must have:
1. A descriptive name (e.g., "introduction", "body_1", etc.)
2. Clear instructions for what that section should cover

Format your response as a JSON object with a key "subtasks" whose value is an object mapping subtask keys to objects with "name" and "instructions"."""),
        ("human", "{input_prompt}")
    ])
    
    planning_function = {
        "name": "create_task_plan",
        "description": "Create a structured task plan with parallel subtasks",
        "parameters": {
            "type": "object",
            "properties": {
                "subtasks": {
                    "type": "object",
                    "patternProperties": {
                        ".*": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "instructions": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["name", "instructions"]
                        }
                    }
                }
            },
            "required": ["subtasks"]
        }
    }

    try:
        response = planner.invoke(
            planning_prompt.format_messages(input_prompt=state["input_prompt"]),
            functions=[planning_function],
            function_call={"name": "create_task_plan"}
        )
        plan_data = json.loads(response.additional_kwargs["function_call"]["arguments"])
        
        # Ensure the plan has all expected subtasks
        expected_subtasks = {"introduction", "body_1", "body_2", "conclusion"}
        plan_subtasks = plan_data.get("subtasks", {})
        if not plan_subtasks or not expected_subtasks.issubset(set(plan_subtasks.keys())):
            print("Plan missing expected subtasks. Using default plan.")
            plan_data = {
                "subtasks": {
                    "introduction": {
                        "name": "Introduction",
                        "instructions": [
                            "Write an engaging introduction to the topic.",
                            "Present the main points that will be discussed."
                        ]
                    },
                    "body_1": {
                        "name": "Body Paragraph 1",
                        "instructions": [
                            "Write the first body paragraph detailing a major aspect of the topic.",
                            "Include supporting evidence and examples."
                        ]
                    },
                    "body_2": {
                        "name": "Body Paragraph 2",
                        "instructions": [
                            "Write the second body paragraph detailing another major aspect of the topic.",
                            "Include supporting evidence and examples."
                        ]
                    },
                    "conclusion": {
                        "name": "Conclusion",
                        "instructions": [
                            "Write a conclusion summarizing the essay.",
                            "Reinforce the key points and provide final thoughts."
                        ]
                    }
                }
            }
        else:
            print("Debug - Task Plan:", plan_data)
            
        return {
            **state,
            "task_plan": plan_data
        }
    except Exception as e:
        print(f"Error in task planner: {e}")
        print("Response:", response)
        # Fallback default plan on error
        default_plan = {
            "subtasks": {
                "introduction": {
                    "name": "Introduction",
                    "instructions": [
                        "Write an engaging introduction to the topic.",
                        "Present the main points that will be discussed."
                    ]
                },
                "body_1": {
                    "name": "Body Paragraph 1",
                    "instructions": [
                        "Write the first body paragraph detailing a major aspect of the topic.",
                        "Include supporting evidence and examples."
                    ]
                },
                "body_2": {
                    "name": "Body Paragraph 2",
                    "instructions": [
                        "Write the second body paragraph detailing another major aspect of the topic.",
                        "Include supporting evidence and examples."
                    ]
                },
                "conclusion": {
                    "name": "Conclusion",
                    "instructions": [
                        "Write a conclusion summarizing the essay.",
                        "Reinforce the key points and provide final thoughts."
                    ]
                }
            }
        }
        return {
            **state,
            "task_plan": default_plan
        }

def create_subtask_executor(subtask_name: str):
    def executor_fn(state: TaskState) -> TaskState:
        try:
            subtask = state["task_plan"]["subtasks"][subtask_name]
        except KeyError:
            # In case the expected subtask is missing, skip execution.
            print(f"Subtask '{subtask_name}' not found in the plan. Skipping this executor.")
            return state

        execution_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             """You are a task execution AI. Execute the given subtask and provide a clear output.
You have the original task context and specific instructions for this subtask."""),
            ("human", 
             f"Execute this subtask: {subtask['name']}\n"
             f"Instructions: {subtask['instructions']}\n"
             f"Original context: {state['input_prompt']}")
        ])
        
        execution_function = {
            "name": "execute_subtask",
            "description": f"Execute the subtask: {subtask_name}",
            "parameters": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "string",
                        "description": "The result of executing the subtask"
                    }
                },
                "required": ["result"]
            }
        }

        try:
            response = executor.invoke(
                execution_prompt.format_messages(),
                functions=[execution_function],
                function_call={"name": "execute_subtask"}
            )
            result_data = json.loads(response.additional_kwargs["function_call"]["arguments"])
            # Each executor returns its result as a one-item list.
            return {"partial_results": [{subtask_name: result_data["result"]}]}
        except Exception as e:
            print(f"Error executing subtask {subtask_name}: {e}")
            return {"partial_results": [{subtask_name: "Error executing subtask"}]}
    
    return executor_fn

def result_merger(state: TaskState) -> TaskState:
    # Combine all partial results into one dictionary.
    if not state["partial_results"]:
        return {"merged_result": "No results to merge"}

    execution_results = {}
    for part in state["partial_results"]:
        execution_results.update(part)
        
    # Format the execution results for the prompt.
    results_str = "\n\n".join([f"{name}:\n{result}" for name, result in execution_results.items()])
    
    merger_prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """You are a result merging AI. Combine the results from multiple subtasks into a 
coherent final output. Ensure the merged result maintains proper flow and transitions between sections."""),
        ("human", 
         """Original task: {input_prompt}

Results to merge:
{execution_results}

Please merge these results into a coherent output.""")
    ])
    
    merger_function = {
        "name": "merge_results",
        "description": "Merge the results from all subtasks into a coherent output",
        "parameters": {
            "type": "object",
            "properties": {
                "merged_result": {
                    "type": "string",
                    "description": "The final merged output"
                }
            },
            "required": ["merged_result"]
        }
    }

    response = merger.invoke(
        merger_prompt.format_messages(
            input_prompt=state["input_prompt"],
            execution_results=results_str
        ),
        functions=[merger_function],
        function_call={"name": "merge_results"}
    )
    # Allow unescaped control characters (or adjust as needed)
    result_data = json.loads(response.additional_kwargs["function_call"]["arguments"], strict=False)
    return {"merged_result": result_data["merged_result"]}

def create_parallel_workflow() -> Graph:
    workflow = StateGraph(TaskState)
    
    # Add the planner node.
    workflow.add_node("planner", task_planner)
    
    # Add the merger node.
    workflow.add_node("merger", result_merger)
    
    # Pre-create executor nodes for all expected subtasks.
    expected_subtasks = ["introduction", "body_1", "body_2", "conclusion"]
    for name in expected_subtasks:
        node_name = f"executor_{name}"
        workflow.add_node(node_name, create_subtask_executor(name))
        # Each executor is triggered by the router.
        workflow.add_edge("router", node_name)
        # Each executor feeds its result into the merger.
        workflow.add_edge(node_name, "merger")
    
    # Define a router node that sends control to each executor based on the task plan.
    def router(state: TaskState) -> Dict:
        subtasks = state["task_plan"].get("subtasks", {})
        next_nodes = [f"executor_{name}" for name in subtasks.keys()]
        # If there are no subtasks, send control to the merger.
        if not next_nodes:
            return {"next": ["merger"]}
        return {"next": next_nodes}
    
    workflow.add_node("router", router)
    
    # Set up the main flow: planner -> router; (router -> executors) -> merger -> END.
    workflow.add_edge("planner", "router")
    workflow.add_edge("merger", END)
    
    workflow.set_entry_point("planner")
    return workflow.compile()

def process_task(prompt: str) -> Dict:
    """
    Process a task through the planning and execution workflow.
    
    Args:
        prompt (str): The input task prompt
        
    Returns:
        Dict: The final state containing the plan, execution results, and merged result
    """
    graph = create_parallel_workflow()
    
    initial_state = {
        "input_prompt": prompt,
        "task_plan": {"subtasks": {}},
        "partial_results": [],
        "merged_result": ""
    }
    
    try:
        result = graph.invoke(initial_state)
        print("Debug - Final State:", result)
        return result
    except Exception as e:
        print(f"Error in workflow execution: {e}")
        print("Current state:", initial_state)
        raise

if __name__ == "__main__":
    sample_prompt = "Write an essay about the benefits of artificial intelligence in healthcare."
    result = process_task(sample_prompt)
    
    print("\nTask Plan:")
    for name, subtask in result["task_plan"]["subtasks"].items():
        print(f"\n{name}:")
        print(f"Instructions: {subtask['instructions']}")
    
    # Merge executor outputs
    execution_results = {}
    for partial in result.get("partial_results", []):
        execution_results.update(partial)
    print("\nExecution Results:")
    for step, output in execution_results.items():
        print(f"\n{step}:")
        print(output)
    
    print("\nMerged Result:")
    print(result["merged_result"])
