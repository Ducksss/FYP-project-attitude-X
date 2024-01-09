##Importing Libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import streamlit as st
import base64
from pathlib import Path
from PIL import Image

##Importing Funnctions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

#Hide Pages after login
hide_pages(["Login"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    switch_page('Login')

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid', width=32, height=32>".format(
      img_to_bytes(img_path)
    )
    return img_html

def on_click_callback():
    human_prompt=st.session_state.human_prompt
    st.session_state.history.append(human_prompt)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []

initialize_session_state()

st.title('chatbot')

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
credit_card_placeholder = st.empty()

with prompt_placeholder:
    st.markdown('**Chat** - _press enter to submit_')
    cols = st.columns((6,1))
    # cols[0].text_input(
    #     "Chat",
    #     value="Hello bot",
    #     label_visibility="collapsed",
    #     key="human_prompt"
    # )
    choice = cols[0].radio(
       "Please select 'yes' if you acknowledge",
       ["Yes :heavy_check_mark:", "No :heavy_multiplication_x:"],
       horizontal=True,
       key = "human_prompt"
    )
    cols[1].form_submit_button(
        "Submit",
        on_click=on_click_callback
    )

with chat_placeholder:
    for chat in st.session_state.history:
        image = img_to_html('docs/static/hr_icon.jpeg')
        div = f"""
        <div class="chat-row">
            {image}
            <div class="ai-bubble">&#8203;{chat}</div>
        </div>
        """
        st.markdown(div, unsafe_allow_html=True)

    if choice == 'Yes :heavy_check_mark:' :
        st.session_state.history.append('Yes')
    else:
        st.session_state.history.append('No')
