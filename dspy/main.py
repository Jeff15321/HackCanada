from model import *

model = "gpt-4o-mini"
prompt = "what is the velocity of an unladden swallow"

if __name__ == "__main__":
    resp = run_api(model, prompt)
    print(resp)