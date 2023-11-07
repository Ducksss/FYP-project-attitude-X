##Importing Libraries
import graphviz
import streamlit as st
# from Login import authenticator
from st_pages import hide_pages

##Importing Funnctions
from streamlit_extras.switch_page_button import switch_page
from app import local_css

local_css('style.css')

#Hide Pages after login
hide_pages(["Login"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    switch_page('Login')

st.sidebar.success("Select a Page above")

##Start of Page
st.write("# Welcome to Attitude-X! 👋")

st.markdown(
    """
    Attitude-X, an AI solution, optimizes hiring processes by analyzing resumes. 
    It integrates cutting-edge NLP technologies and LLMs (Language Model Models) for this purpose.
    
    **Done by group 3A62 from Singapore Polytechnic DAAA FYP Year 2023**
    
    ### More about us:
    - Check out our [GitHub](https://github.com/27thRay/FYP-project-attitude-X)
    - Jump into our [Documentation](https://docs.streamlit.io)
    
    #### Contributors:
    - Raymond Loong Ng
    - Darryl Lim
    - Shaun Ho
    
    ### Flowchart:
"""
)

# Create a graphlib graph object
graph = graphviz.Digraph()
graph.edge('Files', 'PDF')
graph.edge('Files', 'Docx')
graph.edge('PDF', 'pdfminer library')
graph.edge('Docx', 'doc2txt library')
graph.edge('pdfminer library', 'raw text')
graph.edge('doc2txt library', 'raw text')
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