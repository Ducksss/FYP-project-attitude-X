##Importing libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import pandas as pd
import tempfile
import streamlit_scrollable_textbox as stx
import math

# Importing functions
from streamlit_extras.switch_page_button import switch_page
from extra_streamlit_components import CookieManager
from utility.classes import dataProcessor
from utility.speech_tagger import transcribeFile
from utility.ner import transcription_prompt
from utility.cloud import uploadFile
from database import insert_interview, get_interview

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

df = get_interview()
# df = df.reset_index()
if len(df.index) == 0:
    id_counter = 1
else:
    id_counter = max(df["_id"]) + 1

#Start of Page
    
with st.form("Upload Form",clear_on_submit=True):
    upload_files = st.file_uploader('Upload Video/Audio',type=['mp4'],label_visibility='hidden',accept_multiple_files=True)
    #Check that process button was clicked
    if st.form_submit_button("Process"):
        if upload_files is not None:
            transcript_dict = {}
            summary_dict = {}
            url_dict = {}
            counter = 1
            for file in upload_files:
                bytes_data = file.read()
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(bytes_data)
                transcript = transcribeFile(tfile.name)
                file_url = uploadFile(tfile.name)
                filename = tfile.name
                tfile.close()
                os.remove(filename)
                summary = transcription_prompt(transcript)
                transcript_dict[f'Question {counter}'] = transcript
                summary_dict[f'Question {counter}'] = summary
                url_dict[f'Question {counter}'] = file_url
                counter += 1
            insert_interview(id_counter,'test4',transcript_dict,summary_dict,url_dict)
            
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

if st.selectbox("Which applicant's interview would you like to view?",list(df['name']),key='applicant',index=None,placeholder="Select applicant..."):
    tab1, tab2, tab3 = st.tabs(['Video','Transcript','Summary of Transcript'])
    if 'applicant' in st.session_state:
        applicant_df = df[df['name']== st.session_state.applicant]
        print(applicant_df['url_list'].values[0])
        with tab1:
            if st.text_input('Timestamp Input (seconds)',key='timestamp'):
                for question, url in applicant_df['url_list'].values[0].items():
                    with st.expander(f"{question}"):
                        if st.session_state.timestamp.isnumeric():
                            timestamp = int(st.session_state.timestamp)
                            st.markdown(f'<iframe src="{url.split("?")[0]}?t={timestamp}s" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

                        else:
                            st.toast(':red[Hey!] Ensure timestamp is numeric!', icon='👺')
                            st.markdown(f'<iframe src="{url}" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)
            else:
                for question, url in applicant_df['url_list'].values[0].items():
                    with st.expander(f"{question}"):
                        st.markdown(f'<iframe src="{url}" width="640" height="480" allow="autoplay"></iframe>',unsafe_allow_html=True)

        with tab2:
            for question, transcript in applicant_df['transcript'].values[0].items():
                with st.expander(f"{question}"):
                    stx.scrollableTextbox(transcript,fontFamily="Source Sans Pro, sans-serif",height=150)
                    st.download_button('Download Transcript', transcript,file_name='transcript.txt',key=question)

        with tab3:
            for question,summary in applicant_df['summary'].values[0].items():
                with st.expander(f"{question}"):
                        st.text(summary)