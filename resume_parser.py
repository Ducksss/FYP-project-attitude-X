##Importing libraries
import os
from extract_to_text import convertPDFToText, convertDocxToText
from functions import check_file_type

##Download pretrained model from spacy for name
#python -m spacy download en_core_web_lg

#Provide the Resume file path as an argument
file_path = "resume_data/Resume_1.pdf"  
#Check file type
file_type = check_file_type(file_path)
#Check file size
size = os.path.getsize(file_path)

#Text Extracting for file types and file size
if size>10000000:#10 Million Bytes for 10MB
    print('*************File size too large, please compress file or try again!*************')
else:
    #extract text for pdf
    if file_type == "PDF":    
        text = convertPDFToText(file_path)
        #print("*************Successfully extracted PDF*************")
        #print(text)
    elif file_type == "DOCX": #10 Million Bytes for 10MB
        text = convertDocxToText.process(file_path)
        #print("*************Successfully extracted Word File*************")
        #print(text)
    else:
        #File type is not accepted
        raise Exception("*************Filetype is not accepted*************")

#Preprocess document
import spacy
en = spacy.load('en')

sents = en(text)
people = [ee for ee in sents.ents if ee.label_ == 'PERSON']
print(people)
    
    