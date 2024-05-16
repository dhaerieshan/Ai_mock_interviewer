import streamlit as st
from mock import chatbot_tab
from coding import coding_tab
from evaluate import eva_tab

tab1, tab2 ,tab3= st.tabs(["Chatbot", "Coding Interview Practice", "Evaluate"])

with tab1:
    chatbot_tab()

with tab2:
    coding_tab()

with tab3:
    eva_tab()
