from typing import Dict, TypedDict, Annotated, List, Any
from dotenv import load_dotenv
import os
import getpass
from pathlib import Path
import hashlib
import pickle

from pydantic import BaseModel
from openai import OpenAI

import pypdf
from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document

from langgraph.graph import Graph, StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from useless.agent_definitions import *

##### HELPER FUNCTIONS #####
def create_system_prompt(agent_definition):
    system_prompt = (
        f"You are: {agent_definition['name']}.\n"
        f"Your role: {agent_definition['role']}\n"
        f"Your function: {agent_definition['function']}\n"
    )
    return system_prompt

# Merge helpers
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

def get_cache_dir():
    """Get the cache directory, create if it doesn't exist."""
    cache_dir = Path(".cache/rag")
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def compute_files_hash(file_paths: List[str]) -> str:
    """Compute a hash of the files' contents and paths to use as cache key."""
    hasher = hashlib.sha256()
    for file_path in sorted(file_paths):  # Sort for consistency
        try:
            hasher.update(file_path.encode())
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
        except Exception as e:
            print(f"Warning: Error reading {file_path} for hash: {e}")
            # Include error in hash to avoid cache hits on failed reads
            hasher.update(str(e).encode())
    return hasher.hexdigest()

def save_rag_cache(file_paths: List[str], vector_store, doc_store):
    """Save RAG components to cache."""
    try:
        cache_dir = get_cache_dir()
        files_hash = compute_files_hash(file_paths)
        
        # Save FAISS vector store
        vector_store.save_local(str(cache_dir / f"{files_hash}_vectors"))
        
        # Save document store
        with open(cache_dir / f"{files_hash}_docstore.pkl", 'wb') as f:
            pickle.dump(doc_store, f)
            
        # Save file paths for validation
        with open(cache_dir / f"{files_hash}_files.txt", 'w') as f:
            f.write("\n".join(file_paths))
            
        # print("RAG cache saved successfully")
    except Exception as e:
        print(f"Error saving RAG cache: {e}")

def load_rag_cache(file_paths: List[str]) -> tuple:
    """Load RAG components from cache if available."""
    try:
        cache_dir = get_cache_dir()
        files_hash = compute_files_hash(file_paths)
        
        vector_path = cache_dir / f"{files_hash}_vectors"
        docstore_path = cache_dir / f"{files_hash}_docstore.pkl"
        files_path = cache_dir / f"{files_hash}_files.txt"
        
        # Check if cache exists
        if not (vector_path.exists() and docstore_path.exists() and files_path.exists()):
            return None, None
            
        # Validate file paths haven't changed
        with open(files_path, 'r') as f:
            cached_files = f.read().splitlines()
        if set(cached_files) != set(file_paths):
            return None, None
            
        # Load vector store
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        vector_store = FAISS.load_local(str(vector_path), embeddings)
        
        # Load document store
        with open(docstore_path, 'rb') as f:
            doc_store = pickle.load(f)
            
        # print("RAG cache loaded successfully")
        return vector_store, doc_store
    except Exception as e:
        print(f"Error loading RAG cache: {e}")
        return None, None

def setup_rag_for_supplementary_files(file_paths: List[str]):
    """Set up RAG system for supplementary files with caching."""
    # print("\n=== Setting up RAG system ===")
    
    # Try to load from cache first
    vector_store, doc_store = load_rag_cache(file_paths)
    
    if vector_store is not None and doc_store is not None:
        # Initialize retriever with cached components
        retriever = ParentDocumentRetriever(
            vectorstore=vector_store,
            docstore=doc_store,
            child_splitter=RecursiveCharacterTextSplitter(
                chunk_size=200,
                chunk_overlap=20,
                separators=["\n", ".", "!", "?", ";"],
            ),
            parent_splitter=RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ".", "!", "?", ";"],
            ),
            search_kwargs={"k": 3},
        )
        return retriever
    
    # If no cache, proceed with normal setup
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ";"],
    )
    
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        separators=["\n", ".", "!", "?", ";"],
    )
    
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector_store = FAISS.from_texts(["placeholder"], embeddings)
    doc_store = InMemoryStore()
    
    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        docstore=doc_store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
        search_kwargs={"k": 3},
    )
    
    # Load and add documents
    all_docs = []
    for file_path in file_paths:
        try:
            if file_path.lower().endswith('.pdf'):
                try:
                    loader = PDFPlumberLoader(file_path)
                    docs = loader.load()
                except Exception as e:
                    try:
                        loader = PyPDFLoader(file_path)
                        docs = loader.load()
                    except Exception as e2:
                        with open(file_path, 'rb') as file:
                            pdf_reader = pypdf.PdfReader(file)
                            text_content = []
                            for page in pdf_reader.pages:
                                text_content.append(page.extract_text())
                            docs = [Document(page_content="\n".join(text_content))]
            else:
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
            
            cleaned_docs = []
            for doc in docs:
                cleaned_text = " ".join(doc.page_content.split())
                if len(cleaned_text.strip()) > 0:
                    cleaned_docs.append(Document(page_content=cleaned_text))
            
            all_docs.extend(cleaned_docs)
            
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            continue
    
    if all_docs:
        retriever.add_documents(all_docs)
        # Save to cache after successful setup
        save_rag_cache(file_paths, vector_store, doc_store)
    
    return retriever

