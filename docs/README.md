## Group of 3 students from Singapore Polytechnic's Artificial Intelligence course.
### Contributors: Raymond Ng, Darryl Lim, Shaun Ho
### Attitude AI for Startup Drawmetrics

## To view the kaggle notebook:
https://www.kaggle.com/ray27th/facial-emotion-recognition-67-4

## Instructions to run code:
1. Install Docker Engine (https://docs.docker.com/engine/install/)
2. Clone Git Repository using HTTPS
3. Download the zip for additional files from Google Drive (https://drive.google.com/file/d/1b2RqB9Zn3oaxewEDFwpDXuXt2MqryM9N/view?usp=sharing)
4. Drag the contents of the zip file into /FYP-project-attitude-X
5. Open up command prompt
6. cd into /FYP-project-attitude-X
7. Run the following commands:
pip install -r requirements.txt
docker-compose up --build
8. To run the streamlit application:
streamlit run app.py

## To clear images:
docker system prune --all --volumes --force
