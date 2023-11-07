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
        "technical_skills" : Decimal128(str(techsk_score)), 
        "soft_skills": Decimal128(str(softsk_score)), 
        "languages": Decimal128(str(lang_score)), 
        "overall_score": Decimal128(str(overall_score))
        }

    x = mycol.insert_one(mydict)
    return

def get_ovr_score_desc():
    table = pd.DataFrame(mycol.find().sort('overall_score',-1))
    if len(table) != 0:
        table = table.drop(['_id'],axis=1)
        table = set_table_style(table)
    return table

def get_techsk_score_desc():
    table = pd.DataFrame(mycol.find().sort('technical_skills',-1)).drop(['_id'],axis=1)
    return table

def get_softsk_score_desc():
    table = pd.DataFrame(mycol.find().sort('soft_skills',-1)).drop(['_id'],axis=1)
    return table

def get_lang_score_desc():
    table = pd.DataFrame(mycol.find().sort('languages',-1)).drop(['_id'],axis=1)
    return table

def search_score(score):
    myquery = {"overall_score" : {"$gte": score}}
    table = pd.DataFrame(mycol.find(myquery)).drop(['_id'],axis=1)

    return table