def get_relevant_context(query: str, k: int = 3) -> str:
    """Get relevant context from supplementary files using RAG."""
    global _global_retriever
    try:
        if not _global_retriever:
            # print("No RAG retriever available")
            return ""
            
        # print(f"\n=== Retrieving context for query: {query} ===")
        # Get relevant documents with stricter relevance
        relevant_docs = _global_retriever.get_relevant_documents(
            query,
            search_kwargs={"k": k, "score_threshold": 0.7}  # Only return highly relevant results
        )
        # Take top k most relevant results
        relevant_docs = relevant_docs[:k]
        
        # Format the context more cleanly
        contexts = []
        for i, doc in enumerate(relevant_docs, 1):
            # Clean up the text and format it
            clean_text = " ".join(doc.page_content.split())
            contexts.append(f"[{i}] {clean_text}")
        
        context = "\n\n".join(contexts)
        # print("\n=== Retrieved Context ===")
        print(context)
        # print("=== End Retrieved Context ===\n")
        return context
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return ""

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

class TaskPlan(TypedDict):
    plan: Dict[str, List[str]]

class SubtaskSteps(BaseModel):
    subtask_name: str
    subtask_steps: list[str]

class TaskExecutionPlan(BaseModel):
    task_execution_plan: list[SubtaskSteps]

class TaskState(TypedDict):
    """
    - task_plan: holds the dict of subtask => list of instructions
    - partial_results: dictionary of subtask => string output
    - input_prompt: overall prompt
    - merged_result: final merged essay
    - merged_result_with_agent: final merged essay from the agent
    - instructional_content: content from instructional PDF files
    - has_rag: boolean indicating if RAG is available
    """
    task_plan: TaskPlan
    partial_results: Annotated[Dict[str, str], dict_merge]
    input_prompt: str
    merged_result: str
    merged_result_with_agent: str
    instructional_content: str
    has_rag: bool

_global_retriever = None

def get_rag_retriever():
    """Get the global RAG retriever instance."""
    global _global_retriever
    return _global_retriever

def set_rag_retriever(retriever):
    """Set the global RAG retriever instance."""
    global _global_retriever
    _global_retriever = retriever

planner_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
executor_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
merger_llm   = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_task_execution_plan(
    user_prompt: str,
    instructional_content: str
) -> list:
    """
    Calls the Task Planner Agent with the user prompt
    and the *full instructional PDF content* in context.
    """
    client = OpenAI()
    
    system_prompt = create_system_prompt(agent_definitions["Task Planner Agent"])
    
    # Combine user prompt + instructions
    plan_user_msg = (
        f"Below is the overall user task and the instructional guidelines.\n\n"
        f"User Task:\n{user_prompt}\n\n"
        f"Instructional PDF Content:\n{instructional_content}\n"
        "Now create a detailed Task Execution Plan according to the specification."
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": plan_user_msg}
        ],
        response_format=TaskExecutionPlan
    )

    # Extract structured data
    task_execution_plan_raw = completion.choices[0].message.parsed
    task_execution_plan_raw = task_execution_plan_raw.model_dump()  # {'task_execution_plan': [...]}
    task_execution_plan = task_execution_plan_raw['task_execution_plan']
    return task_execution_plan


def task_planner(state: TaskState) -> TaskState:
    
    if not state["task_plan"]["plan"]:
        # If no plan is pre-populated, generate it
        plan_data_list = generate_task_execution_plan(
            state["input_prompt"],
            state["instructional_content"]
        )
        # Convert the structured list to dictionary
        plan_dict = {}
        for subtask in plan_data_list:
            plan_dict[subtask.subtask_name] = subtask.subtask_steps
        
        return {
            **state,
            "task_plan": {"plan": plan_dict}
        }
    else:
        return state
    
def router(state: TaskState) -> Dict:
    """
    Looks at the plan's keys and returns a list of executor node names
    to run in parallel. If no subtasks, jump to merger.
    """
    subtask_keys = list(state["task_plan"]["plan"].keys())
    if not subtask_keys:
        return {"next": ["merger_with_agent"]}

    next_nodes = [f"exec_{k}" for k in subtask_keys]
    return {"next": next_nodes}

