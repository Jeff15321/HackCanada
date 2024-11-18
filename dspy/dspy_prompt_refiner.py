"""
    This file is a baseline for a dspy implementation.
    TODO:
     - Enhance signature i.e. more descriptive fields for the input and output & additional fields which provide more context.
     - Create/use a better module i.e. replacing the ChainOfThought module with a custom one or expirementing with other modules.
     - Implementing an optimizer, use a DSPy optimizer to fine tune the generation through examples and metrics
     - Few-Shot learning? (maybe) Perhaps providing examples to guide DSPy.
     - Caching (also maybe) to improve efficiency

     When testing this file, please pipe the output into a .txt file in dspy-outputs
"""

import os
from dotenv import load_dotenv
import dspy

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found in .env file")

# Configure DSPy
lm = dspy.OpenAI(api_key=openai_api_key, model="gpt-4o-mini")
dspy.configure(lm=lm)

# Define the subtask (this can be changed or passed as an argument)
subtask = "Gather Historical Financial Data"

# Define a signature for the prompt refinement module (this can also be further refined)
class PromptRefiner(dspy.Signature):
    """Refine a prompt for a given subtask."""

    subtask = dspy.InputField(desc="The specific subtask for which a prompt needs to be refined")
    job_context = dspy.InputField(desc="The broader job context in which the subtask exists")
    refined_prompt = dspy.OutputField(desc="A refined, detailed prompt for the LLM based on the given subtask and job context")

# Using ChainOfThought module
refiner = dspy.ChainOfThought(PromptRefiner)

# Getting the refined prompt
def get_refined_prompt(subtask, job_context):
    result = refiner(subtask=subtask, job_context=job_context)
    return result.refined_prompt

if __name__ == "__main__":
    # Test cases
    test_cases = [
        ("Gather Historical Financial Data", "Investment Research"),
        ("Implement Machine Learning Model", "Predictive Analytics"),
        ("Conduct User Experience Survey", "Product Development"),
        ("Perform Environmental Impact Assessment", "Sustainability Planning")
    ]

    for subtask, job_context in test_cases:
        refined_prompt = get_refined_prompt(subtask, job_context)
        print(f"\nRefined prompt for '{subtask}' in the context of '{job_context}':")
        print(refined_prompt)
        print("-" * 80)