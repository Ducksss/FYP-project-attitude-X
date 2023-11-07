##Importing Libraries
import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css('style.css')

# Loading config file
with open('docs/authentication/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'], 
        config['cookie']['key'], 
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

image = Image.open('docs/static/drawmetricslogo.jpg')

col1, col2, col3 = st.columns([1.3, 4, 1.3])
col2.image(image, use_column_width=True)

authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    switch_page("Home")
    authenticator.logout('Logout',"sidebar",key="unique_key")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')