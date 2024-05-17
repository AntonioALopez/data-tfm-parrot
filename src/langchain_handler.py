from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.google_bucket import download_blob
import streamlit as st
import os

directory = "./data/"

# from dotenv import load_dotenv
# load_dotenv(".env")
# OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["open-key"]

os.environ["OPENAI_API_KEY"] = st.secrets["open-key"]

def text_selector(name, user):
    '''Select which file to use from cloud storage'''
    path = f"{directory}{name}.txt"
    download_blob(f"{user}/{name}.txt", path)
    
    with open(path, "r") as f:
        string_data = f.read()
    print(f"Text {path} found")
    return string_data


def api_request(string_data):
    '''API Request'''
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    splits = text_splitter.split_text(string_data)
    vectordb = FAISS.from_texts(splits, OpenAIEmbeddings())
    
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )
    