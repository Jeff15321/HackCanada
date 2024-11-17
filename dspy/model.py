from dotenv import load_dotenv
import os
import traceback
from openai import OpenAI
import anthropic

load_dotenv()

# model prompt -> plan
# str str -> str
def run_api(model, prompt, max_tokens_to_sample: int = 100000, temperature: float = 0):
    if model.startswith('claude') or model.startswith('Claude'):
        print("Use Claude-2 to generate action plan...")
        plan = run_claude(prompt, max_tokens_to_sample=max_tokens_to_sample, temperature=temperature)
    elif (model.startswith('gpt') or model.startswith('GPT')) and '4o' in model and 'mini' not in model:
        print("Use GPT-4o to generate action plan...")
        plan = run_gpt(prompt, temperature=temperature, model="gpt-4o")
    elif (model.startswith('gpt') or model.startswith('GPT')) and '4o' in model and 'mini' in model:
        print("Use GPT-4o-mini to generate action plan...")
        plan = run_gpt(prompt, temperature=temperature, model="gpt-4o-mini-2024-07-18")
    else:
        raise ValueError("Invalid model name")
    return plan

def run_claude(text_prompt, max_tokens_to_sample: int = 100000, temperature: float = 0):
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not claude_api_key:
        raise KeyError("CLAUDE_API_KEY is not set. Ensure it's defined in your .env file.")
    
    client = anthropic.Anthropic(api_key=claude_api_key)
    prompt = f"{anthropic.HUMAN_PROMPT} {text_prompt}{anthropic.AI_PROMPT}"
    resp = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-2",
        max_tokens_to_sample=max_tokens_to_sample,
        temperature=temperature,
    ).completion
    return resp

def run_gpt(text_prompt, temperature: float = 0, model="gpt-4-1106-preview"):
    open_ai_key = os.getenv("OPENAI_API_KEY")
    if not open_ai_key:
        raise KeyError("OPENAI_API_KEY is not set. Ensure it's defined in your .env file.")

    print(f"open_ai_key = {open_ai_key}")  # Debugging to check if the key is loaded
    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text_prompt},
        ],
        temperature=temperature,
    )
    resp = response.choices[0].message.content

    return resp
