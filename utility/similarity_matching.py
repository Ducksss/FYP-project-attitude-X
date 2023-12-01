from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer(model_name_or_path='trained_model')

def get_similarity_score(jd_dict, resume_dict):
    for i in ['Technical Skills', 'Soft Skills', 'Languages']:
        x = ', '.join(jd_dict[i])
        y = ', '.join(resume_dict[i])
        q_vec = model.encode([x],convert_to_tensor= True)
        sim = util.cos_sim(q_vec, model.encode([y],convert_to_tensor=True))
        if i == 'Technical Skills':
            techsk_score = sim[0][0]
        if i == 'Soft Skills':
            softsk_score = sim[0][0]
        if i == 'Languages':
            counter = 0
            for language in jd_dict[i]:
                if language.lower() in y.lower():
                    counter += 1
            lang_score = counter/len(jd_dict[i])
        
    return techsk_score, softsk_score, lang_score