from model import *
from prompt import *

user_role = "Biomass Power Plant Managers"
user_task = "Prepare and manage biomass plant budgets."

model = "gpt-4o-mini"

if __name__ == "__main__":

    initial_prompt = initialize_initial_task_prompt(user_role, user_task)
    print(initial_prompt)

    print("*"*50)
    print("*"*50)
    print("*"*50)

    resp = run_api(model, initial_prompt)
    print(resp)