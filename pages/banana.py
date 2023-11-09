#Importing libraries
import os
import sys
import time
from PIL import Image
import streamlit as st
from st_pages import hide_pages

#Importing functions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

#Hide Pages before Login
hide_pages(["About", "Home", "Charts"])

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    #Set Logo
    image = Image.open('docs/static/draw.png')
    col1, col2, col3 = st.columns([2, 4, 2])
    col2.image(image, use_column_width='auto')

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    col4, col5, col6 = st.columns(3)
    with col5:
        submit = st.form_submit_button("Login",use_container_width=True)

if submit:
    if email == actual_email and password == actual_password:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.success("Login successful")
        time.sleep(0.5)
        switch_page('About')
    elif email != actual_email or password != actual_password:        
        st.toast(":red Login failed",icon='🚨')
    else:
        pass