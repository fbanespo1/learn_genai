import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
import chromadb
from chromadb.config import Settings
import os

def fetch_wikipedia_content():
    url = "https://en.wikipedia.org/wiki/Generative_artificial_intelligence"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(id="mw-content-text").get_text()
    return content

@st.cache_resource
def load_vectorstore():
    persist_directory = os.path.join(os.getcwd(), "chroma_db")
    
    content = fetch_wikipedia_content()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(content)
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
    
    chroma_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=persist_directory
    ))
    
    vectorstore = Chroma.from_texts(
        texts, 
        embeddings, 
        client=chroma_client,
        collection_name="generative_ai_collection"
    )
    return vectorstore

def run_rag_chatbot():
    st.header("RAG Chatbot")

    vectorstore = load_vectorstore()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about Generative AI"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            chain = ConversationalRetrievalChain.from_llm(
                llm=Ollama(model="llama2:7b"),
                retriever=vectorstore.as_retriever(),
                memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            )
            response = chain({"question": prompt})
            st.markdown(response['answer'])
        st.session_state.messages.append({"role": "assistant", "content": response['answer']})

if __name__ == "__main__":
    run_rag_chatbot()