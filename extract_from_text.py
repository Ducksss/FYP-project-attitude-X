##Import NER Libraries
import re
import spacy

def extract_name(text):
    nlp = spacy.load('en_core_web_trf')                                                                                                                  
    sents = nlp(text) 
    people = [ee for ee in sents.ents if ee.label_ == 'PERSON']       
    # Remove newline characters and split the text into lines
    name = str(people[0])

    # Split the text by newline characters and take the first part
    # some names may be falsely extracted to the next line
    corrected_name = name.split("\n")[0]

    # Split the text into words, convert each word to lowercase with the first letter capitalized
    formatted_name = ' '.join(word.capitalize() for word in corrected_name.split())
    return formatted_name

def extract_email(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    # Remove all spaces from the email
    formatted_email = email.replace(" ", "")

    return formatted_email    

def extract_contact_number(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    #pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
        
    # Remove all spaces from the contact number
    formatted_contact_number = contact_number.replace(" ", "")

    return formatted_contact_number