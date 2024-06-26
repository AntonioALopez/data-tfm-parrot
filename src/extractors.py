from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from src.google_bucket import upload_blob
import os, shutil, docx, tika
from io import StringIO 
tika.initVM()
from tika import parser 
import streamlit as st

# from dotenv import load_dotenv
# load_dotenv(".env")
# OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["open-key"]

directory = "./data/"
save_dir="transcript"

def youtubeExtractor(url, name, user):
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
    clean_text = text_cleaning(string_data)
    save_txt(clean_text, name, user)
    return 3
        
def text_extractor(uploaded_file, name, user):
    '''Extracts text from text documents'''
    if checker(name) == 'exists':
        return 2
    
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    clean_text = text_cleaning(string_data)
    save_txt(clean_text, name, user)
    
    
def word_extractor(uploaded_file, name, user):
    '''Extracts text from docx documents'''
    if checker(name) == 'exists':
        return 2
    
    doc = docx.Document(uploaded_file)
    paragraphs = [p.text for p in doc.paragraphs]
    string_data = '\n'.join(paragraphs)
    clean_text = text_cleaning(string_data)
    save_txt(clean_text, name, user)


def pdf_extractor(uploaded_file, name, user):
    '''Extracts text from pdf documents'''
    if checker(name) == 'exists':
        return 2
    text = parser.from_file(uploaded_file)
    string_data = text['content']
    clean_text = text_cleaning(string_data)
    save_txt(clean_text, name, user)
        
        
def checker(name):
    '''Checks if .txt already exists'''
    path = f"{directory}{name.replace(' ','_')}.txt"
    if os.path.exists(path) and name != '':
        return 'exists'
    
def text_cleaning(text):
    separated_text = text.replace("", " - ").split("\n")

    new_one = ""
    for sentence in separated_text:
        if len(sentence) < 10:
            new_one = "".join((new_one, sentence))
            
        else:
            new_one = "\n".join((new_one, sentence))
            
    return new_one
    
def save_txt(string_data, name, user):
    '''Saves text into database'''
    local_path = f"{directory}{name.replace(' ','_')}.txt"
    gcs_path = f"{user}/{name.replace(' ','_')}.txt"
    
    with open(local_path, "w") as f:
        f.write(string_data)
    upload_blob(local_path, gcs_path)