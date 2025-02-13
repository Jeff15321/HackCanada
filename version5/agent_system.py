from agents import *

if __name__ == "__main__":
    # Paths to files
    instructional_pdf = "./documents/Critical Essay Rubric.pdf"  # PDF with general instructions for all agents
    supplementary_files = [
        "./documents/Ensmenger2018.pdf"
    ]

    # This is the user prompt
    prompt_text = "Write a critical essay on the article The Environmental History of Computing by Nathan Ensmenger."
    
    # Process task with both instructional and supplementary files
    final = process_task(
        prompt=prompt_text,
        instructional_pdf_path=instructional_pdf,
        supplementary_files=supplementary_files
    )

    # print("\n=== FINAL STATE ===")
    # print(json.dumps(final, indent=2))

    print("\n=== MERGED RESULT WITH AGENT ===")
    print(final["merged_result_with_agent"])

    # print("\n=== PARTIAL RESULTS ===")
    # for sub, text in final["partial_results"].items():
    #     print(f"Subtask {sub} =>", text)

    # print("\n=== MERGED RESULT ===")
    # print(final["merged_result"])
