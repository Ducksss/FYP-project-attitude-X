##Import Extraction Libraries
import re
import streamlit as st
from pdfminer.high_level import extract_text

##Import PIL Library
from PIL import Image

##Importing from utility 
from utility.stopwords import filter_stopwords
from utility.similarity_matching import get_similarity_score
from utility.ner import jd_prompt_1, resume_prompt, convert_to_dict, chatbot

class dataProcessor:
    
    def __init__(self):
        # Initalize instance attributes
        self.file_name = "./docs/static/style.css"
        self.email = None
        self.contact_number = None

    #CSS File For Streamlit Pages
    def local_css(self,default=1):

        # Loading Image using PIL
        icon = Image.open('docs/static/drawmetrics_icon.jpg')
        # Adding Image to web app
        if default == 1:
            st.set_page_config(page_title="Drawmetrics Applicant Tracking System", page_icon = icon)
        else:
            st.set_page_config(page_title="Drawmetrics Applicant Tracking System", page_icon = icon, layout="wide")

        with open(self.file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    #Functions for conversion PDF
    def convertPDFToText(self,file_path):
        return extract_text(file_path)
    
    #Regex function for extracting email
    def extract_email(self,text):
        # Use regex pattern to find a potential email address
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        if match:
            self.email = match.group()
            # Remove all spaces from the email
            formatted_email = self.email.replace(" ", "")
        else:
            formatted_email = "NA"

        return formatted_email    

    #Regex function for extracting phone number
    def extract_contact_number(self,text):
        # Use regex pattern to find a potential contact number
        if re.search('[(]\d[)]', text):
            text = re.sub('[(].*[)]','',text)
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b"
        match = re.search(pattern, text)
        if match:
            self.contact_number = match.group()
            formatted_contact_number = self.contact_number.replace(" ", "")
        else:
            formatted_contact_number = "NA"
            
        return formatted_contact_number
    
    # Calling NER & Stopwords
    def process_text(self,text,filetype):
        text_filter = filter_stopwords(text)
        print("-"*10 + "Filtered Text"+"-"*10)
        print(text_filter)
        if filetype == 'JD':
            #Getting Dictionary of details from Job Description
            jd_result = jd_prompt_1(text_filter)
            jd_dict = convert_to_dict(jd_result)
            #print(jd_dict)
            return jd_dict
        elif filetype == 'Resume':
            #Getting Dictionary of details from resume
            contact_number = self.extract_contact_number(text)
            email = self.extract_email(text)
            resume_result = resume_prompt(text_filter)
            resume_dict = convert_to_dict(resume_result)
            resume_dict['contact_number'] = contact_number
            resume_dict['email'] = email
            #print(resume_dict)
            return resume_dict
    
    #Calculating Scores
    def get_score(self, jd_dict, resume_dict):
        techsk_score, softsk_score, lang_score = get_similarity_score(jd_dict, resume_dict)
        
        techsk_score = round(techsk_score.item()*100,1)
        softsk_score = round(softsk_score.item()*100,1)
        lang_score = round(lang_score*100,1)
        
        return techsk_score, softsk_score, lang_score
    
    def use_chatbot(self):
        return chatbot()
