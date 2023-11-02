import streamlit as st

st.set_page_config(
    page_title="About Page",
    page_icon="👋",
)

st.write("# Welcome to Attitude-X! 👋")

st.sidebar.success("Select a Page above")

st.markdown(
    """
    Attitude-X, an AI solution, optimizes hiring processes by analyzing resumes. 
    It integrates cutting-edge NLP technologies and LLMs (Language Model Models) for this purpose.
    
    **Done by group 3A62 from Singapore Polytechnic DAAA FYP Year 2023**
    
    ### More about us:
    - Check out our [GitHub](https://github.com/27thRay/FYP-project-attitude-X)
    - Jump into our [Documentation](https://docs.streamlit.io)
    
    #### Contributors:
    - Raymond Loong Ng
    - Darryl Lim
    - Shaun Ho
"""
)