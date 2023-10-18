##Import NER Libraries
import re
import spacy

def extract_name(text):
    nlp = spacy.load('en_core_web_trf')                                                                                                                  
    sents = nlp(text) 
    people = [ee for ee in sents.ents if ee.label_ == 'PERSON']       
    return people[0]

def extract_email(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email    

def extract_contact_number(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    #pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number