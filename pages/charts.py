##Importing libraries
import os
import sys
import pandas as pd
import altair as alt
import streamlit as st
from st_pages import hide_pages
import plotly.figure_factory as ff
from utility.loadcss import local_css
from streamlit_extras.switch_page_button import switch_page

##Importing Functions
from database import get_ovr_score_desc

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

#Hide pages after login
hide_pages(["Login"])
local_css('./docs/static/style.css')

#Logout Button
logout = st.sidebar.button("Logout")
if logout:
    switch_page('Login')

##Start of Page
st.title("Charts Page :chart_with_upwards_trend:")

#Get database data for charts
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
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X(option),
    y=alt.Y('name').sort('-x'),
    color='name',
).interactive()

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Altair theme.
    st.altair_chart(chart, theme=None, use_container_width=True)


###Score Distribution Plot
st.markdown(
    """
    ##### Score Distribution Plot:
    """
)
##Create the distplot with a cleaned 'overall_score' column
if len(df) > 2:
    dist_data = df.set_index('name')[option]
    labels = ['Score Distribution']
    fig = ff.create_distplot([dist_data], labels, bin_size=[1], show_curve=True)

    #Plot
    st.plotly_chart(fig)
else:
    st.error('Make sure table has at least 2 applicants!',icon='🚩')