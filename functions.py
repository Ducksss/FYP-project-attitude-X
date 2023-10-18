import os

# Function to check file extension
def check_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".docx":
        return "DOCX"
    elif file_extension.lower() == ".pdf":
        return "PDF"
    else:
        return "Other"