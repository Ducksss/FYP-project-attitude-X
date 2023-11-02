import streamlit as st
from convert_to_text import convertPDFToText, convertDocxToText
from functions import process_text, print_score

st.title("Attitude-X Home Page")

st.sidebar.success("Select a Page above")

jd_file = st.file_uploader("Upload Job Description in PDF/Word Format", type=["pdf", "docx"])
if st.button("Submit"):    
    if jd_file is not None:  
        if jd_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            jd_text = convertDocxToText(jd_file)
        elif jd_file.type == "application/pdf":
            jd_text = convertPDFToText(jd_file)
            
        jd_dict = process_text(jd_text, 'JD')
        st.write(jd_dict)

docx_file = st.file_uploader("Upload Resumes in PDF/Word Format", type=["pdf", "docx"], accept_multiple_files=True)
if st.button("Process"):    
    if docx_file is not None:  
        for file in docx_file:
            if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = convertDocxToText(file)
            elif file.type == "application/pdf":
                resume_text = convertPDFToText(file)
                
            resume_dict = process_text(resume_text, 'Resume')
            try:
                score = print_score(jd_dict, resume_dict)
                st.write(score)
            except NameError as e:
                st.write('Please upload Job Description for Scoring')
                break
