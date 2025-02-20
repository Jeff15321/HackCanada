from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
import shutil
from pathlib import Path
import traceback

# Add both version5 and version5/src to Python path
root_dir = Path(__file__).resolve().parents[5]
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / 'version5'))
sys.path.append(str(root_dir / 'version5' / 'src'))

print(f"Python path includes: {sys.path}")

from version5.run import process_task

router = APIRouter()

# Get absolute paths
BACKEND_DIR = Path(__file__).resolve().parents[3]  # backend/
DOCUMENTS_DIR = BACKEND_DIR / "documents"
RUBRIC_FILE = DOCUMENTS_DIR / "Critical Essay Rubric.pdf"
ENSMENGER_FILE = DOCUMENTS_DIR / "Ensmenger2018.pdf"

# Create documents directory if it doesn't exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Copy PDF files from version5/documents to backend/documents if they don't exist
VERSION5_DOCS = root_dir / "version5" / "documents"
if VERSION5_DOCS.exists():
    if not RUBRIC_FILE.exists() and (VERSION5_DOCS / "Critical Essay Rubric.pdf").exists():
        shutil.copy2(VERSION5_DOCS / "Critical Essay Rubric.pdf", RUBRIC_FILE)
    if not ENSMENGER_FILE.exists() and (VERSION5_DOCS / "Ensmenger2018.pdf").exists():
        shutil.copy2(VERSION5_DOCS / "Ensmenger2018.pdf", ENSMENGER_FILE)

