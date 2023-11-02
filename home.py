import streamlit as st

st.set_page_config(
    page_title="About Page",
    page_icon="👋",
)

st.write("# Welcome to Attitude-X! 👋")

st.sidebar.success("Select a Page above")

import streamlit as st

uploaded_file = st.file_uploader("Upload Job Description")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()



uploaded_files = st.file_uploader("Upload Resumes in PDF/Word Format", accept_multiple_files=True)