import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["resumeDB"]
mycol = mydb["scores"]


def insert_score(resume_dict, techsk_score, softsk_score, lang_score, overall_score):
    mydict =  {
        "name": resume_dict["Name"],
        "email":resume_dict["email"],
        "contact_number":resume_dict["contact_number"], 
        "technical_skills" : round(techsk_score.item()*100,2), 
        "soft_skills": round(softsk_score.item()*100,2), 
        "languages": round(lang_score*100,2), 
        "overall_score": round(overall_score.item()*100,2)
        }

    x = mycol.insert_one(mydict)

    return

def get_ovr_score_desc():
    table = pd.DataFrame(mycol.find().sort('overall_score',-1))

    return table

def get_techsk_score_desc():
    table = pd.DataFrame(mycol.find().sort('technical_skills',-1))

    return table

def get_softsk_score_desc():
    table = pd.DataFrame(mycol.find().sort('soft_skills',-1))

    return table

def get_lang_score_desc():
    table = pd.DataFrame(mycol.find().sort('languages',-1))

    return table

def search_score(score):
    myquery = {"overall_score" : {"$gte": score}}
    table = pd.DataFrame(mycol.find(myquery))

    return table