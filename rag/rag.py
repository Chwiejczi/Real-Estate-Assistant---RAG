from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def retrieve_context(query):
    """Search the Warsaw district document for information relevant to the user's question."""
    similar_docs=vector_store.similarity_search(query,k=3)
    data=[]
    for doc in similar_docs:
        content = doc.page_content
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        data.append(
            f"Content:\n{content}\n"
            f"Source: {source}\n"
            f"Page: {page}"
        )
    return "\n\n".join(data)


if __name__=="__main__":
    load_dotenv("../agent/.env")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    model=ChatGroq(model='llama-3.3-70b-versatile')
    #loading pdf file
    loader=PyPDFLoader('../data/raw/panorama_dzielnic_warszawy.pdf')
    docs=loader.load()
    #text splitter
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200 )
    #overlap are to save the whole context of sentences in case that  chunks with sentences were split.
    all_splits=text_splitter.split_documents(docs)

    #print(all_splits)
   # agent=create_agent(model=model)
   # messages = [{"role": "user", "content": "jak sie masz"}]
    #res=agent.invoke({"messages": messages})
   # required_data = res
    #print(required_data["messages"][-1].content)

    #Embedding
    #Text->numbers->vectors
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    vector_store=InMemoryVectorStore.from_documents(all_splits,embeddings)
    print(vector_store)
    #res=vector_store.similarity_search("ile dzieci chodzi do szkół",k=3)
   # print(len(res))

   # for i, doc in enumerate(res):
   #     print(f"document {i+1}")
    #    print(doc.page_content)
   #     print(doc.metadata)

  #  print(retrieve_context.invoke({"query": "ile dzieci chodzi do szkół"}))
    prompt = """
    You are a RAG assistant.
    You must use the retrieve_context tool when the user asks about
    Warsaw districts, schools, population or statistics.
    Answer only on the basis of the information returned by the tool.
    If the document does not contain the answer, say that clearly.
    Answer in Polish.
    """

    agent=create_agent(model=model,tools=[retrieve_context],system_prompt=prompt)
    question="ile dzieci chodzi do warszawskich szkół?"
    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    print(result["messages"][-1].content)

