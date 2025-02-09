from typing import List
from pathlib import Path
import hashlib
import pickle

import pypdf
from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document

# Global variable to store the retriever
_global_retriever = None

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
            # print(f"Warning: Error reading {file_path} for hash: {e}")
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
        
        # Load document store with safety flag
        with open(docstore_path, 'rb') as f:
            doc_store = pickle.load(f, fix_imports=True, encoding='latin1', allow_dangerous_deserialization=True)
            
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
                chunk_size=1000,
                chunk_overlap=100,
                separators=["\n\n", "\n", ".", "!", "?", ";"],
            ),
            parent_splitter=RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", "!", "?", ";"],
            ),
            search_kwargs={"k": 3},
        )
        return retriever
    
    # If no cache, proceed with normal setup
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", ";"],
    )
    
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?", ";"],
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

def get_rag_retriever():
    """Get the global RAG retriever instance."""
    global _global_retriever
    return _global_retriever

def set_rag_retriever(retriever):
    """Set the global RAG retriever instance."""
    global _global_retriever
    _global_retriever = retriever

def get_relevant_context(query: str, k: int = 3) -> str:
    """Get relevant context from supplementary files using RAG."""
    global _global_retriever
    try:
        if not _global_retriever:
            return ""
            
        # Use invoke instead of get_relevant_documents
        relevant_docs = _global_retriever.invoke(
            query,
            config={"search_kwargs": {"k": k, "score_threshold": 0.7}}  # Only return highly relevant results
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
        return context
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return "" 