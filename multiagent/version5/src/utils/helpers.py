from typing import Dict, Any
import pypdf
from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader

def create_system_prompt(agent_definition):
    system_prompt = (
        f"You are: {agent_definition['name']}.\n"
        f"Your role: {agent_definition['role']}\n"
        f"Your function: {agent_definition['function']}\n"
    )
    return system_prompt

def dict_merge(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """If multiple parallel updates to a dict come in, merge them."""
    return {**old, **new}

def load_instructional_files(pdf_path: str) -> str:
    """Load and read instructional PDF files that will be available to all agents."""
    try:
        try:
            # print(f"\n=== Loading instructional file: {pdf_path} ===")
            loader = PDFPlumberLoader(pdf_path)
            pages = loader.load()
        except Exception as e:
            print(f"PDFPlumber failed, trying PyPDFLoader: {e}")
            # Fallback to PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
        
        content = "\n".join(page.page_content for page in pages)
        # print("\n=== Instructional Content ===")
        # print(content)
        # print("=== End Instructional Content ===\n")
        return content
    except Exception as e:
        print(f"Error loading instructional file {pdf_path}: {e}")
        return "" 