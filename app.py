import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd

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

    st.subheader("Look Up Your Gaming History")
    st.title("Get insights and statistics on your performance!")

    st.write(
        """
        Imagine having an all-seeing eye that reveals every move, every decision, 
    and every opportunity for improvement from your recent matches. With League Insights, 
    you gain access to a treasure trove of detailed statistics, strategic analysis, 
    and personalized recommendations, tailored exclusively to your gameplay style.
    """
    )


with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column: 
        st.header("Step into a world where data becomes your most valuable ally.")
        st.write(pd.read_csv('/Users/maxremme/Desktop/Programming/Code_Academy/Riot/player_stats/game_1.csv'))
        st.write("##")
        st.write(
            """
            _Uncover the secrets to your success, identify your strengths, 
            and pinpoint areas for growth. Dive deep into your match history, 
            relive epic battles, and dissect pivotal moments that turned the tides of victory. 
            Unearth the patterns, strategies, and champion synergies that set you apart from the rest_.
            """
        )
        
    with right_column:
        st_lottie(lottie_coding, height=500, key='coding')

