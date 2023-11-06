import os
import sys
import streamlit as st
from Login import authenticator
from streamlit_extras.switch_page_button import switch_page

import pymongo
from database import get_ovr_score_desc, insert_score

# Get the absolute path to 'Utility Folder'
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Import specific functions from the package
from utility.functions import process_text, get_score
from utility.convert_to_text import convertPDFToText, convertDocxToText

authenticator.logout('Logout','sidebar',key="unique_key")
if st.session_state["authentication_status"] is None:
    switch_page('Login')

st.title("Home Page")

st.sidebar.success("Select a Page above")

st.markdown(
    """
    ##### Description:
    Upload multiple files, consisting of one Job Description and several Resumes. 
    Evaluate each candidate against the Job Description using an AI-based algorithm 
    that matches and ranks candidates.
    
    ##### Note:
    - **Rename Job Description file as "job_description.docx" or ".pdf"**
    - **Upload anything between 1-30 resumes**
    - **File < 200MB in size and in PDF or Docx Format**
"""
)

upload_files = st.file_uploader("Upload Resumes and Job Descriptions in PDF/Word Format", type=["pdf", "docx"], accept_multiple_files=True)

#Check that process button was clicked
if st.button("Process"):    
    #Ensure at least 2 or more files are uploaded
    if len(upload_files)>1: 
        resume_array = []
        #Loop through each file
        for file in upload_files:
            #Check file type pdf or docx and convert to text
            if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = convertDocxToText(file)
            elif file.type == "application/pdf":
                text = convertPDFToText(file)
            
            #Check for Job Description file
            if file.name.lower() == "job_description.docx" or file.name.lower() == 'job_description.pdf':
                jd_dict = process_text(text, 'JD')
            else:
                resume_dict = process_text(text, 'Resume')
                resume_array.append(resume_dict)
        
        if jd_dict and resume_array:
            for resume_dict in resume_array:
                techsk_score, softsk_score, lang_score, overall_score = get_score(jd_dict, resume_dict)
                insert_score(resume_dict, techsk_score, softsk_score, lang_score, overall_score)
                st.toast(f"Resume for {resume_dict['Name']} :green[successfully uploaded]!", icon='🎉')
        else:
            st.toast(':red[Hey!] Please upload both job description and resume files!', icon='👺')
    else:
        st.toast(':red[Hey!] Please upload job description and resume files!', icon='👺')
                
st.table(get_ovr_score_desc())