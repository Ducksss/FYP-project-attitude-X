#Importing libraries
from PIL import Image
import streamlit as st
from st_pages import hide_pages

#Importing functions
from streamlit_extras.switch_page_button import switch_page
from utility.loadcss import local_css

local_css('style.css')

#Hide Pages before Login
hide_pages(["About", "Home", "Charts"])

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    #Set Logo
    image = Image.open('docs/static/drawmetricslogo.jpg')
    col1, col2, col3 = st.columns([1.3, 4, 1.3])
    col2.image(image, use_column_width=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    st.success("Login successful")
    switch_page('About')
elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass