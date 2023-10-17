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
file_path = "resume_data/10MB_file.pdf"  
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
        print("*************Successfully extracted PDF*************")
        print(text)
    elif file_type == "DOCX": #10 Million Bytes for 10MB
        text = docx2txt.process(file_path)
        print("*************Successfully extracted Word File*************")
        print(text)
    else:
        #File type is not accepted
        raise Exception("*************Filetype is not accepted*************")

