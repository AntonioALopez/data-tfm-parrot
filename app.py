
from src.lang_call import text_selector, api_call
from src.extractors import youtubeExtractor, text_extractor, word_extractor, pdf_extractor
import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
from src.google_bucket import list_blobs
import os

import yaml
from yaml.loader import SafeLoader

# from dotenv import load_dotenv
# load_dotenv(".env")
# OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = st.secrets["open-key"]
os.environ["OPENAI_API_KEY"] = st.secrets["open-key"]

path = 'data/'
if not os.path.exists(path):
    os.mkdir(path)
    
# Page title
st.set_page_config(page_title='Ask the Doc App', page_icon='🦜')

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    
    st.title('Ask Parrot App')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.markdown("""---""") 
    
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
                                user = st.session_state["name"].replace(" ", "_")
                                extraction = youtubeExtractor([url], name, user)
                                if extraction == 1:
                                    st.warning(f" URL or name empty", icon="⚠️")
                                    
                                if extraction == 2:
                                    st.success(f" {name}.txt already saved on database", icon="✅")
                                
                                if extraction == 3:
                                    st.success(f" {name}.txt saved on database", icon="✅")
                                    
                            except:
                                st.warning('URL not valid')
    
    def form(typeDoc):
        with st.form(f"{typeDoc}-extract-text"):
            uploaded_file = st.file_uploader('Upload an article', type=typeDoc)
            name = st.text_input("Enter a short name for text document to be extracted and saved",
                            disabled=False,
                            max_chars=14,
                            placeholder="Name for file",
                            key='text_extraction')
            
            
            submit_button = st.form_submit_button("Submit File")
            if submit_button:
                with st.spinner('Extracting text from document...'):
                    try:
                        user = st.session_state["name"].replace(" ", "_")
                        if typeDoc == 'txt':
                            response = text_extractor(uploaded_file, name, user)
                        if typeDoc == 'docx':
                            response = word_extractor(uploaded_file, name, user)
                        if typeDoc == 'pdf':
                            response = pdf_extractor(uploaded_file, name, user)     
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
            form('txt')
            
        if choice == 'Docx Document':
            form('docx')
            
        if choice == 'PDF Document':
            form('pdf')
        authenticator.logout('Logout', 'sidebar', key='unique_key')

    list_of_blobs = list_blobs()
    user = st.session_state["name"].replace(" ", "_")
    
    matched_values = []
    for blob in list_of_blobs:
        parts = blob.split("/")
        if len(parts) > 0 and parts[0] == user:
            matched_values.append(parts[1])
            
    if len(list_of_blobs) != 0:
        new_set = {x.removesuffix('.txt') for x in matched_values}
        option = st.selectbox('Select document to use as base', (new_set))
        
        if 'option' not in st.session_state or st.session_state.option != option:
            print("CAMBIO DE OPCION")
            st.session_state.option = option
            with st.spinner('Training on text...'):
                if option != None:
                    print("Selecting Text")
                    string_data = text_selector(option, user)                    
                    st.session_state.text_train = [string_data]
                    print("NEW TEXT")
                    st.session_state.call = api_call(string_data)
                    print("TRAINED")
                        
                        
        if option == st.session_state.option:
            print("MISMA OPCION")
            with st.spinner('Training on text...'):
                print("Text Selected")
                st.text_area('Text Selected:', value=st.session_state.text_train[0], key="2")
                print("READY TO CALL")
        
        prompt = st.chat_input("Ask something")
        if prompt:
            with st.spinner('Analizing prompt...'):
                response = st.session_state.call.run(prompt) 
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
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')