@router.post("/process")
def chat_endpoint(message: Dict[str, Any]):
    """
    Chat endpoint that processes messages and returns responses
    """
    try:
        print(f"Received message: {message}")
        
        # Verify files exist
        if not RUBRIC_FILE.exists():
            raise HTTPException(
                status_code=500, 
                detail=f"Required file not found: {RUBRIC_FILE}"
            )
        if not ENSMENGER_FILE.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Required file not found: {ENSMENGER_FILE}"
            )

        # Use hardcoded prompt_text instead of message content
        prompt_text = """
        ### Role:
    - You are a **Grad student** specializing in **writing a critical essay on the environmental history of computing**.

    ### Task:
    1. Summarize the historical evolution of computing technologies and their societal implications based on the document.
    2. Analyze the environmental impact of computing technologies, focusing on energy consumption and resource exploitation.
    3. Extract and summarize case studies from the document, specifically the transatlantic communication infrastructure and Bitcoin.
    4. Research and compile insights from environmental history and technology studies relevant to the essay's themes.
    5. Identify and list academic sources that discuss the ecological consequences of computing and sustainability solutions.
    6. Critically evaluate the assumptions made in the document regarding computing technologies and their environmental impact.
    7. Propose sustainability solutions based on historical insights and current ecological challenges discussed in the document.
     Generated Knowledge Base:
    1. **Theoretical Foundations**
    - **Environmental History**: Examines the impact of human activities and technologies on the environment over time.
    - **Technological Determinism vs. Social Constructivism**: Analyzes the influence of technology on society and vice versa, particularly in computing.
    - **Sustainability and Ethics in Technology**: Investigates the ethical implications of technological advancements regarding resource consumption and environmental degradation.

    2. **Key Considerations for Task Execution Using LLM**
    - **Input Clarity**: Provide clear prompts specifying themes, length, and viewpoints.
    - **Iterative Feedback**: Use feedback to enhance the depth of LLM responses.
    - **Fact-Checking**: Cross-reference facts for accuracy, especially regarding historical events.
    - **Engagement with Source Material**: Encourage critical analysis of documents, summarizing key arguments and exploring counterarguments.
    - **Multi-Perspective Analysis**: Explore various viewpoints on computing's environmental implications.

    3. **Insights from the Provided Document**
    - **Historical Context**: Highlights the interaction between computing technologies and environmental factors.
    - **Infrastructure and Consumption**: Examines the ecological footprints of digital technology infrastructures.
    - **Growing Environmental Consciousness**: Emphasizes the need for historical perspectives on current sustainability challenges.
    - **Case Studies**: Provides concrete examples of technology-environment interplay (e.g., transatlantic communication, industrialization, Bitcoin).
    - **Interdisciplinary Approach**: Advocates for integrating environmental history with technological studies for better sustainability practices.

    4. **Potential Essay Structure**
    - **Introduction**: Introduce the topic and thesis statement.
    - **Historical Development**: Discuss key milestones in computing history and their environmental implications.
    - **Imposed Infrastructures**: Analyze the environmental costs of computing infrastructures.
    - **Contemporary Challenges**: Highlight current ecological concerns linked to computing technologies.
    - **Future Directions**: Propose how insights from environmental history can inform sustainable practices.
    - **Conclusion**: Summarize key arguments and the importance of interdisciplinary approaches.

    Extracted File Summary:
    content='### Summary of "The Environmental History of Computing"\n#### Author: Nathan Ensmenger\n\n**Publication Details:**\n- **Journal:** Technology and Culture\n- **Volume:** 59, Number 4 Supplement\n- **Date:** October 2018\n- **Pages:** 57-533\n- **Published by:** Johns Hopkins University Press\n- **DOI:** [Link](https://doi.org/10.1353/tech.2018.0148)\n\n**Abstract:**\nThis paper explores the environmental history of computing from the early mechanical devices to modern information technology. It investigates the environmental impacts of these technologies and recognizes the need to understand the relationship between computing power and resource management historically.\n\n**Key Themes:**\n1. **Historical Context**:\n   - Traces the evolution from early devices like Charles Babbage\'s Difference Engine and Hermann Hollerith\'s tabulating machine to contemporary technologies.\n   - Argues that early information technologies were deeply intertwined with human environments and societal needs.\n\n2. **Infrastructure and Consumption**:\n   - Examines the significant yet often invisible infrastructures supporting digital technologies.\n   - Discusses how internet activities influence energy consumption and resource management, presenting the digital realm as both extensive and exploitative.\n\n3. **Environmental Consciousness**:\n   - Highlights a growing awareness of the environmental impacts of computing technologies.\n   - Connects the historical development of computing to modern challenges in resource extraction and environmental sustainability.\n\n4. **Case Studies**:\n   - Uses examples like the transatlantic communication infrastructure, industrial impacts, and the emergence of platforms like Bitcoin to elucidate how technology interacts with environmental concerns.\n\n5. **Future Directions**:\n   - Suggests that understanding the history of technology is vital for addressing current ecological challenges.\n   - Encourages an interdisciplinary approach that merges environmental history with technological studies to better inform future practices.\n\nThis article contributes to a broader understanding of the implications of computing on environmental issues and advocates for more sustainable practices in technology development and usage.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 403, 'prompt_tokens': 4014, 'total_tokens': 4417, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_bd83329f63', 'finish_reason': 'stop', 'logprobs': None} id='run-0406b2b9-64fb-4213-b7ab-cb0766b9f095-0' usage_metadata={'input_tokens': 4014, 'output_tokens': 403, 'total_tokens': 4417, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

    Profession Context:
    Professionals in this field often utilize a variety of methodologies, including qualitative research, case studies, and historical analysis. They engage deeply with source materials, critically evaluating documents and synthesizing information from multiple perspectives. Tools such as academic databases, citation management software, and collaborative platforms are commonly used to facilitate research and writing. The emphasis on interdisciplinary approaches encourages grad students to draw connections between environmental history and technological studies, fostering a comprehensive understanding of sustainability challenges. This holistic perspective is crucial for developing informed arguments and proposing viable solutions to contemporary ecological issues.

    Task Context:
    In academia, particularly at the graduate level, writing a critical essay is a common task that requires a deep understanding of the subject matter. Graduate students typically start by reading the assigned document multiple times to grasp its nuances. They often take notes and highlight important sections to reference later. Best practices include creating a thesis statement that encapsulates their argument and organizing their essay into clear sections: introduction, body paragraphs, and conclusion. Collaboration is encouraged, as peer feedback can enhance the quality of the essay. Constraints may include deadlines, the need for original thought, and adherence to specific formatting guidelines. Additionally, students must ensure that they properly cite all sources to avoid plagiarism, which adds another layer of complexity to the task.

    Key Considerations:
    1. **Historical Context**: Understanding the evolution of computing technologies and their societal implications is vital. This includes examining early devices and their environmental interactions.
    2. **Environmental Impact**: Analyzing the ecological consequences of computing, including energy consumption and resource exploitation, is crucial for a critical perspective.
    3. **Case Studies**: Incorporating specific examples from the document, such as the transatlantic communication infrastructure and Bitcoin, will provide concrete evidence to support arguments.
    4. **Interdisciplinary Approach**: Merging insights from environmental history and technology studies will enhance the depth of analysis and argumentation.
    5. **Research Tools**: Utilizing academic databases and citation management software will aid in sourcing relevant literature and ensuring proper referencing.
    6. **Critical Evaluation**: Engaging with the source material critically, questioning assumptions, and synthesizing information from multiple perspectives will strengthen the essay.
    7. **Sustainability Solutions**: Proposing viable solutions based on historical insights will be essential for addressing contemporary ecological challenges.
        """

        # Process the chat message
        response = process_task(
            prompt=prompt_text,
            instructional_pdf_path=str(RUBRIC_FILE),
            supplementary_files=[str(ENSMENGER_FILE)]
        )
        
        print("Full response:", response)
        
        if response is None:
            raise HTTPException(status_code=500, detail="Process task returned None")
            
        if not isinstance(response, dict):
            raise HTTPException(status_code=500, detail=f"Expected dict response but got {type(response)}")
            
        if 'merged_result_with_agent' not in response:
            raise HTTPException(
                status_code=500, 
                detail=f"Response missing merged_result_with_agent. Keys: {response.keys() if isinstance(response, dict) else 'not a dict'}"
            )

        return response

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        print("Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
