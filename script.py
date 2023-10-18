#pip install -r requirements.txt

##Importing libraries
import os
import docx2txt
from pdfminer.high_level import extract_text

# Function to check file extension
def check_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".docx":
        return "DOCX"
    elif file_extension.lower() == ".pdf":
        return "PDF"
    else:
        return "Other"

#Provide the Resume file path as an argument
file_path = "resume_data/Resume_4.pdf"  
#Check file type
file_type = check_file_type(file_path)
#Check file size
size = os.path.getsize(file_path)
print(size) #95772


#Text Extracting for file types and file size
if size>10000000:#10 Million Bytes for 10MB
    print('*************File size too large, please compress file or try again!*************')
else:
    #extract text for pdf
    if file_type == "PDF":    
        text = extract_text(file_path)
        #print("*************Successfully extracted PDF*************")
        #print(text)
    elif file_type == "DOCX": #10 Million Bytes for 10MB
        text = docx2txt.process(file_path)
        #print("*************Successfully extracted Word File*************")
        #print(text)
    else:
        #File type is not accepted
        raise Exception("*************Filetype is not accepted*************")



# nltk library
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag

# def preprocess(sent):
#     sent = nltk.word_tokenize(sent)
#     sent = nltk.pos_tag(sent)
#     return sent

# sent = preprocess(text)
# print(sent)

# pattern = 'NP: {<DT>?<JJ>*<NN>}'
# cp = nltk.RegexpParser(pattern)
# cs = cp.parse(sent)
# print(cs)



import spacy
from spacy.matcher import Matcher
import re

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    #pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number

def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email

import spacy
from spacy.matcher import Matcher

def extract_name_from_resume(text):
    name = None

    # Use regex pattern to find a potential name
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()

    return name

# if __name__ == '__main__':
#     resume_text = text

#     name = extract_name_from_resume(resume_text)
#     if name:
#         print("Name:", name)
#     else:
#         print("Name not found")

#     contact_number = extract_contact_number_from_resume(resume_text)
#     if contact_number:
#         print("Contact Number:", contact_number)
#     else:
#         print("Contact Number not found")

#     email = extract_email_from_resume(resume_text)
#     if email:
#         print("Email:", email)
#     else:
#         print("Email not found")



import spacy                                                                                                                            

nlp = spacy.load('en_core_web_trf')                                                                                                                  
sents = nlp(text) 
people = [ee for ee in sents.ents if ee.label_ == 'PERSON']        
print(people)