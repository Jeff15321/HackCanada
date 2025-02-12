from typing import Dict, List
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import ValidationError

from ..utils.types import TaskState, VerificationFeedback
from ..utils.helpers import create_system_prompt
from ..definitions.agent_definitions import agent_definitions

verification_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_verification_output(
    user_prompt: str,
    instructional_content: str, 
    merged_output: str
) -> list:
    """
    Calls the Verification Agent, instructional PDF content and the output in context. 
    """
    client = OpenAI()
    
    system_prompt = create_system_prompt(agent_definitions["Verification Agent"])
    
    # Combine user prompt + instructions
    plan_user_msg = (
        f"Below is the original user task, the instructional PDF content, and the task output.\n\n"
        f"User Task:\n{user_prompt}\n\n"
        f"Instructional PDF Content:\n{instructional_content}\n"
        f"Task output:\n{merged_output}"
        "Now critique the output according to the original prompt and instructional content."
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": plan_user_msg}
        ],
        response_format=VerificationFeedback
    )

    # Extract structured data
    try: 
        verification_output_raw = completion.choices[0].message.parsed
        verification_output_dict = verification_output_raw.model_dump()  
    except ValidationError as e: 
        print(f"Validation error: {e}")
        
    return verification_output_dict

def verification_agent(state: TaskState) -> TaskState:
    """
    Updates state by updating verification output. 
    """
    
    verification_report = generate_verification_output(
        state["input_prompt"], 
        state["instructional_content"],
        state["merged_result"]
    )
    
    return {
        **state,
        "verification_report": verification_report
    }
