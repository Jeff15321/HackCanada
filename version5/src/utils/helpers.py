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

def extract_word_count_limit(instructional_content: str) -> int:
    """Extract word count limit from instructional content. Returns default if not found."""
    DEFAULT_WORD_LIMIT = 2500
    
    # Convert to lowercase for easier matching
    content = instructional_content.lower()
    
    # Look for common word count patterns
    import re
    patterns = [
        r'(\d+)(?=\s*(?:word|words))',  # "2000 words" or "2000 word"
        r'word count:?\s*(\d+)',         # "word count: 2000" or "wordcount 2000"
        r'word limit:?\s*(\d+)',         # "word limit: 2000"
        r'limit of (\d+) words',         # "limit of 2000 words"
        r'maximum of (\d+) words',       # "maximum of 2000 words"
        r'not exceed (\d+) words',       # "not exceed 2000 words"
        r'between \d+ and (\d+) words',  # "between 1800 and 2000 words" (takes upper limit)
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        if matches:
            # Take the first valid number found
            for match in matches:
                if isinstance(match, tuple):
                    # Some regex groups return tuples, take first non-empty value
                    match = next((m for m in match if m), None)
                if match and match.isdigit():
                    limit = int(match)
                    if 500 <= limit <= 10000:  # Sanity check for reasonable limits
                        return limit
    
    return DEFAULT_WORD_LIMIT

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