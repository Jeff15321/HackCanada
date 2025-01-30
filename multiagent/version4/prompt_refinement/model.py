import os
from dotenv import load_dotenv
import getpass

from openai import OpenAI

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

from langchain_community.document_loaders import PyPDFLoader
import asyncio
import aiohttp

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# Loading pdf pages (for file upload and rag)
async def load_pages(loader):
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

# Define state for application (for rag)
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# normal calling gpt
def run_gpt(text_prompt, agent_role, model="gpt-4o-mini", temperature: float = 0):
    open_ai_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
      model = model,
      messages=[
        {"role": "developer", "content": agent_role},
        {"role": "user", "content": text_prompt},
      ],
      temperature=temperature,
    )
    resp = response.choices[0].message.content
    return resp

# calling chat gpt with an entire file (primary documents)
def run_gpt_with_file(text_prompt, agent_role, file_paths, model="gpt-4o-mini", temperature: float = 0):
    open_ai_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=open_ai_key)

    file_contents = "Below are the files for you to reference. Each file given to you will start with a line that has the file name and total number of pages in brackets on one line and encapsulated with ***** (five asterisk symbols) on the left and right of said line.\n"
    for i in range(0, len(file_paths)):
        file_path = file_paths[i]
        file_name = file_path.replace('\\', '/').split('/')[-1]
        loader = PyPDFLoader(file_path)
        pages = asyncio.run(load_pages(loader))

        file_contents += f"*****File {i+1}: {file_name} (total pages: {len(pages)})*****\n"
        for i in range(0, len(pages)):
            file_contents += f"**page {i+1}**\n{pages[i].page_content}"

    text_prompt += "\n" + file_contents
    
    response = client.chat.completions.create(
      model = model,
      messages=[
        {"role": "developer", "content": agent_role},
        {"role": "user", "content": text_prompt},
      ],
      temperature=temperature,
    )
    resp = response.choices[0].message.content
    return resp

# calling chat gpt but with rag (supplementary documents)
def run_gpt_with_rag(text_prompt, agent_role, file_path, model="gpt-4o-mini", temperature: float = 0):
    loader = PyPDFLoader(file_path)
    pages = asyncio.run(load_pages(loader)) # type(pages): , type(pages[0]): langchain_core.documents.base.Document
    vector_store = InMemoryVectorStore.from_documents(pages, OpenAIEmbeddings())
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = hub.pull("rlm/rag-prompt") # Note: this gives a rly sus prompt an ideally we could change this up (You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:")
    # Define application steps
    def retrieve(state: State):
        retrieved_docs = vector_store.similarity_search(state["question"], k=3)
        return {"context": retrieved_docs}
    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}

    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    response = graph.invoke({"question": text_prompt})
    return response["answer"]

class ConnectionPool:
    def __init__(self):
        self.session = None
        self._lock = asyncio.Lock()
        
    async def get_session(self):
        if not self.session:
            async with self._lock:
                if not self.session:
                    self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

pool = ConnectionPool()

if __name__ == '__main__':
    monke = run_gpt("What is the velocity of an unladden swallow?", "")
    print(monke)

    monke = run_gpt_with_rag("Who is the greatest ruler of all time?", "", "./documents/IA_ZhuDi.pdf")
    print(monke)

    monke = run_gpt_with_file("Write me a psych essay and based on the instructions in the guideline", "", ["./documents/PsychRubric.pdf"])
    print(monke)

