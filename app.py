import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="My Webpage", page_icon=":sparkles:", layout="wide")

def load_url(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    return resp.json()





#Load Assets

lottie_coding = load_url("https://assets9.lottiefiles.com/packages/lf20_8rs5Fb08t9.json")
#https://assets10.lottiefiles.com/packages/lf20_dews3j6m.json
#https://assets8.lottiefiles.com/packages/lf20_r2rsf2yk.json
#https://assets9.lottiefiles.com/packages/lf20_8rs5Fb08t9.json

#Header Section
with st.container():

    st.subheader("Get insights and statistics on your performance")
    st.title("Look up Your Gaming History")
    st.write("Imagine having an all-seeing eye that reveals every move, every decision, and every opportunity for improvement from your recent matches. With League Insights, you gain access to a treasure trove of detailed statistics, strategic analysis, and personalized recommendations, tailored exclusively to your gameplay style.")


with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column: 
        st.header("What You Will Get!")
        st.write()
        st.write("##")
        st.write(
            """
            Most recent 20 Matches analysed using in depth statistical analysis on:
            - Kills
            - Deaths
            - Vision Score
            - etc  
            """
        )

    with right_column:
        st_lottie(lottie_coding, height=500, key='coding')

