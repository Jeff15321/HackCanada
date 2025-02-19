# test_rag.py

from model import run_gpt_with_rag

if __name__ == "__main__":
    system_prompt = "You are a helpful assistant that retrieves relevant information based on the user's query."
    user_prompt = "What is the main point of this article?"
    instructional_files = ["./documents/Critical Essay 3.pdf"]
    supplementary_files = ["./documents/Critical Essay Rubric.pdf"]

    rag_output = run_gpt_with_rag(system_prompt, user_prompt, instructional_files, supplementary_files)
    print("RAG Output:\n", rag_output)
