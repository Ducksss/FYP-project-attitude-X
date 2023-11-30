from sentence_transformers import SentenceTransformer, util, InputExample, losses
from torch.utils.data import DataLoader

model = SentenceTransformer('all-mpnet-base-v2')

#Define the training examples
train_examples = [InputExample(texts=['Sales and business development', 'Prezi'], label=0.2),
                  InputExample(texts=['Sales and business development', 'Sales Negotiation'], label=0.6),
                  InputExample(texts=['Sales and business development', 'Market Trend'], label=0.55),
                  InputExample(texts=['Sales and business development', 'Digital Marketing'], label=0.65),
                  InputExample(texts=['Lead generation and prospecting', 'Mircosoft Excel'], label=0.1),
                  InputExample(texts=['Lead generation and prospecting', 'Leadership'], label=0.6),
                  InputExample(texts=['Relationship building and management', 'Google Analytics'], label=0.1),
                  InputExample(texts=['Relationship building and management', 'Networking'], label=0.65),
                  InputExample(texts=['Relationship building and management', 'Raport Building'], label=0.65),
                  InputExample(texts=['Relationship building and management', 'Team Management'], label=0.65),
                  InputExample(texts=['Relationship building and management', 'Interpersonal communication'], label=0.65),
                  InputExample(texts=['Relationship building and management', 'Interpersonal skills'], label=0.65),
                  InputExample(texts=['Sales presentations and negotiations', 'SurveyMonkey'], label=0.1),
                  InputExample(texts=['Sales presentations and negotiations', 'Market Trend'], label=0.4),
                  InputExample(texts=['Sales presentations and negotiations', 'Vendor Negotiations'], label=0.5),
                  InputExample(texts=['Sales presentations and negotiations', 'Sales Negotiation'], label=0.5),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Project Management'], label=0.5),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Communication'], label=0.55),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Team Management'], label=0.65),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Team collaboration'], label=0.65),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Rapport Building'], label=0.65),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Interpersonal communication'], label=0.7),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Interpersonal skills'], label=0.7),
                  InputExample(texts=['Collaboration and coordination with internal teams', 'Teamwork'], label=0.7),
                  InputExample(texts=['Product demonstrations and proposal creation', 'Data Analysis'], label=0.1),
                  InputExample(texts=['Product demonstrations and proposal creation', 'Collaboration'], label=0.1),
                  InputExample(texts=['Market research and analysis', 'Strategic Planning'], label=0.2),
                  InputExample(texts=['Market research and analysis', 'Market Trend'], label=0.4),
                  InputExample(texts=['Market research and analysis', 'Data Analysis'], label=0.7),
                  InputExample(texts=['Market research and analysis', 'Google Analysis'], label=0.65),
                  InputExample(texts=['Market research and analysis', 'SAS Office Analysis'], label=0.65),
                  InputExample(texts=['Customer success management', 'Process Optimization'], label=0.1),
                  InputExample(texts=['Customer success management', 'Team Management'], label=0.4),
                  InputExample(texts=['Customer success management', 'Stake holder engagement'], label=0.55),
                  InputExample(texts=['Customer success management', 'Customer Retention'], label=0.7),
                  InputExample(texts=['Customer success management', 'Customer Satisfaction'], label=0.7),
                  InputExample(texts=['Customer success management', 'Customer service'], label=0.7),
                  InputExample(texts=['Customer success management', 'Consumer engagement'], label=0.7),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Networking'], label=0.6),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Detail-oriented Communication'], label=0.65),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Written and Oral Communication'], label=0.65),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Communication'], label=0.65),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Rapport Building'], label=0.65),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Collaboration'], label=0.6),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Team collaboration'], label=0.6),
                  InputExample(texts=['Excellent communication and interpersonal skills', 'Interpersonal communication'], label=0.85),
                  InputExample(texts=['Results-oriented mindset', 'HubSpot'], label=0.1),
                  InputExample(texts=['Results-oriented mindset', 'Data Analysis'], label=0.1),
                  InputExample(texts=['Results-oriented mindset', 'Detail-oriented Communication'], label=0.6),
                  InputExample(texts=['Results-oriented mindset', 'Attention to details'], label=0.6),
                  InputExample(texts=['Results-oriented mindset', 'Goal-oriented'], label=0.85),
                  InputExample(texts=['Time management and prioritization', 'Attention to details'], label=0.35),
                  InputExample(texts=['Time management and prioritization', 'Process Optimization'], label=0.55),
                  InputExample(texts=['Time management and prioritization', 'Work Ethic'], label=0.55),
                  InputExample(texts=['Time management and prioritization', 'Team Management'], label=0.55),
                  InputExample(texts=['Self-motivation and drive to exceed sales targets', 'Project Management'], label=0.2),
                  InputExample(texts=['Self-motivation and drive to exceed sales targets', 'Work Ethic'], label=0.55),
                  InputExample(texts=['Self-motivation and drive to exceed sales targets', 'Power BI'], label=0.1),
                  InputExample(texts=['Ability to work independently and as a team player', 'Active Listener'], label=0.35),
                  InputExample(texts=['Ability to work independently and as a team player', 'Collaboration'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Team collaboration'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Team Management'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Rapport Building'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Networking'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Interpersonal skills'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Interpersonal communication'], label=0.5),
                  InputExample(texts=['Ability to work independently and as a team player', 'Adaptability'], label=0.4),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'HubSpot'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Google Analytics'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'SAS Office Analytics'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'PowerBI'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Microsoft Excel'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Microsoft'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'JIRA'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Pivot Tables'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Microsoft Office'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Microsoft Office Suite'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Salesforce'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Social media marketing software'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Mailchimp'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'SAP'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Zendesk'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'LinkedIn'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Data-driven software analytics programs'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Tableau'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Wordpress'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Vecta'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'DevOps'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Point of Sale'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'POS'], label=0.5),
                  InputExample(texts=['Good knowledge of technology and social networking tools', 'Bitrix'], label=0.5)
                ]

#Define train dataset, the dataloader and the train loss
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=8)
train_loss = losses.CosineSimilarityLoss(model)

#Tune the model
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=5, warmup_steps=100)

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