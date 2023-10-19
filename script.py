##Importing libraries
import os

##Importing Functions
from functions import check_file_type
from convert_to_text import convertPDFToText, convertDocxToText
from extract_from_text import extract_name, extract_email, extract_contact_number

#Provide the Resume file path as an argument
file_path = "resume_data/Resume_2.docx"  
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
        resume_text = convertPDFToText(file_path)
        #print("*************Successfully extracted PDF*************")
        #print(text)
    elif file_type == "DOCX": #10 Million Bytes for 10MB
        resume_text = convertDocxToText(file_path)
        #print("*************Successfully extracted Word File*************")
        #print(text)
    else:
        #File type is not accepted
        raise Exception("*************Filetype is not accepted*************")

if __name__ == '__main__':
    contact_number = extract_contact_number(resume_text)
    if contact_number:
        print("Contact Number:", contact_number)
    else:
        print("Contact Number not found")

    email = extract_email(resume_text)
    if email:
        print("Email:", email)
    else:
        print("Email not found")
    name = extract_name(resume_text)
    if name:
        print("Name:", name)
    else:
        print("Name not found")
                                                                                                                           
