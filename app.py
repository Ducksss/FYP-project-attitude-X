#Importing libraries
import streamlit as st
from st_pages import Page, show_pages, add_page_title
from utility.loadcss import local_css
#Importing functions
from streamlit_extras.switch_page_button import switch_page

# Optional -- adds the title and icon to the current page
add_page_title()
local_css('style.css')

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("pages/Login.py", "Login", ":key:"),
        Page("pages/About.py","About",":book:"),
        Page("pages/Home.py","Home",":house:"),
        Page("pages/Charts.py", "Charts", ":chart_with_upwards_trend:")]
)

switch_page("Login")