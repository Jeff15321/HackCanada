import os
from dotenv import load_dotenv
import getpass
from openai import OpenAI
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
import warnings
from functools import lru_cache

# Suppress all UserWarnings (which includes LangSmith warnings)
warnings.filterwarnings("ignore", category=UserWarning)

# Setup logging
logger = setup_logger("model_input_output")

def do_logging(func, prompt, output):
    logger.info("\n" + "="*100)
    logger.info(f"FUNCTION CALL: {func.__name__}")
    logger.info("="*100)
    
    # Log system and user messages separately for better readability
    if isinstance(prompt, list):  # For message-style prompts
        logger.info("SYSTEM PROMPT:")
        logger.info("-"*50)
        logger.info(prompt[0].content)
        logger.info("\nUSER PROMPT:")
        logger.info("-"*50)
        logger.info(prompt[1].content)
    else:  # For direct string prompts
        logger.info("PROMPT:")
        logger.info("-"*50)
        logger.info(prompt)
    
    logger.info("\nOUTPUT:")
    logger.info("-"*50)
    if hasattr(output, 'content'):  # For OpenAI/LangChain style responses
        logger.info(output.content)
    else:  # For direct string outputs
        logger.info(output)
    
    logger.info("="*100 + "\n")

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# Cache the loaded pages to avoid reloading the same file multiple times
@lru_cache(maxsize=32)
async def load_cached_pages(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

# runs just the prompt without any additional file information
async def run_gpt(system_prompt: str, user_prompt: str, model="gpt-4o-mini", temperature: float = 0.0) -> str:
    open_ai_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=open_ai_key)
    
    response = await asyncio.to_thread(
        client.chat.completions.create,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    
    do_logging(run_gpt, [system_prompt, user_prompt], response)
    return response.choices[0].message.content

# consumes the the files listed in its entirety and adds it to the prompt
async def run_gpt_with_file(system_prompt: str, user_prompt: str, file_paths: List[str], model="gpt-4o-mini", temperature: float = 0.3) -> str:
    open_ai_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=open_ai_key)

    file_contents = "Below are the files for reference:\n"
    
    # Load all files in parallel
    async with asyncio.TaskGroup() as tg:
        file_tasks = [
            tg.create_task(load_cached_pages(fp))
            for fp in file_paths
        ]
    
    # Process results
    for i, task in enumerate(file_tasks):
        pages = await task
        file_name = basename(file_paths[i])
        file_contents += f"*****File {i+1}: {file_name} (total pages: {len(pages)})*****\n"
        for idx, page in enumerate(pages, 1):
            file_contents += f"**page {idx}**\n{page.page_content}"

    combined_prompt = user_prompt + "\n" + file_contents
    
    response = await asyncio.to_thread(
        client.chat.completions.create,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_prompt},
        ],
        temperature=temperature,
    )
    
    return response.choices[0].message.content

# puts the files through rag and adds the result of that to the prompt
async def run_gpt_with_rag(system_prompt: str, user_prompt: str,
                     instructional_files: List[str], supplementary_files: List[str],
                     model="gpt-4o-mini", temperature: float = 0.3) -> str:
    open_ai_key = os.environ["OPENAI_API_KEY"]
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=open_ai_key)

    # Combine docs from both sets of files
    all_docs = []
    for fp in instructional_files + supplementary_files:
        loader = PyPDFLoader(fp)
        pages = await load_cached_pages(fp)
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

    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}\n\nContext:\n{doc_text}"},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content

@lru_cache(maxsize=1000)
def cache_key(prompt: str, model: str) -> str:
    return hashlib.md5(f"{prompt}:{model}".encode()).hexdigest()

@lru_cache(maxsize=100)
async def cached_run_gpt(system_prompt: str, user_prompt: str, model="gpt-4o-mini", temperature: float = 0.0) -> str:
    key = cache_key(f"{system_prompt}:{user_prompt}", model)
    return await run_gpt(system_prompt, user_prompt, model, temperature)

class FileCache:
    def __init__(self):
        self.cache = {}
        self._lock = asyncio.Lock()

    async def get_file_content(self, file_path: str) -> List[Document]:
        if file_path not in self.cache:
            async with self._lock:
                if file_path not in self.cache:
                    loader = PyPDFLoader(file_path)
                    pages = await load_cached_pages(file_path)
                    self.cache[file_path] = pages
        return self.cache[file_path]

file_cache = FileCache()

class AgentResponseCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        self._lock = asyncio.Lock()

    async def get(self, key: str):
        return self.cache.get(key)

    async def set(self, key: str, value: str):
        async with self._lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest entry
                self.cache.pop(next(iter(self.cache)))
            self.cache[key] = value

response_cache = AgentResponseCache()

async def cached_run_gpt_with_rag(system_prompt: str, user_prompt: str,
                           instructional_files: List[str], supplementary_files: List[str],
                           model="gpt-4o-mini", temperature: float = 0.3) -> str:
    cache_key = hashlib.md5(f"{system_prompt}:{user_prompt}:{','.join(instructional_files + supplementary_files)}".encode()).hexdigest()
    
    # Check cache
    cached_response = await response_cache.get(cache_key)
    if cached_response:
        return cached_response

    # If not in cache, proceed with RAG
    response = await run_gpt_with_rag(system_prompt, user_prompt, instructional_files, supplementary_files, model, temperature)
    
    # Cache the response
    await response_cache.set(cache_key, response)
    return response

class PhiHandler:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5")
        self.pipe = pipeline("text-generation", model="microsoft/phi-1_5", device_map="auto")

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        prompt = f"System: {system_prompt}\nUser: {user_prompt}\nAssistant:"
        response = self.pipe(
            prompt,
            max_length=1000,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            num_return_sequences=1
        )
        return response[0]['generated_text'].split("Assistant:")[-1].strip()

try:
    phi_handler = PhiHandler()
except Exception as e:
    print(f"Warning: Could not initialize Phi-1.5 model: {str(e)}")
    print("Falling back to default model for delegator agents")
    phi_handler = None

async def run_phi(system_prompt: str, user_prompt: str) -> str:
    return await phi_handler.generate(system_prompt, user_prompt)

async def run_inference(system_prompt: str, user_prompt: str) -> str:
    """Dedicated function for delegator agents using Phi-1.5"""
    if phi_handler is not None:
        return await run_phi(system_prompt, user_prompt)
    else:
        # Fallback to GPT if Phi-1.5 is not available
        return await run_gpt(system_prompt, user_prompt, "gpt-4o-mini")

if __name__ == '__main__':
    test_resp = run_gpt("System prompt here", "User says: Hello world!", "gpt-4o-mini")
    print("Test run_gpt:\n", test_resp)
