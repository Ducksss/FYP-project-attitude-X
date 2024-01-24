##Importing libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import pandas as pd
import streamlit_scrollable_textbox as stx
from extra_streamlit_components import CookieManager
import math
import time

# Importing functions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor
from utility.speech_tagger import transcribeFile
from utility.ner import transcription_prompt
from utility.cloud import uploadFile
from database import get_ovr_score_desc ,get_interview, insert_personality, insert_applicantPers, get_personality, get_applicantPers, update_applicantPers, update_personality, callback

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

st.markdown('<style>label p{font-size:18px !important; font-weight:bold; color: rgb(150, 150, 150)}</style>',unsafe_allow_html=True)

st.title('Database Management :pencil2:')

def get_counter(df):
    if len(df.index) == 0:
        counter = 1
    else:
        counter = max(df["_id"]) + 1
    return counter

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

if st.selectbox('Which database would you like to view?',['Personality','Applicant/Personality'],key='db',index=None,placeholder="Select database..."):
    tab1, tab2, tab3 = st.tabs(['Insert','Edit/Update','Delete'])
    with tab1:
        if st.session_state.db == 'Personality':
            counter = get_counter(get_personality())
            with st.form('Insert Personality',clear_on_submit=True):
                p_type = st.text_input('What is the name of the Personality Type?')
                st.divider()
                question = st.text_area('What are the questions to be asked for this Personality Type? (separate questions using "Enter")')
                questionList = question.split('\n')
                if st.form_submit_button('Insert'):
                    insert_personality(counter,p_type,questionList)
                    st.toast(f"Entry has been :green[successfully uploaded]!", icon='🎉')

        else:
            counter = get_counter(get_applicantPers())
            df1 = get_ovr_score_desc(0.4,0.4,0.2)
            df2 = get_personality()
            with st.form('Insert Applicant/Personality',clear_on_submit=True):
                try:
                    applicant = st.selectbox('Applicant',[x for x in df1['name'].unique()],index=None,placeholder='Select applicant...',label_visibility='hidden')
                    st.divider()
                    personality = st.selectbox('Question',[x for x in df2['personality_type'].unique()],index=None,placeholder='Select personality type...',label_visibility='hidden')
                    if st.form_submit_button('Insert'):
                        insert_applicantPers(counter,applicant,personality)
                        st.toast(f"Entry has been :green[successfully uploaded]!", icon='🎉')

                except KeyError:
                    deadButton = st.form_submit_button('Insert')
                    st.error('Database is not populated!')

    with tab2:
        if st.session_state.db == 'Personality':
            df = get_personality()
            if st.selectbox('Which entry would you like to update?',[f"{df['_id'][x]} - {df['personality_type'][x]}, {df['questions'][x]}" for x,row in enumerate(df.values)],key='id',index=None,placeholder='Select entry...'):
                if st.selectbox('Which column would you like to update?',df.drop(['_id'],axis=1).columns,key='column',index=None,placeholder='Select column...'):
                    st.divider()
                    current_val = df[df['_id'] == int(st.session_state.id[0])][st.session_state.column].values[0]
                    if st.session_state.column == 'questions':
                        updated_val = st.text_area('What is the new value?',value='\n'.join(current_val))
                        updated_val = updated_val.split("\n")
                    else:
                        updated_val = st.text_input('What is the new value?',value=current_val)

                    if st.button('Update'):
                        if updated_val == current_val:
                            st.toast(':red[Hey!] Updated value is the same as the current value!', icon='👺')
                        else:
                            update_personality(int(st.session_state.id[0]),st.session_state.column,updated_val)
                            st.toast(f"Database has been :green[successfully updated]!", icon='🎉')
                            time.sleep(0.2)
                            st.rerun()
        else:
            df1 = get_applicantPers()
            df2 = get_ovr_score_desc(0.4,0.4,0.2)
            df3 = get_personality()
            if st.selectbox('Which entry would you like to update?',[f"{df1['_id'][x]} - {df1['applicant'][x]}, {df1['personality_type'][x]}" for x,row in enumerate(df1.values)],key='id',index=None,placeholder='Select entry...'):
                if st.selectbox('Which column would you like to update?',df1.drop(['_id'],axis=1).columns,key='column',index=None,placeholder='Select column...'):
                    st.divider()
                    current_val = df1[df1['_id'] == int(st.session_state.id[0])][st.session_state.column].values[0]
                    if st.session_state.column == 'applicant':
                        updated_val = st.selectbox('Applicant',df2['name'].unique(),index=None,placeholder='Select applicant...',label_visibility='hidden')
                    else:
                        updated_val = st.selectbox('Question',df3['personality_type'].unique(),index=None,placeholder='Select personality type...',label_visibility='hidden')
                    if st.button('Update'):
                        if updated_val == current_val:
                            st.toast(':red[Hey!] Updated value is the same as the current value!', icon='👺')
                        else:
                            update_applicantPers(int(st.session_state.id[0]),st.session_state.column,updated_val)
                            st.toast(f"Database has been :green[successfully updated]!", icon='🎉')
                            time.sleep(0.2)
                            st.rerun()

    with tab3:
        if st.session_state.db == 'Personality':
            st.session_state['data'] = get_personality()
            st.session_state.default_table = get_personality()
            st.session_state.dbcode = 1
        else:
            st.session_state['data'] = get_applicantPers()
            st.session_state.default_table = get_applicantPers()
            st.session_state.dbcode = 2

        columns = st.session_state['data'].columns

        column_config = {column: st.column_config.Column(disabled=True) for column in columns}

        modified_df = st.session_state['data'].copy()
        modified_df["Delete"] = False

        # Make Delete be the first column
        modified_df = modified_df[["Delete"] + modified_df.columns[:-1].tolist()]
        if len(modified_df) > 0:
            if st.session_state.db == 'Personality':
                modified_df = modified_df[["Delete","_id","personality_type","questions"]]
            else:
                modified_df = modified_df[["Delete","_id","applicant","personality_type"]]

        st.data_editor(
            modified_df,
            key="data_editor",
            hide_index=True,
            column_config=column_config,
        )

        st.button('Delete',on_click=callback,type='primary')