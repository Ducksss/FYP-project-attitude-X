##Importing libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import pandas as pd
import streamlit_scrollable_textbox as stx
from extra_streamlit_components import CookieManager
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2 
import ffmpeg
from pydub import AudioSegment
from pathlib import Path
import requests
import json

# Importing functions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor
from utility.cloud import uploadFile, downloadFile
from database import get_interview, update_interview

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

AudioSegment.converter = "./ffmpeg.exe"
AudioSegment.ffmpeg = "./ffmpeg.exe"

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css(2)

cookie_manager = CookieManager()
email = cookie_manager.get(cookie='email')

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

#Start of Page
    
class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
# Change font size of questions
st.markdown('<style>label p{font-size:18px !important; font-weight:bold; color: rgb(150, 150, 150)}</style>',unsafe_allow_html=True)

if df.empty:
    st.error('Database for interviews is empty!')
else:
    col1, gap, col2 = st.columns([0.35, 0.15, 0.5])
    with col1:
        st.title('Interview Analysis :movie_camera:')
        applicant = st.selectbox("Which applicant's interview would you like to view?",list(df['name']),key='applicant',index=None,placeholder="Select applicant...")
        st.divider()
        applicant_df = df[df['name']== st.session_state.applicant]
        if applicant:
            question = st.selectbox("Which question would you like to view?",list(applicant_df['transcript'].values[0].keys()),key='question',index=None,placeholder="Select question...")
        else:
            st.selectbox("Which question would you like to view?",[],key='question',index=None,placeholder="Select question...",disabled=True )
        st.divider()
        
    with col2:
        tab1, tab2, tab3, tab4 = st.tabs(['Video','Bounding Box Analysis','Transcript','Summary of Transcript'])
        if applicant and question:
            with tab1:
                url = applicant_df['url_list'].values[0][question]
                if st.text_input('Timestamp Input (seconds)',key='timestamp'):
                    if st.session_state.timestamp.isnumeric():
                        timestamp = int(st.session_state.timestamp)
                        st.markdown(f'<iframe src="{url.split("?")[0]}?t={timestamp}s" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

                    else:
                        st.toast(':red[Hey!] Ensure timestamp is numeric!', icon='👺')
                        st.markdown(f'<iframe src="{url}" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

                else:
                    st.markdown(f'<iframe src="{url}" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

            with tab2:
                    url = applicant_df['url_list'].values[0][question]
                    entry_id = applicant_df['_id'].values[0]
                    if 'bounding_url_list' not in applicant_df or pd.isna(applicant_df['bounding_url_list'].values[0]) or question not in applicant_df['bounding_url_list'].values[0].keys():
                        if st.button('Activate bounding box'):
                            RECORD_DIR = Path("./records")
                            
                            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                            emotion_dict = {0:'angry', 1 :'disgust', 2: 'fear', 3:'happy', 4: 'sad', 5:'surprise', 6:'neutral'}
                            # classifier = load_model('improved_vgg_fer.h5')
                            video_name = downloadFile(url)
                            input_file = cv2.VideoCapture("./records/temp_video.mp4") 
                            output_file = cv2.VideoWriter(
                                "records/temp_video_bounding.mp4", cv2.VideoWriter_fourcc(*'MP4V'),
                                30, (640, 480)) 

                            while(True): 
                                ret, frame = input_file.read() 
                                if(ret): 

                                    #image = frame.to_ndarray(format="bgr24")
                                    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                                    # adding filled rectangle on each frame 
                                    faces = face_cascade.detectMultiScale(
                                        image=img_gray, scaleFactor=1.3, minNeighbors=5)
                                    for (x, y, w, h) in faces:
                                        cv2.rectangle(img=frame, pt1=(x, y), pt2=(
                                            x + w, y + h), color=(0, 255, 0), thickness=2)

                                        roi_gray = img_gray[y:y + h, x:x + w]
                                        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                                        if np.sum([roi_gray]) != 0:
                                            roi = roi_gray.astype('float') / 255.0
                                            roi = img_to_array(roi)
                                            roi = np.expand_dims(roi, axis=0)
                                            data = json.dumps({"instances":roi.tolist()})
                                            headers = {"content-type":"application/json"}
                                            prediction = requests.post("http://localhost:8080/v1/models/fer_model:predict",data=data,headers=headers)
                                            prediction = json.loads(prediction.text)['predictions']
                                            # prediction = classifier.predict(roi)[0]
                                            maxindex = int(np.argmax(prediction))
                                            finalout = emotion_dict[maxindex]
                                            output = str(finalout)
                                        label_position = (x, y)
                                        cv2.putText(frame, output, label_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                                    output_file.write(frame)

                                else:
                                    input_file.release()
                                    output_file.release()
                                    cv2.destroyAllWindows()
                                    audio_file = AudioSegment.from_file("./records/temp_video.mp4",'mp4')
                                    audio_file.export('./records/temp_audio.wav',format = 'wav')
                                    video_stream = ffmpeg.input("./records/temp_video_bounding.mp4")
                                    audio_stream = ffmpeg.input('./records/temp_audio.wav')
                                    stream = ffmpeg.output(video_stream, audio_stream, filename=f"./records/{video_name}.mp4")

                                    try:
                                        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
                                    except ffmpeg.Error as e:
                                        print(e.stdout, file=sys.stderr)
                                        print(e.stderr, file=sys.stderr)

                                    bounding_url = uploadFile(f'./records/{video_name}.mp4',1)

                                    if 'bounding_url_list' not in applicant_df or pd.isna(applicant_df['bounding_url_list'].values[0]):
                                        bounding_url_dict = {}
                                        bounding_url_dict[question] = bounding_url
                                        update_interview(int(entry_id),bounding_url_dict)

                                    else:
                                        bounding_url_dict = applicant_df['bounding_url_list'].values[0]
                                        bounding_url_dict[question] = bounding_url
                                        update_interview(int(entry_id),bounding_url_dict)

                                    os.remove(f'./records/{video_name}.mp4')
                                    os.remove(f'./records/temp_video.mp4')
                                    os.remove(f'./records/temp_video_bounding.mp4')
                                    os.remove(f'./records/temp_audio.wav')
                                    st.rerun()

                    else:
                        bound_url = applicant_df['bounding_url_list'].values[0][question]
                        if st.text_input('Timestamp Input (seconds)',key='bound_timestamp'):
                            if st.session_state.bound_timestamp.isnumeric():
                                timestamp = int(st.session_state.bound_timestamp)
                                st.markdown(f'<iframe src="{bound_url.split("?")[0]}?t={timestamp}s" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

                            else:
                                st.toast(':red[Hey!] Ensure timestamp is numeric!', icon='👺')
                                st.markdown(f'<iframe src="{bound_url}" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

                        else:
                            st.markdown(f'<iframe src="{bound_url}" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

                        # st.video()

            with tab3:
                transcript = applicant_df['transcript'].values[0][question]
                stx.scrollableTextbox(transcript,fontFamily="Source Sans Pro, sans-serif",height=250)
                st.download_button('Download Transcript', transcript,file_name='transcript.txt',key=question)

            with tab4:
                summary = applicant_df['summary'].values[0][question]
                st.text(summary)

        else:
            with tab1:
                st.error('Please select applicant and interview question!')
            with tab2:
                st.error('Please select applicant and interview question!')
            with tab3:
                st.error('Please select applicant and interview question!')
            with tab4:
                st.error('Please select applicant and interview question!')