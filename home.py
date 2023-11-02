import os
import sys
import streamlit as st

# Get the absolute path to 'Utility Folder'
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Import specific functions from the package
from functions import process_text, print_score
from convert_to_text import convertPDFToText, convertDocxToText

st.title("Home Page")

st.sidebar.success("Select a Page above")

st.markdown(
    """
    ### Description:
    Upload multiple files, consisting of one Job Description and several Resumes. 
    Evaluate each candidate against the job description using an AI-based algorithm 
    that matches and assesses candidates, assigning scores across various sectors,
    including Technical Skills, Soft Skills, and Language. 
    Candidates will be ranked based on these scores.
    
    #### Note:
    - **Rename Job Description file as jd.docx or jd.pdf**
    - **Upload anything between 1-30 resumes**
    - **Nothing above 200MB per file**
    - **Files must be in PDF or Docx format**
"""
)

upload_files = st.file_uploader("Upload Resumes and Job Descriptions in PDF/Word Format", type=["pdf", "docx"], accept_multiple_files=True)

try:
    #Check that process button was clicked
    if st.button("Process"):    
        #Ensure at least some files are uploaded
        if upload_files is not None:  
            #Loop through each file
            for file in upload_files:
                #Check file type pdf or docx and convert to text
                if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = convertDocxToText(file)
                elif file.type == "application/pdf":
                    text = convertPDFToText(file)
                
                #Check for Job Description file
                if file.name.lower() == "jd.docx" or file.name.lower() == 'jd.pdf':
                    jd_dict = process_text(text, 'JD')
                else:
                    resume_dict = process_text(text, 'Resume')
            
            #Not part of for loop
            if jd_dict and resume_dict:
                score = print_score(jd_dict, resume_dict)
                st.write(score)

except:
    st.write('Please follow instructions')