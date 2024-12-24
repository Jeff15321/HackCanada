import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")

def run_gpt(text_prompt, agent_role, temperature: float = 0, model = "gpt-4o-mini"):
    open_ai_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
      model = model,
      messages=[
        {"role": "developer", "content": agent_role},
        {"role": "user", "content": text_prompt},
      ],
      temperature=temperature,
    )
    resp = response.choices[0].message.content
    return resp


if __name__ == '__main__':
    monke = run_gpt("What is the velocity of an unladden swallow?")
    print(monke)