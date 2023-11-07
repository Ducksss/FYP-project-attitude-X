#Importing Libraries
import pymongo
import pandas as pd
import streamlit as st
from bson import Decimal128

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["resumeDB"]
mycol = mydb["scores"]

def set_table_style(table):
    blankIndex=[''] * len(table)
    table.index=blankIndex
    return table

def insert_score(resume_dict, techsk_score, softsk_score, lang_score, overall_score):
    mydict =  {
        "name": resume_dict["Name"],
        "email":resume_dict["email"],
        "contact_number":resume_dict["contact_number"], 
        "technical_skills" : float(techsk_score), 
        "soft_skills": float(softsk_score), 
        "languages": float(lang_score), 
        "overall_score": float(overall_score)
        }

    x = mycol.insert_one(mydict)
    return

def get_ovr_score_desc():
    table = pd.DataFrame(mycol.find().sort('overall_score',-1))
    if len(table) != 0:
        table = table.drop(['_id'],axis=1)
        table = set_table_style(table)     
    return table

def get_ovr_score_asc():
    table = pd.DataFrame(mycol.find().sort('overall_score',1))
    if len(table) != 0:
        table = table.drop(['_id'],axis=1)
        table = set_table_style(table)     
    return table

def search_score():
    try:
        score = float(st.session_state.score)
        if st.session_state.var == 'Technical Skills':
            variable = 'technical_skills'
        elif st.session_state.var == 'Soft Skills':
            variable = 'soft_skills'
        elif st.session_state.var == 'Language':
            variable = 'languages'
        else:
            variable = 'overall_score'
        if st.session_state.eq == 'Less than Equal to':
            equality = '$lte'
        else:
            equality = '$gte'
        myquery = { variable : {equality: score}}
        table = pd.DataFrame(mycol.find(myquery))
        if len(table) != 0:
            table = table.drop(['_id'],axis=1)
        st.session_state.filter_table = table
        return table
    except:
        return