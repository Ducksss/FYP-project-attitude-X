##Importing Libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import streamlit as st
import base64
from pathlib import Path
from PIL import Image
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from aiortc.contrib.media import MediaRecorder
from extra_streamlit_components import CookieManager
import av
import regex as re
from twilio.rest import Client
import datetime
import time
import threading 

##Importing Funnctions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

cookie_manager = CookieManager()
email = cookie_manager.get(cookie='email')

#Hide Pages after login
if email == 'admin':
    hide_pages(["Login","Chatbot"])
elif email == 'email' or 'yes':
     hide_pages(["Login","Charts","Video","Home"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    cookie_manager.delete('email')
    switch_page('Login')

#chatbot script
ariel_script = [
    "Hello! I'm Ariel, a Virtual HR Interviewer with Drawmetrics.",
    "I'll be conducting an interview based on your Attitude Scores, recording your responses via your camera and microphone to simulate a real-life interview experience. The questions will be derived from your previous answers to our drawmetrics attitude test, aiming to assess your 'attitude' as a candidate.",
    "Please respond with 'yes' if you acknowledge",
    "Great! Let's move on. I'm about to present your initial question. Click the pop-up recording button to start recording when you're prepared. Once finished, click the button again to submit. Keep in mind, there won't be any retakes, mirroring the authenticity of a real-life interview. Best of luck!",
    "Sure, please click 'yes' when you are ready to move on.",    
    "When was the last time you “broke the rules”?", #Personality A <Honesty & Integrity>
    "Describe a situation where you saw an employee or co-worker do something you thought was inappropriate.", #Personality A
    "Describe an instance when your curious nature significantly impacted a project outcome.", #Personality B <Curiosity>
    "Relate a time when being too curious led to an unexpected challenge or setback.", #Personality B
    "third question for personality a",
    "thrid question for personality b",
    "This is the end of the interview thank you for your time."
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

        if email == 'email':
             st.session_state.history.append(ariel_script[5])
        elif email == 'yes':
             st.session_state.history.append(ariel_script[7])

        reaappear = 1

    elif choice == 'No :heavy_multiplication_x:':
        st.session_state.history.append('No')
        st.session_state.history.append(ariel_script[4])
        reaappear = 0
    
    return reaappear

st.title('chatbot')
if 'last_user' in st.session_state:
    if st.session_state.last_user != email:
        st.session_state.clear()

initialize_session_state()

chat_placeholder = st.container()
# prompt_placeholder = st.form("chat-form")
prompt_placeholder = st.empty()
record_placeholder = st.empty()
# record_placeholder = st.container()

with prompt_placeholder.form("chat-form"):
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
            st.session_state.recorder = choice_change()

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

record_placeholder = st.container()

if 'recorder' in st.session_state:
    if st.session_state.recorder == 1 :
        prompt_placeholder.empty()
        account_sid = "ACbd4b35f39a2bf507fcc89a9f12d85056"
        auth_token = "04b7ce3b5ce46a854573c9607a743152"
        client = Client(account_sid, auth_token)

        token = client.tokens.create()

        RECORD_DIR = Path("./records")
        RECORD_DIR.mkdir(exist_ok=True)
        timenow = str(datetime.datetime.now())
        timenow = re.sub(' ','_',timenow)
        timenow = re.sub(':','.',timenow)

        if "prefix" not in st.session_state:
            st.session_state["prefix"] = timenow
        prefix = st.session_state["prefix"]
        if 'prefix2' in st.session_state:
            prefix = st.session_state["prefix2"]
        if 'prefix3' in st.session_state:
            prefix = st.session_state["prefix3"]
        in_file = RECORD_DIR / f"{prefix}_input.mp4"
        verify = in_file.exists()
        # print(verify)
             

        def in_recorder_factory() -> MediaRecorder:
                    return MediaRecorder(
                        str(in_file), format="mp4"
                    ) 
                
        def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
                    img = frame.to_ndarray(format="bgr24")

                    return av.VideoFrame.from_ndarray(img, format="bgr24")

        def questionend():
            global record_placeholder
            record_placeholder = st.empty()
            record_placeholder = st.container() 
            st.session_state.history.append(ariel_script[11])
            record_placeholder.empty()

        def questionthree():
            global record_placeholder
            record_placeholder = st.empty()
            record_placeholder = st.container() 
            timenow3 = str(datetime.datetime.now())
            timenow3 = re.sub(' ','_',timenow3)
            timenow3 = re.sub(':','.',timenow3)
            if 'prefix3'  not in  st.session_state:
                st.session_state["prefix3"] = timenow3
            if email == 'email':
                st.session_state.history.append(ariel_script[9])
            elif email == 'yes':
                st.session_state.history.append(ariel_script[10])

        
        def questiontwo():
            global record_placeholder
            record_placeholder = st.empty()
            record_placeholder = st.container() 
            timenow2 = str(datetime.datetime.now())
            timenow2 = re.sub(' ','_',timenow2)
            timenow2 = re.sub(':','.',timenow2)
            if 'prefix2'  not in  st.session_state:
                st.session_state["prefix2"] = timenow2
            if email == 'email':
                st.session_state.history.append(ariel_script[6])
            elif email == 'yes':
                st.session_state.history.append(ariel_script[8])

        def add_counter():
            if 'verify_count' not in st.session_state:
                st.session_state.verify_count = 0
            else:
                st.session_state.verify_count += 1
            print(st.session_state.verify_count)

        if 'end' not in st.session_state:
            with record_placeholder:
                ctx = webrtc_streamer(
                    key="record",
                    mode=WebRtcMode.SENDRECV,
                    rtc_configuration={"iceServers":token.ice_servers},
                    media_stream_constraints={
                        "video": True,
                        "audio": True,
                    },
                    video_frame_callback=video_frame_callback,
                    in_recorder_factory=in_recorder_factory,
                    on_change=add_counter
            )
        
            # if ctx.state.playing == False and ctx.state.signalling == False:
            #     if 'verify_count' not in st.session_state:
            #         counter = 0
            #     else:
            #         counter = int(st.session_state.verify_count)
            #     counter += 1
            #     st.session_state.verify_count = counter
            if 'verify_count' in st.session_state:
                if st.session_state.verify_count == 1:
                        st.session_state.history.append("Recording#1 Sent")
                        questiontwo()

                if st.session_state.verify_count == 4:
                        st.session_state.history.append("Recording#2 Sent")
                        questionthree()

                if st.session_state.verify_count == 7:
                        st.session_state.history.append("Recording#3 Sent")
                        questionend()
                        st.session_state.end = 1
                        st.session_state.last_user = email
                        #print(2, st.session_state.last_user, email)