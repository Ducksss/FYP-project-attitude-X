##Importing Libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import streamlit as st
import base64
from pathlib import Path
from PIL import Image
from streamlit_modal import Modal

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

#chatbot script
ariel_script = [
    "Hi XX! I'm Ariel, a Virtual HR Interviewer with Drawmetrics.",
    "I'll be conducting an interview based on your Attitude Scores, recording your responses via your camera and microphone to simulate a real-life interview experience. The questions will be derived from your previous answers to our drawmetrics attitude test, aiming to assess your 'attitude' as a candidate.",
    "Please respond with 'yes' if you acknowledge",
    "Great! Let's move on. I'm about to present your initial question. Click the pop-up recording button to start recording when you're prepared. Once finished, click the button again to submit. Keep in mind, there won't be any retakes, mirroring the authenticity of a real-life interview. Best of luck!",
    "Sure, please click 'yes' when you are ready to move on."    
]

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid', width=32, height=32>".format(
      img_to_bytes(img_path)
    )
    return img_html

# def on_click_callback():
#     human_prompt=st.session_state.human_prompt
#     st.session_state.history.append(human_prompt)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = [ariel_script[0],ariel_script[1],ariel_script[2]]

def choice_change():
    if choice == 'Yes :heavy_check_mark:' :
        st.session_state.history.append('Yes')
        st.session_state.history.append(ariel_script[3])
        

    elif choice == 'No :heavy_multiplication_x:':
        st.session_state.history.append('No')
        st.session_state.history.append(ariel_script[4])

st.title('chatbot')

initialize_session_state()

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
credit_card_placeholder = st.empty()

with prompt_placeholder:
    st.markdown('**Chat** - _press enter to submit_')
    cols = st.columns((6,1))

    with cols[0]:
        choice = st.radio(
       "Please select 'yes' and 'no' accordingly",
       ["Yes :heavy_check_mark:", "No :heavy_multiplication_x:"],
       horizontal=True,
       key = "human_prompt"
    )
    with cols[1]:
        submit_button = st.form_submit_button()
        if submit_button:
            choice_change()

with chat_placeholder:
    for chat in st.session_state.history[:3]:
            image = img_to_html('docs/static/hr_icon.jpeg')
            div = f"""
            <div class="chat-row">
                {image}
                <div class="ai-bubble">&#8203;{chat}</div>
            </div>
            """
            st.markdown(div, unsafe_allow_html=True)
    # for chat in st.session_state.history[3:]:
    #     image = img_to_html('docs/static/user_icon.jpeg')
    #     div = f"""
    #     <div class="chat-row row-reverse">
    #         {image}
    #         <div class="human-bubble">&#8203;{chat}</div>
    #     </div>
    #     """
    #     st.markdown(div, unsafe_allow_html=True)
        
    for chat in st.session_state.history[3:]:
            userimage = img_to_html('docs/static/user_icon.jpeg')
            aiimage = img_to_html('docs/static/hr_icon.jpeg')
            div = f"""
            <div class= "chat-row
                {"" if chat in ariel_script
                    else "chat-row row-reverse"
            }">
                {aiimage if chat in ariel_script
                        else userimage}
                <div class={
                     "ai-bubble" if chat in ariel_script
                                    else "human-bubble"
                }>&#8203;{chat}</div>
            </div>
            """
            st.markdown(div, unsafe_allow_html=True)