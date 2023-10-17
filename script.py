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


# Provide the Resume file path as an argument
file_path = "C:/Users/Admin/OneDrive - Singapore Polytechnic/Desktop/Desktop/FYP/Project Code/FYP-project-attitude-X/resume_data/Resume1.docx"  # Replace with the path to your file
file_type = check_file_type(file_path)

#extract text for docx
if file_type == "DOCX":
    text = docx2txt.process(file_path)
#extract text for pdf
elif file_type == "PDF":    
    text = extract_text(file_path)
else:
    #File type is not accepted
    raise Exception("Filetype is not accepted")

print(text)
