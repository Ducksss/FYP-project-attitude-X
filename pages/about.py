##Importing Libraries
import os
import sys
import graphviz
import streamlit as st
from st_pages import hide_pages

##Importing Funnctions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

#Hide Pages after login
hide_pages(["Login"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
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

st.divider()  # 👈 Draws a horizontal rule
    
st.markdown(
    """
    ### Flowchart:
    """
)

# Create a graphlib graph object
graph = graphviz.Digraph()
graph.edge('Files', 'PDF')
graph.edge('PDF', 'pdfminer library')
graph.edge('pdfminer library', 'raw text')
graph.edge('raw text', 'stopwords removal (spaCy model)')
graph.edge('stopwords removal (spaCy model)', 'Job Description')
graph.edge('stopwords removal (spaCy model)', 'Resume')
graph.edge('Job Description', 'Prompt for Job Description (LLM model)')
graph.edge('Resume', 'Extract phone no. + email (regex library)')
graph.edge('Prompt for Job Description (LLM model)', 'Job Description Dictionary (regex library)')
graph.edge('Extract phone no. + email (regex library)', 'Prompt for Resume (LLM model)')
graph.edge('Prompt for Resume (LLM model)', 'Resume Dictionary (regex library)')
graph.edge('Resume Dictionary (regex library)', 'Similarity scoring (Bert model)')
graph.edge('Job Description Dictionary (regex library)', 'Similarity scoring (Bert model)')
graph.edge('Similarity scoring (Bert model)', 'Output.csv')

st.graphviz_chart(graph)