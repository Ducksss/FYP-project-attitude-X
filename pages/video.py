##Importing libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import pandas as pd
import tempfile
import streamlit_scrollable_textbox as stx
from extra_streamlit_components import CookieManager
import math
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2 
import av 
import io
import time
import ffmpeg
from pydub import AudioSegment
from pathlib import Path

# Importing functions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor
from utility.speech_tagger import transcribeFile
from utility.ner import transcription_prompt
from utility.cloud import uploadFile
from database import insert_interview, get_interview

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

AudioSegment.converter = "C:/Users/Shaun Ho/Documents/SP Year 2 Work/FYP/FYP-project-attitude-X/ffmpeg.exe"
AudioSegment.ffmpeg = "C:/Users/Shaun Ho/Documents/SP Year 2 Work/FYP/FYP-project-attitude-X/ffmpeg.exe"

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

cookie_manager = CookieManager()
email = cookie_manager.get(cookie='email')

#Hide Pages after login
if email == 'admin':
    hide_pages(["Login","Chatbot"])
else:
     hide_pages(["Login","Charts","Video","Home","Edit"])

st.title('Interview Analysis :movie_camera:')

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
    
# Change font size of questions
st.markdown('<style>label p{font-size:18px !important; font-weight:bold; color: rgb(150, 150, 150)}</style>',unsafe_allow_html=True)
    
# with st.form("Upload Form",clear_on_submit=True):
#     upload_files = st.file_uploader('Upload Video/Audio',type=['mp4'],label_visibility='hidden',accept_multiple_files=True)
#     #Check that process button was clicked
#     if st.form_submit_button("Process"):
#         if upload_files is not None:
#             transcript_dict = {}
#             summary_dict = {}
#             url_dict = {}
#             counter = 1
#             for file in upload_files:
#                 bytes_data = file.read()
#                 tfile = tempfile.NamedTemporaryFile(delete=False)
#                 tfile.write(bytes_data)
#                 transcript = transcribeFile(tfile.name)
#                 file_url = uploadFile(tfile.name)
#                 filename = tfile.name
#                 tfile.close()
#                 os.remove(filename)
#                 summary = transcription_prompt(transcript)
#                 transcript_dict[f'Question {counter}'] = transcript
#                 summary_dict[f'Question {counter}'] = summary
#                 url_dict[f'Question {counter}'] = file_url
#                 counter += 1
#             insert_interview(id_counter,'test',transcript_dict,summary_dict,url_dict)
            
# st.divider()
# if 'transcript' in st.session_state:
#     tab1, tab2, tab3 = st.tabs(['Video','Transcript','Summary of Transcript'])
#     with tab1:
#         if 'fileID' in st.session_state:
#             fileID = st.session_state.fileID
#         if st.text_input('Timestamp Input (seconds)',key='timestamp'):
#             if st.session_state.timestamp.isnumeric():
#                 timestamp = int(st.session_state.timestamp)
#                 # st.video(st.session_state.tempfile_name,start_time=timestamp)
#                 st.markdown(f'<iframe src="https://drive.google.com/file/d/{fileID}/preview?t={timestamp}s" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

#             else:
#                 st.toast(':red[Hey!] Ensure timestamp is numeric!', icon='👺')
#                 st.markdown(f'<iframe src="https://drive.google.com/file/d/{fileID}/preview?" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)
#         else:
#             st.markdown(f'<iframe src="https://drive.google.com/file/d/{fileID}/preview?" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

#     with tab2:
#         stx.scrollableTextbox(st.session_state.transcript,fontFamily="Source Sans Pro, sans-serif",height=150)
#         st.download_button('Download Transcript', st.session_state.transcript,file_name='transcript.txt')

#     with tab3:
#         lines = st.session_state.transcript.split("\n")
#         for i in range(math.ceil(len(lines)/100)):
#             newstring = "\n"
#             newstring = newstring.join(lines[100*i:100+i*100])
#             reply = transcription_prompt(newstring)
#             with st.expander(f"{i+1}"):
#                 st.text(reply)
if df.empty:
    st.error('Database for interviews is empty!')
