#Importing Libraries
import pymongo
import pandas as pd
import streamlit as st

#local host
# mongo_url = "mongodb://localhost:27017"
#docker 
mongo_url = "mongodb://localhost:27012"

myclient = pymongo.MongoClient(mongo_url)   
# myclient = pymongo.MongoClient('', 27017)
mydb = myclient["resumeDB"]
mycol = mydb["scores"]
interview_col = mydb['interview']
personality_col = mydb['personality']
applicantPersonality_col = mydb['applicant_personality']

def calculate_score(w1,w2,w3):
    return lambda x : round(w1* x['technical_skills'] + w2*x['soft_skills'] + w3*x['languages'],1)

def aggregate_table(table,w1,w2,w3):
    table = table.assign(overall_score = calculate_score(w1,w2,w3))
    return table


def insert_score(counter,resume_dict, techsk_score, softsk_score, lang_score):
    mydict =  {
        "_id": counter,
        "name": resume_dict["Name"],
        "email":resume_dict["email"],
        "contact_number":resume_dict["contact_number"], 
        "technical_skills" : float(techsk_score), 
        "soft_skills": float(softsk_score), 
        "languages": float(lang_score), 
        }

    x = mycol.insert_one(mydict)
    return

def insert_interview(counter,name,transcript,summary,url_list):
    mydict =  {
        "_id": counter,
        "name": name,
        "transcript": transcript,
        "summary": summary, 
        "url_list" : url_list 
        }

    x = interview_col.insert_one(mydict)
    return x

def insert_personality(counter,type, questions):
    mydict =  {
        "_id": counter,
        "personality_type": type,
        "questions": questions,
        }

    x = personality_col.insert_one(mydict)
    return

def insert_applicantPers(counter,name,personality):
    mydict = {
        "_id": counter,
        "applicant": name,
        "personality_type": personality
    }

    x = applicantPersonality_col.insert_one(mydict)
    return

def get_personality():
    table = pd.DataFrame(personality_col.find())

    return table

def get_applicantPers():
    table = pd.DataFrame(applicantPersonality_col.find())

    return table

def update_personality(count,column,updated_val):
    filter = { '_id': count }
    
    # Values to be updated.
    newvalues = { "$set": { column: updated_val } }
    
    personality_col.update_one(filter, newvalues) 

    return

def update_applicantPers(count,column,updated_val):
    # Updating fan quantity from 10 to 25.
    filter = { '_id': count }
    
    # Values to be updated.
    newvalues = { "$set": { column: updated_val } }
    
    applicantPersonality_col.update_one(filter, newvalues) 

    return

def update_interview(count,new_value):
    # Updating fan quantity from 10 to 25.
    filter = { '_id': count }
    
    # Values to be updated.
    newvalues = { "$set": { 'bounding_url_list': new_value } }

    interview_col.update_one(filter, newvalues) 

    return

def get_interview():
    table = pd.DataFrame(interview_col.find())

    return table

def get_ovr_score_desc(w1,w2,w3):
    table = pd.DataFrame(mycol.find())
    if len(table) != 0:
        table = aggregate_table(table,w1,w2,w3)
        st.session_state.default_table = table
        table = search_score(table)
    return table

def search_score(table):
    try:
        if 'score' not in st.session_state:
            score = 0
        else:
            score = float(st.session_state.score)

        if 'var' not in st.session_state:
            variable = 'overall_score'
        else:
            if st.session_state.var == 'Technical Skills':
                variable = 'technical_skills'
            elif st.session_state.var == 'Soft Skills':
                variable = 'soft_skills'
            elif st.session_state.var == 'Language':
                variable = 'languages'
            else:
                variable = 'overall_score'

        if 'eq' not in st.session_state:
            equality = '>='
        else:
            if st.session_state.eq == 'Lesser than Equal to':
                equality = '<='
            else:
                equality = '>='

        myquery = f'{variable}{equality}{score}'
        table = table.query(myquery)
        return table
    except:
        return

def remove_rows(collection,count):
    collection.delete_one({"_id": count})

def callback():
    df = st.session_state.default_table
    db = st.session_state.dbcode
    edited_rows = st.session_state["data_editor"]["edited_rows"]
    rows_to_delete = []
    
    for idx, value in edited_rows.items():
        if value["Delete"] is True:
            rows_to_delete.append(idx)

        if len(rows_to_delete)==1:
            count = df._get_value(rows_to_delete[0],'_id')
            count = int(count)
            if db == 1:
                remove_rows(personality_col,count)
            elif db == 2:
                remove_rows(applicantPersonality_col,count)
            else:
                remove_rows(mycol,count)
            st.toast(":green[Deletion Complete]!", icon='🎉')

        elif len(rows_to_delete)> 1:
            while len(rows_to_delete) > 0:
                count = df._get_value(rows_to_delete[0],'_id')
                count = int(count)
                if db == 1:
                    remove_rows(personality_col,count)
                elif db == 2:
                    remove_rows(applicantPersonality_col,count)
                else:
                    remove_rows(mycol,count)
                rows_to_delete.pop(0)
        else:
            st.toast(':red[Hey!] Please select the rows you want to delete!', icon='👺')

    st.session_state["data"] = (
        st.session_state["data"].drop(index = rows_to_delete,axis=0).reset_index(drop=True)
    )