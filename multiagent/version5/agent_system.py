from agents import *

if __name__ == "__main__":
    # This is the user prompt
    # prompt_text = "Write an essay about the benefits of artificial intelligence in healthcare."
    prompt_text = "Write an essay on seven different factors that caused the fall of the Ming Dynasty"
    final = process_task(prompt_text)

    print("\n=== FINAL STATE ===")
    print(json.dumps(final, indent=2))

    # print("\n=== PARTIAL RESULTS ===")
    # for sub, text in final["partial_results"].items():
    #     print(f"Subtask {sub} =>", text)

    # print("\n=== MERGED RESULT ===")
    # print(final["merged_result"])