else:
    if st.selectbox("Which applicant's interview would you like to view?",list(df['name']),key='applicant',index=None,placeholder="Select applicant..."):
        st.divider()
        if st.selectbox("Which question would you like to view?",list(df['transcript'].values[0].keys()),key='question',index=None,placeholder="Select question..."):
            st.divider()
            tab1, tab2, tab3, tab4 = st.tabs(['Video','Bounding Box Analysis','Transcript','Summary of Transcript'])
            if 'applicant' in st.session_state:
                applicant_df = df[df['name']== st.session_state.applicant]
                question = st.session_state.question
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
                    if st.button('Activate bounding box'):
                        if "load_video" not in st.session_state:
                            st.session_state.load_video = 0

                        print('1:',st.session_state.load_video)
                        RECORD_DIR = Path("./records")

                        if st.session_state.load_video == 0:
                            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                            emotion_dict = {0:'angry', 1 :'disgust', 2: 'fear', 3:'happy', 4: 'sad', 5:'surprise', 6:'neutral'}
                            classifier = load_model('improved_vgg_fer.h5')

                            input_file = cv2.VideoCapture("records/2024-01-24_18.11.04.982050_input.mp4") 
        
                            output_file = cv2.VideoWriter( 
                                "records/2024-01-24_18.11.04.982050_bounding_output2.mp4", cv2.VideoWriter_fourcc(*'MP4V'),  
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
                                            prediction = classifier.predict(roi)[0]
                                            maxindex = int(np.argmax(prediction))
                                            finalout = emotion_dict[maxindex]
                                            output = str(finalout)
                                        label_position = (x, y)
                                        cv2.putText(frame, output, label_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                                    # # adding filled rectangle on each frame 
                                    # cv2.rectangle(frame, (100, 150), (500, 600), 
                                    #               (0, 255, 0), -1) 

                                    # writing the new frame in output 
                                    output_file.write(frame) 
                                    #cv2.imshow("output", frame) 
                                    # if cv2.waitKey(1) & 0xFF == ord('s'): 
                                    #     break
                                
                                
                                

                                else: 
                                    st.session_state.load_video += 1 
                                    print('2:',st.session_state.load_video)
                                    input_file.release()
                                    output_file.release()
                                    cv2.destroyAllWindows()
                                    audio_file = AudioSegment.from_file("./records/2024-01-24_18.11.04.982050_input.mp4",'mp4')
                                    audio_file.export(RECORD_DIR/f'temp_audio.wav',format = 'wav')
                                    video_stream = ffmpeg.input(RECORD_DIR/f"2024-01-24_18.11.04.982050_bounding_output2.mp4")
                                    audio_stream = ffmpeg.input(RECORD_DIR/f'temp_audio.wav')
                                    # while (not os.path.exists(audio_file)):
                                    #     print("waiting for audio file to exit...")
                                    stream = ffmpeg.output(video_stream, audio_stream, filename="./records/tempMerge.mp4")

                                    try:
                                        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
                                    except ffmpeg.Error as e:
                                        print(e.stdout, file=sys.stderr)
                                        print(e.stderr, file=sys.stderr)

                                    st.rerun()
                                    # break

                        else:
                            print('3:',st.session_state.load_video)
                            #time.sleep(30)
                            uploadFile(f'{RECORD_DIR}/tempMerge.mp4',1)
                            st.video("records/2024-01-24_18.11.04.982050_bounding_output2.mp4")

                with tab3:
                    transcript = applicant_df['transcript'].values[0][question]
                    stx.scrollableTextbox(transcript,fontFamily="Source Sans Pro, sans-serif",height=150)
                    st.download_button('Download Transcript', transcript,file_name='transcript.txt',key=question)

                with tab4:
                    summary = applicant_df['summary'].values[0][question]
                    st.text(summary)
