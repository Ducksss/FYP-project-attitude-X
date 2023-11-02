import os
from stopwords import filter_stopwords
from ner import jd_prompt_1, resume_prompt, convert_to_dict
from extract_from_text import extract_email, extract_contact_number
from similarity_matching import get_similarity_score

# Function to check file extension
def check_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".docx":
        return "DOCX"
    elif file_extension.lower() == ".pdf":
        return "PDF"
    else:
        return "Other"
    
def process_text(text, filetype):
    text_filter = filter_stopwords(text)
    if filetype == 'JD':
        #Getting Dictionary of details from Job Description
        jd_result = jd_prompt_1(text_filter)
        jd_dict = convert_to_dict(jd_result)
        return jd_dict
    elif filetype == 'Resume':
        #Getting Dictionary of details from resume
        contact_number = extract_contact_number(text)
        email = extract_email(text)
        resume_result = resume_prompt(text_filter)
        resume_dict = convert_to_dict(resume_result)
        resume_dict['contact_number'] = contact_number
        resume_dict['email'] = email
        return resume_dict
    
def print_score(jd_dict, resume_dict):
    techsk_score, softsk_score, lang_score = get_similarity_score(jd_dict, resume_dict)
    overall_score = techsk_score*0.4+softsk_score*0.4+lang_score*0.2
    
    score_string = "Scoring for " + resume_dict['Name'] + "\n" + \
                'Technical Skills Score: ' + techsk_score + "\n" + \
                'Soft Skills Score: ' + softsk_score + "\n" + \
                'Language Skills Score: ' + lang_score + "\n" + \
                'Overall Skills Score: ' + str(overall_score) + "\n"

                    
    return score_string