from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
import os

directory = "./data/"
OPEN_AI_API_KEY = st.secrets["open-key"]
  
def text_selector(name):
    path = f"{directory}{name}.txt"
    with open(path, "r") as f:
        string_data = f.read()
    return string_data
        
def gpt_call(string_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    splits = text_splitter.split_text(string_data)
    vectordb = FAISS.from_texts(splits, OpenAIEmbeddings())
    
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
    )
    