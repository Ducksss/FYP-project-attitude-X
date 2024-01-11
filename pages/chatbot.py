##Importing Libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import streamlit as st
import base64
from pathlib import Path
from PIL import Image
from audio_recorder_streamlit import audio_recorder
from st_audiorec import st_audiorec
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from utility.turn_server import get_ice_servers
from aiortc.contrib.media import MediaRecorder
import av
import cv2
import uuid
from twilio.rest import Client

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
        
        # with record_placeholder:
        #     audio_bytes = audio_recorder()
        #     if audio_bytes:
        #         record = st.audio(audio_bytes, format="audio/wav")
        #         record.export("/docs/record.wav",format = "wav")
                # with open('./', mode='bw') as f:
                #     f.write(audio_bytes)
                #     f.close()
        
        # with record_placeholder:
             
        #     wav_audio_data = st_audiorec()

        #     if wav_audio_data is not None:
        #         st.audio(wav_audio_data, format='audio/wav')

        account_sid = "ACbd4b35f39a2bf507fcc89a9f12d85056"
        auth_token = "626e9bf064c5bdc07f618a01f384e7f2"
        client = Client(account_sid, auth_token)

        token = client.tokens.create()

        RECORD_DIR = Path("./records")
        RECORD_DIR.mkdir(exist_ok=True)

        if "prefix" not in st.session_state:
            st.session_state["prefix"] = str(uuid.uuid4())
        prefix = st.session_state["prefix"]
        in_file = RECORD_DIR / f"{prefix}_input.flv"
        out_file = RECORD_DIR / f"{prefix}_output.flv"

        def in_recorder_factory() -> MediaRecorder:
            return MediaRecorder(
                str(in_file), format="flv"
            )  # HLS does not work. See https://github.com/aiortc/aiortc/issues/331

        def out_recorder_factory() -> MediaRecorder:
                return MediaRecorder(str(out_file), format="flv")
        
        def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            # perform edge detection
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            return av.VideoFrame.from_ndarray(img, format="bgr24")

        with record_placeholder:
            webrtc_streamer(
            key="record",
            mode=WebRtcMode.SENDRECV,
            # rtc_configuration={"iceServers": get_ice_servers()},
            # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            rtc_configuration={"iceServers":token.ice_servers},
            media_stream_constraints={
                "video": True,
                "audio": True,
            },
            video_frame_callback=video_frame_callback,
            in_recorder_factory=in_recorder_factory,
            out_recorder_factory=out_recorder_factory,
            )
            # webrtc_streamer(key='example')

            if in_file.exists():
                with in_file.open("rb") as f:
                    st.download_button(
                        "Download the recorded video without video filter", f, "input.flv"
                    )
            if out_file.exists():
                with out_file.open("rb") as f:
                    st.download_button(
                        "Download the recorded video with video filter", f, "output.flv"
                    )

        prompt_placeholder.empty()  

    elif choice == 'No :heavy_multiplication_x:':
        st.session_state.history.append('No')
        st.session_state.history.append(ariel_script[4])

st.title('chatbot')

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

# with record_placeholder:
#     webrtc_streamer(key='example')
record_placeholder = st.container()
account_sid = "ACbd4b35f39a2bf507fcc89a9f12d85056"
auth_token = "626e9bf064c5bdc07f618a01f384e7f2"
client = Client(account_sid, auth_token)

token = client.tokens.create()

RECORD_DIR = Path("./records")
RECORD_DIR.mkdir(exist_ok=True)

if "prefix" not in st.session_state:
    st.session_state["prefix"] = str(uuid.uuid4())
prefix = st.session_state["prefix"]
in_file = RECORD_DIR / f"{prefix}_input.flv"
out_file = RECORD_DIR / f"{prefix}_output.flv"

def in_recorder_factory() -> MediaRecorder:
            return MediaRecorder(
                str(in_file), format="flv"
            )  # HLS does not work. See https://github.com/aiortc/aiortc/issues/331

def out_recorder_factory() -> MediaRecorder:
                return MediaRecorder(str(out_file), format="flv")
        
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            # perform edge detection
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            return av.VideoFrame.from_ndarray(img, format="bgr24")

with record_placeholder:
            webrtc_streamer(
            key="record",
            mode=WebRtcMode.SENDRECV,
            # rtc_configuration={"iceServers": get_ice_servers()},
            # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            rtc_configuration={"iceServers":token.ice_servers},
            media_stream_constraints={
                "video": True,
                "audio": True,
            },
            video_frame_callback=video_frame_callback,
            in_recorder_factory=in_recorder_factory,
            out_recorder_factory=out_recorder_factory,
            )
            # webrtc_streamer(key='example')

if in_file.exists():
                with in_file.open("rb") as f:
                    st.download_button(
                        "Download the recorded video without video filter", f, "input.flv"
                    )
if out_file.exists():
                with out_file.open("rb") as f:
                    st.download_button(
                        "Download the recorded video with video filter", f, "output.flv"
                    )
