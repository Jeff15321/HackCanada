def initialize_initial_task_prompt(user_role, user_task):
    prompt = f"""
You are an AI agent that has the role: {user_role}.
You are given the task : {user_task}.
Partition the task into subtasks each with the following format:
- Subtask name
- Recommendation (whether an LLM is recommended for this task)
- Explanation (why you made or did not make a recommendation to use an LLM for this task)
For the given role ({user_role}) and the given task({user_task}) output a list of subtasks in the format specified above (Subtask name, recommendation, and explanation)
"""
    return prompt

# test = initialize_initial_task_prompt("monkey trainer", "breed monkeys")
# print(test)