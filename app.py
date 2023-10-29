
from src.lang_call import text_selector, api_call
from src.extractors import youtubeExtractor, text_extractor, word_extractor, pdf_extractor
import streamlit as st
from PIL import Image
import os

# # from dotenv import load_dotenv
# # load_dotenv(".env")
# # OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = st.secrets["open-key"]
os.environ["OPENAI_API_KEY"] = st.secrets["open-key"]

path = 'data/'
if not os.path.exists(path):
    os.mkdir(path)
    
# Page title
st.set_page_config(page_title='Ask the Doc App', page_icon='🦜')
st.title(' Ask the Parrot App')

st.write("""*Enter the text you want to analyze*""")

def save_results(query_text, response):
    if 'query_text' not in st.session_state:
            st.session_state.query_text = [query_text]
            st.session_state.response = [response]
    else:  
        st.session_state.query_text.append(query_text)
        st.session_state.response.append(response)
        
def show_results():
    if 'response' not in st.session_state:
        with st.chat_message("assistant"):
            st.write(" Hello there, I'll be answering your questions down here!")
                
    else:
        for index, response in enumerate(st.session_state.response):
            with st.chat_message("user"):
                st.write(st.session_state.query_text[index])
            with st.chat_message("assistant"):
                st.write(response)

def youtube_form():
    with st.form("text-extract-youtube"):
                url = st.text_input(
                        "Enter link for youtube video here 👇",
                        disabled=False,
                        placeholder="https://www.youtube.com/watch?v=AiOUojVd6xQ",
                        key='firstQuery'
                )
                name = st.text_input(
                        "Enter a short name for text document to be extracted and saved",
                        disabled=False,
                        max_chars=14,
                        placeholder="Name for file",
                        key='text_extraction',
                )
                
                submit_button = st.form_submit_button("Submit URL")
                if submit_button:
                    with st.spinner('Extracting text from video...'):
                        try:
                            extraction = youtubeExtractor([url], name)
                            if extraction == 1:
                                st.warning(f" URL or name empty", icon="⚠️")
                                
                            if extraction == 2:
                                st.success(f" {name}.txt already saved on database", icon="✅")
                            
                            if extraction == 3:
                                st.success(f" {name}.txt saved on database", icon="✅")
                                
                        except:
                            st.warning('URL not valid')
                            
def text_form():
    with st.form("text-extract-text"):
        uploaded_file = st.file_uploader('Upload an article', type='txt')
        name = st.text_input(
                        "Enter a short name for text document to be extracted and saved",
                        disabled=False,
                        max_chars=14,
                        placeholder="Name for file",
                        key='text_extraction',
                )
        
        submit_button = st.form_submit_button("Submit File")
        if submit_button:
            with st.spinner('Extracting text from document...'):
                try:
                    response = text_extractor(uploaded_file, name)
                    if response == 2:
                        st.success(f" {name}.txt already saved on database", icon="✅")
                except:
                    st.warning('Document or name not valid')

def docx_form():
    with st.form("docx-extract-text"):
        uploaded_file = st.file_uploader('Upload an document', type='docx')
        name = st.text_input(
                        "Enter a short name for text document to be extracted and saved",
                        disabled=False,
                        max_chars=14,
                        placeholder="Name for file",
                        key='text_extraction',
                )
        submit_button = st.form_submit_button("Submit File")
        if submit_button:
            with st.spinner('Extracting text from document...'):
                try:
                    response = word_extractor(uploaded_file, name)
                    if response == 2:
                        st.success(f" {name}.txt already saved on database", icon="✅")
                except:
                    st.warning('Document or name not valid')
                    
def pdf_form():
    with st.form("pdf-extract-text"):
        uploaded_file = st.file_uploader('Upload an document', type='pdf')
        name = st.text_input(
                        "Enter a short name for text document to be extracted and saved",
                        disabled=False,
                        max_chars=14,
                        placeholder="Name for file",
                        key='text_extraction',
                )
        submit_button = st.form_submit_button("Submit File")
        if submit_button:
            with st.spinner('Extracting text from document...'):
                try:
                    response = pdf_extractor(uploaded_file, name)
                    if response == 2:
                        st.success(f" {name}.txt already saved on database", icon="✅")
                except:
                    st.warning('Document or name not valid')
    

with st.sidebar:
    image = Image.open('references/parrot_innovative2.png')

    st.image(image)
    choice = st.selectbox("Select input type:",
    ("Youtube", "Text Document", "Docx Document", "PDF Document"))
    
    if choice == 'Youtube':
        youtube_form()
        
    if choice == 'Text Document':
        text_form()
        
    if choice == 'Docx Document':
        docx_form()
        
    if choice == 'PDF Document':
        pdf_form()

list_of_files = os.listdir("data/")
if len(list_of_files) != 0:
    new_set = {x.removesuffix('.txt') for x in list_of_files}
    option = st.selectbox('Select document to use as base', (new_set))

    with st.spinner('Training on text...'):
        string_data = text_selector(option)
        st.text_area('Text Selected:', value=string_data)
        call = api_call(string_data)
        
    prompt = st.chat_input("Ask something")
    if prompt:
        with st.spinner('Analizing prompt...'):
            response = call.run(prompt)    #CALL
            save_results(prompt, response)
    st.markdown("""---""")        
    show_results()


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)