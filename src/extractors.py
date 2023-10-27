from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
import os, shutil, docx
from io import StringIO
import tika
tika.initVM()
from tika import parser 
import streamlit as st

# from dotenv import load_dotenv
# load_dotenv(".env")
# OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_API_KEY = st.secrets["open-key"]

directory = "./data/"
save_dir="transcript"

def youtubeExtractor(url, name):
    '''Extracts text from Youtube URL'''
    if name == '' or url[0] == '':
        return 1

    if checker(name) == 'exists':
        return 2

    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    os.mkdir(save_dir)
    loader = GenericLoader(
        YoutubeAudioLoader(url,save_dir),
        OpenAIWhisperParser()
    )
    docs = loader.load()

    combined_docs = [doc.page_content for doc in docs]
    string_data = " ".join(combined_docs)

    save_txt(string_data, name)
    return 3
        
def text_extractor(uploaded_file, name):
    '''Extracts text from text documents'''
    if checker(name) == 'exists':
        return 2
    
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    save_txt(string_data, name)
    
    
def word_extractor(uploaded_file, name):
    '''Extracts text from docx documents'''
    if checker(name) == 'exists':
        return 2
    
    doc = docx.Document(uploaded_file)
    paragraphs = [p.text for p in doc.paragraphs]
    string_data = '\n'.join(paragraphs)
    save_txt(string_data, name)


def pdf_extractor(uploaded_file, name):
    '''Extracts text from pdf documents'''
    if checker(name) == 'exists':
        return 2
    st.write("new doc")
    text = parser.from_file(uploaded_file)
    st.write(text)
    string_data = text['content']
    st.write(string_data = text['content'])
    save_txt(string_data, name)
        
        
def checker(name):
    '''Checks if .txt already exists'''
    path = f"{directory}{name.replace(' ','_')}.txt"
    if os.path.exists(path) and name != '':
        return 'exists'
    
    
def save_txt(string_data, name):
    '''Saves text into database'''
    path = f"{directory}{name.replace(' ','_')}.txt"    
    with open(path, "w") as f:
        f.write(string_data)
        