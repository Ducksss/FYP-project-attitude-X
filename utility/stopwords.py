#using spacy stopwords
import spacy
#loading the english language small model of spacy
en = spacy.load('en_core_web_sm')
stopwords = en.Defaults.stop_words

def filter_stopwords(text):
    lst=[]
    for token in text.split():
        if token.lower() not in stopwords:    #checking whether the word is not 
            lst.append(token)                 #present in the stopword list.
        
    #Join items in the list
    #print("Original text  : ",text)
    return "Text after removing stopwords  :   ",' '.join(lst)
    
    
