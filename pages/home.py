##Importing libraries
import os
import sys
import pymongo
import numpy as np
import pandas as pd
import streamlit as st
from st_pages import hide_pages
import plotly.figure_factory as ff

# Importing functions
from utility.functions import process_text, get_score
from utility.convert_to_text import convertPDFToText, convertDocxToText
from database import get_ovr_score_desc, insert_score, search_score
from streamlit_extras.switch_page_button import switch_page
from utility.loadcss import local_css

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

local_css('style.css')
#Hide pages after login
hide_pages(["Login"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    switch_page('Login')

##Start of Page
st.title("Home Page :house:")

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
                
filter = st.slider('Filter',value=0,on_change=search_score, key='score')

col1, col2 = st.columns(2)
with col1:
    equalities = st.radio('Equalities',options=["Greater than Equal to", "Lesser than Equal to"],key='eq',on_change=search_score)
with col2:
    variable = st.selectbox('Variable',options=['Overall Score','Technical Skills','Soft Skills','Language'],key='var',on_change=search_score)

if filter != 0:
    st.dataframe(st.session_state.filter_table, hide_index=True)
else:
    st.dataframe(get_ovr_score_desc(),hide_index=True)

# #Bar Chart Ranking Plot
# columns=["Resume 1", "Resume 2"]
# barchart_data = get_ovr_score_desc()#This is dataframe
# print(barchart_data)

# st.bar_chart(barchart_data)

# ##Score Distribution Plot
# data = np.random.randn(200) - 2
# labels = ['Score Distribution']

# #Create distplot with custom bin_size
# fig = ff.create_distplot([data], labels, bin_size=[.1, .25, .5])

# #Plot
# st.plotly_chart(fig, use_container_width=True)