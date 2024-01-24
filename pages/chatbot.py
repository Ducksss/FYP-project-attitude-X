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
import json
from database import insert_interview, get_interview, get_personality, get_applicantPers, get_ovr_score_desc
from utility.speech_tagger import transcribeFile
from utility.ner import transcription_prompt
from utility.cloud import uploadFile

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
# print(cookie_manager.get("last_user"))
if 'last_user' in cookie_manager.get_all().keys():
    if cookie_manager.get('last_user') != email:
        st.session_state.clear()
        cookie_manager.set('last_user', email)

#Hide Pages after login
if email == 'admin':
    hide_pages(["Login","Chatbot"])
else:
     hide_pages(["Login","Charts","Video","Home","Edit"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    cookie_manager.delete('email')
    switch_page('Login')

df = get_interview()
if len(df.index) == 0:
    id_counter = 1
else:
    id_counter = max(df["_id"]) + 1

df2 = get_personality()
df3 = get_applicantPers()
df4 = get_ovr_score_desc(0.4,0.4,0.2)

applicantName = df4['name'][df4['email'] == email].values[0]
personality_type = df3['personality_type'][df3['applicant'] == applicantName].values[0]
personality_questions = df2['questions'][df2['personality_type'] == personality_type].values[0]

#chatbot script
ariel_script = [
    "Hello! I'm Ariel, a Virtual HR Interviewer with Drawmetrics.",
    "I'll be conducting an interview based on your Attitude Scores, recording your responses via your camera and microphone to simulate a real-life interview experience. The questions will be derived from your previous answers to our drawmetrics attitude test, aiming to assess your 'attitude' as a candidate.",
    "Please respond with 'yes' if you acknowledge",
    "Great! Let's move on. I'm about to present your initial question. Click the pop-up recording button to start recording when you're prepared. Once finished, click the button again to submit. Keep in mind, there won't be any retakes, mirroring the authenticity of a real-life interview.",
    "Sure, please click 'yes' when you are ready to move on.",    
    "This is the end of the interview thank you for your time. Please do not close or exit this page until the next message appears. Thank you for your cooperation.",
    "Thank you for your patience, you may now close this page. Goodbye.",
    "After you click the start button, you have about 30-60s of preperation time. Once the webcam is set up, you may test your microphone for the first 10 seconds and mute the audio at the bottom right of the camera should you want to turn off microphone feedback. I wish you the best for this interview, good luck!"
] 
ariel_script = ariel_script + personality_questions

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

def videoUpload(video_dict):
    transcript_dict = {}
    summary_dict = {}
    url_dict = {}
    for question, file in video_dict.items():
        transcript = transcribeFile(file)
        file_url = uploadFile(file)
        os.remove(file)
        summary = transcription_prompt(transcript)
        transcript_dict[question] = transcript
        summary_dict[question] = summary
        url_dict[question] = file_url
    st.session_state.history.append(ariel_script[6])
    st.session_state.end += 1
    return insert_interview(id_counter,applicantName,transcript_dict,summary_dict,url_dict), st.rerun()

def choice_change():
    if choice == 'Yes :heavy_check_mark:' :
        st.session_state.history.append('Yes')
        st.session_state.history.append(ariel_script[3])
        st.session_state.history.append(ariel_script[7])
        st.session_state.history.append(ariel_script[8])

        reaappear = 1

    elif choice == 'No :heavy_multiplication_x:':
        st.session_state.history.append('No')
        st.session_state.history.append(ariel_script[4])
        reaappear = 0
    
    return reaappear

st.title('HR Interview Chatbot :robot_face:')

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
        if 'server_auth.json' in os.listdir('./docs/'):
            with open('./docs/server_auth.json') as server_file:
                server = json.load(server_file)
                account_sid = server['account_sid']
                auth_token = server['auth_token']

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
            st.session_state.history.append(ariel_script[5])

        def questionthree():
            timenow3 = str(datetime.datetime.now())
            timenow3 = re.sub(' ','_',timenow3)
            timenow3 = re.sub(':','.',timenow3)
            if 'prefix3'  not in  st.session_state:
                st.session_state["prefix3"] = timenow3
            st.session_state.history.append(ariel_script[10])
        
        def questiontwo():
            timenow2 = str(datetime.datetime.now())
            timenow2 = re.sub(' ','_',timenow2)
            timenow2 = re.sub(':','.',timenow2)
            if 'prefix2'  not in  st.session_state:
                st.session_state["prefix2"] = timenow2
            st.session_state.history.append(ariel_script[9])

        def add_counter():
            if 'verify_count' not in st.session_state:
                st.session_state.verify_count = 0
            else:
                st.session_state.verify_count += 1

        if 'end' not in st.session_state:
            cookie_manager.set('last_user',email)
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
                    # st.session_state.verify_count += 1

        elif st.session_state.end == 1:
            vidDict = {}
            vidDict[ariel_script[8]] = RECORD_DIR / f"{st.session_state.prefix}_input.mp4"
            vidDict[ariel_script[9]] = RECORD_DIR / f"{st.session_state.prefix2}_input.mp4"
            vidDict[ariel_script[10]] = RECORD_DIR / f"{st.session_state.prefix3}_input.mp4"
            videoUpload(vidDict)
            
             