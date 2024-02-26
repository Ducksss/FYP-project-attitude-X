##Importing libraries
import os
import sys
import streamlit as st
from st_pages import hide_pages
import pandas as pd
from extra_streamlit_components import CookieManager
import time

# Importing functions
from streamlit_extras.switch_page_button import switch_page
from utility.classes import dataProcessor
from database import get_ovr_score_desc, insert_personality, insert_applicantPers, get_personality, get_applicantPers, update_applicantPers, update_personality, callback

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css(2)

st.markdown('<style>label p{font-size:18px !important; font-weight:bold; color: rgb(150, 150, 150)}</style>',unsafe_allow_html=True)

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

col1, gap, col2 = st.columns([0.4,0.1,0.5])
with col1:
    database = st.selectbox('Which database would you like to view?',['Personality','Applicant/Personality'],key='db',index=None,placeholder="Select database...")
    tab1, tab2 = st.tabs(['Insert','Edit/Update'])
    with tab1:
        if st.session_state.db == 'Personality':
            counter = get_counter(get_personality())
            with st.form('Insert Personality',clear_on_submit=True):
                p_type = st.text_input('What is the name of the Personality Type? :face_with_monocle:')
                st.divider()
                question = st.text_area('What are the questions to be asked for this Personality Type? (separate questions using "Enter") :speech_balloon:')
                questionList = question.split('\n')
                if st.form_submit_button('Insert'):
                    if p_type.strip() != '' and len(questionList) != 0:
                        if len(questionList) == 3:
                            insert_personality(counter,p_type,questionList)
                            st.toast(f"Entry has been :green[successfully uploaded]!", icon='🎉')
                        else:
                            st.toast(':red[Hey!] Make sure there are exactly 3 questions!', icon='👺')
                    else:
                        st.toast(':red[Hey!] Value for personality or question(s) is/are empty!', icon='👺')

        elif st.session_state.db == 'Applicant/Personality':
            counter = get_counter(get_applicantPers())
            df1 = get_ovr_score_desc(0.4,0.4,0.2)
            df2 = get_personality()
            if not df1.empty and not df2.empty:
                with st.form('Insert Applicant/Personality',clear_on_submit=True):
                    applicant = st.selectbox('Who is the Applicant? :office_worker:',[x for x in df1['name'].unique()],index=None,placeholder='Select applicant...')
                    st.divider()
                    personality = st.selectbox("What is the Applicant's personality? :face_with_monocle:",[x for x in df2['personality_type'].unique()],index=None,placeholder='Select personality type...')
                    if st.form_submit_button('Insert'):
                        if applicant.strip() != '' and personality.strip() != '' :
                            insert_applicantPers(counter,applicant,personality)
                            st.toast(f"Entry has been :green[successfully uploaded]!", icon='🎉')
                        else:
                            st.toast(':red[Hey!] Value for applicant or personality is empty!', icon='👺')

            else:
                st.error("Either Applicant's Scoring database or Personality database is empty!")

        else:
            st.error('Please select a database!')

        with tab2:
            try:
                if st.session_state.db == 'Personality':
                    df = get_personality()
                    entry = st.selectbox('Which entry would you like to update? :scroll:',[f"{df['_id'][x]} - {df['personality_type'][x]}, {df['questions'][x]}" for x,row in enumerate(df.values)],key='id',index=None,placeholder='Select entry...')
                    dfColumn = st.selectbox('Which column would you like to update? :bookmark_tabs:',df.drop(['_id'],axis=1).columns,key='column',index=None,placeholder='Select column...')
                    st.divider()
                    if entry and dfColumn:
                        current_val = df[df['_id'] == int(st.session_state.id[0])][st.session_state.column].values[0]
                        if st.session_state.column == 'questions':
                            updated_val = st.text_area('What question(s) to update to? :speech_balloon:',value='\n'.join(current_val))
                            updated_val = updated_val.split("\n")
                        else:
                            updated_val = st.text_input('What is the new personality? :face_with_monocle:',value=current_val)

                        if st.button('Update'):
                            if updated_val == current_val:
                                st.toast(':red[Hey!] Updated value is the same as the current value!', icon='👺')
                            elif isinstance(updated_val,list) == False:
                                if updated_val.strip()=='':
                                    st.toast(':red[Hey!] Updated value is empty!', icon='👺')
                                else:
                                    update_personality(int(st.session_state.id[0]),st.session_state.column,updated_val)
                                    st.toast(f"Database has been :green[successfully updated]!", icon='🎉')
                                    time.sleep(0.2)
                                    st.rerun()
                            else:
                                if len(updated_val) == 3:
                                    update_personality(int(st.session_state.id[0]),st.session_state.column,updated_val)
                                    st.toast(f"Database has been :green[successfully updated]!", icon='🎉')
                                    time.sleep(0.2)
                                    st.rerun()
                                else:
                                    st.toast(':red[Hey!] Make sure there are exactly 3 questions!', icon='👺')

                elif st.session_state.db == 'Applicant/Personality':
                    df1 = get_applicantPers()
                    df2 = get_ovr_score_desc(0.4,0.4,0.2)
                    df3 = get_personality()
                    entry = st.selectbox('Which entry would you like to update? :scroll:',[f"{df1['_id'][x]} - {df1['applicant'][x]}, {df1['personality_type'][x]}" for x,row in enumerate(df1.values)],key='id',index=None,placeholder='Select entry...')
                    dfColumn = st.selectbox('Which column would you like to update? :bookmark_tabs:',df1.drop(['_id'],axis=1).columns,key='column',index=None,placeholder='Select column...')
                    st.divider()
                    if entry and dfColumn:
                        current_val = df1[df1['_id'] == int(st.session_state.id[0])][st.session_state.column].values[0]
                        if st.session_state.column == 'applicant':
                            updated_val = st.selectbox('Which Applicant to update to? :office_worker:',df2['name'].unique(),index=None,placeholder='Select applicant...')
                        else:
                            updated_val = st.selectbox('What Question(s) to update to? :speech_balloon:',df3['personality_type'].unique(),index=None,placeholder='Select personality type...')
                        
                        if st.button('Update'):
                            if updated_val == current_val:
                                st.toast(':red[Hey!] Updated value is the same as the current value!', icon='👺')
                            elif updated_val.strip() == '':
                                st.toast(':red[Hey!] Updated value is empty!', icon='👺')
                            else:
                                update_applicantPers(int(st.session_state.id[0]),st.session_state.column,updated_val)
                                st.toast(f"Database has been :green[successfully updated]!", icon='🎉')
                                time.sleep(0.2)
                                st.rerun()

                else:
                    st.error('Please select a database!')

            except KeyError:
                if st.session_state.db == 'Applicant/Personality':
                    st.error("Either Applicant's Scoring database, Applicant/Personality or Personality database is empty!")
                else:
                    st.error("Personality database is empty!")
                    
        with col2:
            st.title('Database Management :pencil2:')
            if database:
                try:
                    if st.session_state.db == 'Personality':
                        st.session_state['data'] = get_personality()
                        st.session_state.default_table = get_personality()
                        st.session_state.dbcode = 1
                    elif st.session_state.db == 'Applicant/Personality':
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
                        use_container_width=True
                    )

                    st.button('Delete',on_click=callback,type='primary')
                except KeyError:
                    st.warning('Database is not populated!')

            else:
                st.dataframe(pd.DataFrame(),use_container_width=True)