def make_executor(subtask_name: str):
    """
    Creates a node function that uses the subtask instructions + overall prompt +
    the global instructional content. Also fetches relevant RAG context.
    """
    def executor_fn(state: TaskState) -> TaskState:
        instructions = state["task_plan"]["plan"][subtask_name]
        
        # ONLY the executor uses RAG to fetch relevant context
        rag_context = ""
        if state["has_rag"]:
            # Construct a retrieval query from the instructions
            rag_query = (
                f"Find relevant info about subtask: {subtask_name}\n"
                f"For the overall user task: {state['input_prompt']}\n"
                f"Instructions: {'. '.join(instructions)}"
            )
            rag_context = get_relevant_context(rag_query)

        # Build final prompt for the subtask
        full_prompt = f"""Subtask: {subtask_name}
Overall Task: {state['input_prompt']}

Instructions for this subtask:
{instructions}

Instructional Guidelines (always visible to you):
{state['instructional_content']}

Relevant Context from Supplementary Files (only for this subtask):
{rag_context}
"""
        # print(f"\n=== Executor {subtask_name} running ===")
        # print("Prompt:\n", full_prompt)

        system_text = create_system_prompt(agent_definitions['Task Executor Agent'])
        msgs = [
            AIMessage(role="system", content=system_text),
            HumanMessage(content=full_prompt)
        ]
        
        try:
            response = executor_llm(msgs)
            output_text = response.content.strip()
        except Exception as e:
            print(f"ERROR - Executor {subtask_name} error: {e}")
            output_text = f"Error occurred in {subtask_name}."

        # Write the executor output to partial_results
        return {
            "partial_results": {subtask_name: output_text}
        }
    return executor_fn

def merger_with_agent(state: TaskState) -> TaskState:
    """
    Merges partial_results into one coherent output, in subtask order.
    Then calls the Merger Agent for final formatting/organization.
    """
    plan_keys = list(state["task_plan"]["plan"].keys())

    # Gather partial results in plan order
    partials_text = []
    for k in plan_keys:
        sub_res = state["partial_results"].get(k, "")
        partials_text.append(f"--- {k} ---\n{sub_res}\n")

    combined_subtasks = "\n".join(partials_text)

    # Pass everything to the Merger Agent
    system_prompt = create_system_prompt(agent_definitions["Merger Agent"])
    user_prompt = (
        f"Original Task:\n{state['input_prompt']}\n\n"
        f"Here are the subtask outputs (in order):\n{combined_subtasks}\n\n"
        "Please merge these into a coherent final product."
        "\nYou also have access to the same instructional guidelines below:\n"
        f"{state['instructional_content']}"
    )

    messages = [
        AIMessage(role="system", content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        llm_response = merger_llm(messages)
        merged_text = llm_response.content.strip()
    except Exception as e:
        print(f"ERROR - Merger Agent error: {e}")
        merged_text = "Error occurred in merger agent."

    # print("\n=== MERGER WITH AGENT ===\nMerged output:\n", merged_text)
    return {
        **state,
        "merged_result_with_agent": merged_text,
        "merged_result": merged_text
    }

from langgraph.graph import Graph, StateGraph

def create_parallel_workflow(task_execution_plan) -> Graph:
    workflow = StateGraph(TaskState)

    # Add nodes
    workflow.add_node("planner", task_planner)
    workflow.add_node("router", router)
    workflow.add_node("merger_with_agent", merger_with_agent)

    # Create executor nodes for each subtask
    subtask_names = list(task_execution_plan.keys())
    exec_nodes = []
    for st in subtask_names:
        node_name = f"exec_{st}"
        workflow.add_node(node_name, make_executor(st))
        workflow.add_edge("router", node_name)
        exec_nodes.append(node_name)

    # Wire up edges
    workflow.add_edge("planner", "router")
    workflow.add_edge(exec_nodes, "merger_with_agent")
    workflow.add_edge("merger_with_agent", END)

    # Planner is the entry point
    workflow.set_entry_point("planner")
    return workflow.compile()

def process_task(
    prompt: str,
    instructional_pdf_path: str = None,
    supplementary_files: List[str] = None
) -> TaskState:
    """
    Orchestrates:
      1) Loading the instructional PDF (always accessible)
      2) Setting up RAG (only the Task Executors will use it for retrieval)
      3) Generating a plan
      4) Running the parallel execution + merging.
    """
    # 1) Load instructional PDF
    instructional_content = ""
    if instructional_pdf_path:
        instructional_content = load_instructional_files(instructional_pdf_path)
    
    # 2) Setup RAG for supplementary files
    has_rag = False
    if supplementary_files:
        retriever = setup_rag_for_supplementary_files(supplementary_files)
        if retriever:
            set_rag_retriever(retriever)
            has_rag = True
    
    # 3) Generate the plan and convert to expected format
    generated_plan = generate_task_execution_plan(prompt, instructional_content)
    # Reformat into a dict - handle both object and dict formats
    plan_dict = {}
    for st in generated_plan:
        if isinstance(st, dict):
            plan_dict[st['subtask_name']] = st['subtask_steps']
        else:
            plan_dict[st.subtask_name] = st.subtask_steps

    # 4) Build and run the parallel workflow
    graph = create_parallel_workflow(plan_dict)
    init_state: TaskState = {
        "input_prompt": prompt,
        "task_plan": {"plan": plan_dict},
        "partial_results": {},
        "merged_result": "",
        "merged_result_with_agent": "",
        "instructional_content": instructional_content,
        "has_rag": has_rag
    }

    final_state = graph.invoke(init_state)
    return final_state


if __name__ == "__main__":
    print("RAHHHHHHHHH")
