from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0)

class Subtask(BaseModel):
    subtask_name: str = Field(description="Name of the subtask")
    recommendation: str = Field(description="Whether an LLM is recommended for this task")
    explanation: str = Field(description="Explanation for the recommendation or lack of recommendation")

# Set up a JSON parser for the Subtask schema
parser = JsonOutputParser(pydantic_object=Subtask)

# Prepare the prompt template
template = """
Answer the following query in JSON format:
{format_instructions}
{query}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def initialize_task_to_json(user_role, user_task):
    # Generate the task-specific prompt
    query = f"""
    You are an AI agent that has the role: {user_role}.
    You are given the task: {user_task}.
    Partition the task into subtasks each with the following format:
    - Subtask name
    - Recommendation (whether an LLM is recommended for this task)
    - Explanation (why you made or did not make a recommendation to use an LLM for this task)
    For the given role ({user_role}) and the given task ({user_task}), output a list of subtasks in JSON format.
    """
    # Run the chain and parse the response
    chain = prompt | model | parser
    response = chain.invoke({"query": query})
    return response

if __name__ == "__main__":
    # This should probably be moved somewhere else lol
    role = "Biomass Power Plant Manager"
    task = "Prepare and manage biomass plant budgets"
    json_result = initialize_task_to_json(role, task)
    print(json_result)  
