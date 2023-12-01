##Importing libraries
import os
import sys
import pymongo
import streamlit as st
from st_pages import hide_pages
import pandas as pd

# Importing functions
from database import get_ovr_score_desc, insert_score, callback
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

#Hide pages after login
hide_pages(["Login"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    switch_page('Login')

##Start of Page
if len(get_ovr_score_desc(0.4,0.4,0.2)) > 0:
    if 'default_table' in st.session_state:
        df = st.session_state.default_table
else:
    df = get_ovr_score_desc(0.4,0.4,0.2)

# df = df.reset_index()
if len(df.index) == 0:
    counter = 1
else:
    counter = max(df["_id"]) + 1

st.title("Home Page :house:")

st.markdown(
    """
    ##### Description:
    Upload multiple files, consisting of one Job Description and several Resumes. 
    Evaluate each candidate against the Job Description using an AI-based algorithm 
    that matches and ranks candidates.
    """
)

st.markdown(
    """
    ##### Note:
    - **Rename Job Description file as "job_description.pdf"**
    - **Upload anything between 1-30 resumes**
    - **File < 200MB in size and in PDF Format**
    """
)

st.divider()  # 👈 Draws a horizontal rule

with st.form("Upload Form",clear_on_submit=True):
    upload_files = st.file_uploader('Upload Files',type=["pdf"], accept_multiple_files=True,label_visibility='hidden')

    #Check that process button was clicked
    if st.form_submit_button("Process"):    
        #Ensure at least 2 or more files are uploaded
        if len(upload_files)>1: 
            jd_dict = False
            resume_array = []
            #Loop through each file
            if 'job_description.pdf' not in (file.name.lower() for file in upload_files):
                st.toast(':red[Hey!] Please upload both job description and resume files!', icon='👺')
            else:
                for file in upload_files:
                    #Convert PDF to Text
                    text = dataprocessor.convertPDFToText(file)
                    
                    #Check for Job Description file
                    if file.name.lower() == 'job_description.pdf':
                        jd_dict = dataprocessor.process_text(text, 'JD')
                    else:
                        resume_dict = dataprocessor.process_text(text, 'Resume')
                        resume_array.append(resume_dict)
                
                if jd_dict and resume_array:
                    for resume_dict in resume_array:
                        techsk_score, softsk_score, lang_score = dataprocessor.get_score(jd_dict, resume_dict)
                        insert_score(counter, resume_dict, techsk_score, softsk_score, lang_score)
                        counter += 1
                        st.toast(f"Resume for {resume_dict['Name']} :green[successfully uploaded]!", icon='🎉')
                else:
                    st.toast(':red[Hey!] Please upload both job description and resume files!', icon='👺')
        else:
            st.toast(':red[Hey!] Please upload job description and resume files!', icon='👺')


tab1, tab2 = st.tabs(['Weightage','Filters'])
with tab1:
    st.markdown(
"""
#### Input Weightage of skills:
*(Please ensure weightages add up to 100)*
"""
    )
    tech_slider = st.slider('Input Technical Skills Weightage (%)', 0, 100, 40, 10)
    soft_slider = st.slider('Input Soft Skills Weightage (%)', 0, 100, 40, 10)
    lang_slider = st.slider('Input Languages Weightage (%)', 0, 100, 20, 10)

with tab2:
    st.markdown(
"""
#### Input Filter Parameters of table search:
"""
    )
    col1, col2 = st.columns(2)
    with col1:
        equalities = st.radio('Equalities',options=["Greater than Equal to", "Lesser than Equal to"],key='eq')
    with col2:
        variable = st.selectbox('Variable',options=['Overall Score','Technical Skills','Soft Skills','Language'],key='var')
    filter = st.slider('Filter',value=0, key='score')

if st.button("Calculate"):
    if tech_slider+soft_slider+lang_slider==100:
        st.session_state['data'] = get_ovr_score_desc(tech_slider/100,soft_slider/100,lang_slider/100)
        columns = st.session_state['data'].columns
        column_config = {column: st.column_config.Column(disabled=True) for column in columns}

        modified_df = st.session_state['data'].copy()
        modified_df["Delete"] = False

        # Make Delete be the first column
        modified_df = modified_df[["Delete"] + modified_df.columns[:-1].tolist()]
        if len(modified_df) > 0:
            modified_df = modified_df[["Delete","_id","name","overall_score","technical_skills","soft_skills","languages","email","contact_number"]]
        st.data_editor(
            modified_df,
            key="data_editor",
            hide_index=True,
            column_config=column_config,
        )

        # st.dataframe(get_ovr_score_desc(tech_slider/100,soft_slider/100,lang_slider/100),hide_index=True)
    else:
        st.toast(':red[Hey!] Ensure weightages add up to 100%!', icon='👺')
else:
    st.session_state['data'] = get_ovr_score_desc(0.4,0.4,0.2)
    columns = st.session_state['data'].columns
    column_config = {column: st.column_config.Column(disabled=True) for column in columns}

    modified_df = st.session_state['data'].copy()
    modified_df["Delete"] = False

    # Make Delete be the first column
    modified_df = modified_df[["Delete"] + modified_df.columns[:-1].tolist()]
    if len(modified_df) > 0:
        modified_df = modified_df[["Delete","_id","name","overall_score","technical_skills","soft_skills","languages","email","contact_number"]]

    st.data_editor(
        modified_df,
        key="data_editor",
        hide_index=True,
        column_config=column_config,
    )

st.button('Delete',on_click=callback,type='primary')