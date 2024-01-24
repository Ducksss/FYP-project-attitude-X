##Importing libraries
import os
import sys
import pandas as pd
import altair as alt
import streamlit as st
from st_pages import hide_pages
import plotly.figure_factory as ff
from utility.classes import dataProcessor
from streamlit_extras.switch_page_button import switch_page
from extra_streamlit_components import CookieManager

##Importing Functions
from database import get_ovr_score_desc

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

dataprocessor = dataProcessor()

dataprocessor.local_css()

cookie_manager = CookieManager()
email = cookie_manager.get(cookie='email')

#Hide Pages after login
if email == 'admin':
    hide_pages(["Login","Chatbot"])
else:
     hide_pages(["Login","Charts","Video","Home","Edit"])

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    cookie_manager.delete('email')
    switch_page('Login')

##Start of Page
st.title("Charts Page :chart_with_upwards_trend:")

#Get database data for charts
if len(get_ovr_score_desc(0.4,0.4,0.2)) > 0:
    if 'default_table' in st.session_state:
        df = st.session_state.default_table
else:
    df = get_ovr_score_desc(0.4,0.4,0.2)

#Altair Bar Chart Ranking Plot
# Convert the 'overall_score' column to numeric (float) type
# df['overall_score'] = pd.to_numeric(df['overall_score'], errors='coerce')
# df['technical_skills'] = pd.to_numeric(df['technical_skills'], errors='coerce')
# df['soft_skills'] = pd.to_numeric(df['soft_skills'], errors='coerce')
# df['languages'] = pd.to_numeric(df['languages'], errors='coerce')

st.markdown(
    """
    ##### Top 20ᵗʰ Percentile:
    """
)

if len(df) >= 2:
    df = df[["_id","name","overall_score","technical_skills","soft_skills","languages","email","contact_number"]]
    st.dataframe(df.sort_values('overall_score', ascending = False ).iloc[:round(20/100 * (len(df)+1))],hide_index=True)
else:
    st.error('Make sure table has at least 2 applicants!',icon='🚩')


option="overall_score"

option = st.selectbox(
    "What skill would you like the charts to be based on?",
    ("overall_score", "technical_skills", "soft_skills", "languages"),
    placeholder="Select skill..."
)

st.markdown(
    """
    ##### Bar Chart Ranking:
    """
)
#Sort in descending overall_score
if len(df) >= 1:
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(option),
        y=alt.Y('name').sort('-x'),
        color='name',
    ).interactive()

    st.altair_chart(chart, theme="streamlit", use_container_width=True)

else:
    st.error('Make sure table has at least 1 applicant!',icon='🚩')

###Score Distribution Plot
st.markdown(
    """
    ##### Score Distribution Plot:
    """
)
##Create the distplot with a cleaned 'overall_score' column
if len(df) >= 2:
    dist_data = df.set_index('name')[option]
    labels = ['Score Distribution']
    fig = ff.create_distplot([dist_data], labels, bin_size=[1], show_curve=True)

    #Plot
    st.plotly_chart(fig)
else:
    st.error('Make sure table has at least 2 applicants!',icon='🚩')