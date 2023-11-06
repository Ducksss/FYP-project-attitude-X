##Importing libraries
import os

##Importing Functions
from utility.functions import check_file_type
from utility.convert_to_text import convertPDFToText, convertDocxToText
from utility.extract_from_text import extract_email, extract_contact_number
from utility.ner import jd_prompt_1, resume_prompt, convert_to_dict
from utility.similarity_matching import get_similarity_score
from utility.stopwords import filter_stopwords
  
def file_processing(file_path):
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
        elif file_type == "DOCX": #10 Million Bytes for 10MB
            text = convertDocxToText(file_path)
        else:
            #File type is not accepted
            raise Exception("*************Filetype is not accepted*************")
        
    return text

if __name__ == '__main__':
    #Provide the Job Description & Resume file path as an argument
    file_path_job = "sample_data/JD.docx"
    file_path_resume = "sample_data/Resume_1.docx"
    
    #Extract text for resume and job description
    jd_text = file_processing(file_path_job)
    resume_text = file_processing(file_path_resume)
    
    #Filter the stopwords
    resume_text_filter = filter_stopwords(resume_text)
    jd_text_filter = filter_stopwords(jd_text)
    
    #Getting Dictionary of details from Job Description
    jd_result = jd_prompt_1(jd_text_filter)
    jd_dict = convert_to_dict(jd_result)
    print(f'*****************Job Description: {jd_dict}')
    
    #Getting Dictionary of details from resume
    contact_number = extract_contact_number(resume_text)
    email = extract_email(resume_text)
    resume_result = resume_prompt(resume_text_filter)
    resume_dict = convert_to_dict(resume_result)
    resume_dict['contact_number'] = contact_number
    resume_dict['email'] = email
    print(f'*****************Resume Description: {resume_dict}')
    
    #Compare Job Description and Resume 
    techsk_score, softsk_score, lang_score = get_similarity_score(jd_dict, resume_dict)
    overall_score = techsk_score*0.4+softsk_score*0.4+lang_score*0.2
    
    print(f"Scoring for {resume_dict['Name']}")
    print(f'Technical Skills Score: {techsk_score}')
    print(f'Soft Skills Score: {softsk_score}')
    print(f'Language Skills Score: {lang_score}')
    print(f'Overall Skills Score:{overall_score}')
    
    
    #No. 1 Charlotte
    #0.49, 0.6 (overall language has problem)
    #No. 2 Bertrand
    #0.46, 0.47
    #No. 3 Mykola
    #0.50, 0.86
    #No. 4 Djamila
    #0.46, 0.56
    #No. 5 Lu zhang 
    #0.41, 0.84
    

    