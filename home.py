import streamlit as st
import base64

st.set_page_config(
    page_title="About Page",
    page_icon="👋",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css('style.css')

st.write("# Welcome to Attitude-X! 👋")

import streamlit as st
import pymongo
from database import get_ovr_score_desc

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

uploaded_files = st.file_uploader("Upload Resumes in PDF/Word Format", accept_multiple_files=True)

st.dataframe(get_ovr_score_desc())
