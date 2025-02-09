from typing import Dict, List
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from ..utils.types import TaskState, TaskExecutionPlan
from ..utils.helpers import create_system_prompt
from ..definitions.agent_definitions import agent_definitions

planner_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_task_execution_plan(
    user_prompt: str,
    instructional_content: str
) -> list:
    """
    Calls the Task Planner Agent with the user prompt
    and the *full instructional PDF content* in context.
    """
    client = OpenAI()
    
    system_prompt = create_system_prompt(agent_definitions["Task Planner Agent"])
    
    # Combine user prompt + instructions
    plan_user_msg = (
        f"Below is the overall user task and the instructional guidelines.\n\n"
        f"User Task:\n{user_prompt}\n\n"
        f"Instructional PDF Content:\n{instructional_content}\n"
        "Now create a detailed Task Execution Plan according to the specification."
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": plan_user_msg}
        ],
        response_format=TaskExecutionPlan
    )

    # Extract structured data
    task_execution_plan_raw = completion.choices[0].message.parsed
    task_execution_plan_raw = task_execution_plan_raw.model_dump()  # {'task_execution_plan': [...]}
    task_execution_plan = task_execution_plan_raw['task_execution_plan']
    return task_execution_plan

def task_planner(state: TaskState) -> TaskState:
    if not state["task_plan"]["plan"]:
        # If no plan is pre-populated, generate it
        plan_data_list = generate_task_execution_plan(
            state["input_prompt"],
            state["instructional_content"]
        )
        # Convert the structured list to dictionary
        plan_dict = {}
        for subtask in plan_data_list:
            plan_dict[subtask.subtask_name] = subtask.subtask_steps
        
        return {
            **state,
            "task_plan": {"plan": plan_dict}
        }
    else:
        return state 