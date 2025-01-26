import os
from dotenv import load_dotenv
import getpass
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document, SystemMessage, HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, TypedDict
import asyncio
import json
from os.path import basename
from task_execution.logger import setup_logger

# Setup logging -> Yeah no we are redoing model.py logging -> putting it in its own log files
# logger = logging.getLogger("ModelLogger")
# logger.setLevel(logging.INFO)
# if not logger.handlers:
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)

logger = setup_logger("model_input_output")
def do_logging(func, prompt, output):
    logger.info("\n"*6)

    logger.info(func.__name__)
    logger.info("="*90)
    logger.info("PROMPT" + "="*84)
    logger.info("="*90)

    logger.info(prompt)
    
    logger.info("="*90)
    logger.info("OUTPUT" + "="*84)
    logger.info("="*90)

    logger.info(output)

    logger.info("\n"*6)
    

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

async def load_pages(loader):
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    logger.info(f"Loaded {len(pages)} pages from {loader.file_path}")
    return pages

# runs just the prompt without any additional file information
def run_gpt(system_prompt: str, user_prompt: str, model="gpt-4o-mini", temperature: float = 0.0) -> str:
    open_ai_key = os.environ["OPENAI_API_KEY"]
    llm = ChatOpenAI(model_name=model, temperature=temperature, openai_api_key=open_ai_key)
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)

    do_logging(run_gpt, messages, response)
    return response.content

# consumes the the files listed in its entirety and adds it to the prompt
def run_gpt_with_file(system_prompt: str, user_prompt: str, file_paths: List[str], model="gpt-4o-mini", temperature: float = 0.3) -> str:
    open_ai_key = os.environ["OPENAI_API_KEY"]
    llm = ChatOpenAI(model_name=model, temperature=temperature, openai_api_key=open_ai_key)

    file_contents = "Below are the FULL files for reference:\n"
    for i, fp in enumerate(file_paths, 1):
        file_name = basename(fp)
        loader = PyPDFLoader(fp)
        pages = asyncio.run(load_pages(loader))
        file_contents += f"\n--- File {i}: {file_name} (Pages: {len(pages)}) ---\n"
        for idx, page in enumerate(pages, 1):
            file_contents += f"Page {idx}:\n{page.page_content}\n"

    combined_prompt = user_prompt + "\n\n" + file_contents
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=combined_prompt)]
    response = llm.invoke(messages)
    
    do_logging(run_gpt_with_file, messages, response)
    return response.content

# puts the files through rag and adds the result of that to the prompt
def run_gpt_with_rag(system_prompt: str, user_prompt: str,
                     instructional_files: List[str], supplementary_files: List[str],
                     model="gpt-4o-mini", temperature: float = 0.3) -> str:
    open_ai_key = os.environ["OPENAI_API_KEY"]
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=open_ai_key)

    # Combine docs from both sets of files
    all_docs = []
    for fp in instructional_files + supplementary_files:
        loader = PyPDFLoader(fp)
        pages = asyncio.run(load_pages(loader))
        all_docs.extend(pages)
    logger.info(f"Total documents loaded for RAG: {len(all_docs)}")

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
    chunks = text_splitter.split_documents(all_docs)
    logger.info(f"Total chunks created: {len(chunks)}")

    # FAISS vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    logger.info("FAISS vector store created.")

    retrieved_docs = vector_store.similarity_search(user_prompt, k=3)
    doc_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    logger.info(f"Retrieved {len(retrieved_docs)} docs for the prompt.")

    llm = ChatOpenAI(model_name=model, temperature=temperature, openai_api_key=open_ai_key)
    combined_prompt = (
        f"QUESTION:\n{user_prompt}\n\n"
        f"RETRIEVED CONTENT:\n{doc_text}\n\n"
        "Answer strictly with relevant information from above, no extra. "
        "Ensure the final answer is coherent and as detailed as possible."
    )
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=combined_prompt)]
    response = llm.invoke(messages)

    do_logging(run_gpt_with_rag, messages, response)
    return response.content

if __name__ == '__main__':
    test_resp = run_gpt("System prompt here", "User says: Hello world!", "gpt-4o-mini")
    print("Test run_gpt:\n", test_resp)
