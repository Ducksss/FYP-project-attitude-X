##Importing Libraries
import os
import sys
import graphviz
import streamlit as st
from st_pages import hide_pages

##Importing Funnctions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor
from extra_streamlit_components import CookieManager

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

cookie_manager = CookieManager()

if 'email' not in st.session_state:
    cookie_manager.get(cookie='email')
else:
    cookie_manager.set('email',st.session_state.email)

email = cookie_manager.get(cookie='email')

#Hide Pages after login
if email == 'admin':
    hide_pages(["Login","Chatbot"])
else:
    hide_pages(["Login","Charts","Video","Home","Edit"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    cookie_manager.delete('email')
    switch_page('Login')

##Start of Page
st.write("# Welcome to Attitude-X!👋")

st.markdown(
    """
    Attitude-X, an AI solution, optimizes hiring processes by analyzing resumes. 
    It integrates cutting-edge NLP technologies and LLMs (Language Model Models) for this purpose.
    
    **Done by group 3A62 from Singapore Polytechnic DAAA FYP Year 2023**
    """
)

st.divider()  # 👈 Draws a horizontal rule
    
st.markdown(
    """
    ### Flowchart:
    """
)

# Create a graphlib graph object
graph = graphviz.Digraph()
graph.edge('Login', 'Job Candidate')
graph.edge('Login', 'HR Personnel')
graph.edge('Job Candidate', 'Interview Chatbot')
graph.edge('Interview Chatbot', 'Audio Recording (pyaudio)')
graph.edge('Interview Chatbot', 'Video Recording (cv2)')
graph.edge('Audio Recording (pyaudio)', 'Transcribing (whisper)')
graph.edge('HR Personnel', 'View Recording (FER Model)')
graph.edge('View Recording (FER Model)', 'Interview Summary (GPT-3.5-turbo-instruct)')
graph.edge('Interview Summary (GPT-3.5-turbo-instruct)', 'Prompt for Job Description (LLM model)')
graph.edge('HR Personnel', 'Edit Page')

st.graphviz_chart(graph)

st.divider()  # 👈 Draws a horizontal rule

st.markdown(
    """
    ### More about us:
    - Check out our [GitHub](https://github.com/27thRay/FYP-project-attitude-X)
    - Jump into our [Documentation](https://docs.streamlit.io)
    """
)    

st.divider()  # 👈 Draws a horizontal rule

st.markdown(
    """
    #### Contributors:
    - Raymond Loong Ng
    - Darryl Lim
    - Shaun Ho
    """
)