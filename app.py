#Importing libraries
import streamlit as st
from st_pages import Page, show_pages, add_page_title
#Importing functions
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages
from PIL import Image

# Loading Image using PIL
icon = Image.open('./docs/static/drawmetrics_icon.jpg')
# Adding Image to web app
st.set_page_config(page_title="Drawmetrics Applicant Tracking System", page_icon = icon)


# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("pages/login.py", "Login", ":key:"),
        Page("pages/about.py","About",":book:"),
        Page("pages/home.py","Home",":house:"),
        Page("pages/charts.py", "Charts", ":chart_with_upwards_trend:"),
        Page("pages/chatbot.py", "Chatbot", ":robot_face:"),
        Page("pages/video.py", "Video", ":movie_camera:"),
        Page("pages/edit.py", "Edit", ":pencil2:")
        ]
)
hide_pages(["About", "Home", "Charts", "Chatbot", "Video"])


switch_page("Login")