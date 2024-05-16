import streamlit as st
from services.speech_service import SpeechService
from services.chatbot_service import Chatbot
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def chatbot_tab():
    st.header("Chatbot Interaction")
    try:
        speech_service = SpeechService(
            speech_key=os.getenv("SPEECH_API_KEY"),
            service_region=os.getenv("SPEECH_SERVICE_REGION")
        )
        chatbot = Chatbot(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("API_VERSION"),
            position="",
            speech_service=speech_service
        )
    except Exception as e:
        st.error(f"Failed to initialize the services: {str(e)}")
        st.stop()

    # Streamlit User Interface
    st.title('Chatbot Interview System')

    if 'qa_pairs' not in st.session_state:
        st.session_state['qa_pairs'] = []

    name = st.text_input("Enter your name:")
    position = st.text_input("Enter the position you are applying for:")

    if st.button("Start Conversation") and name and position:
        chatbot.position = position
        initial_message = chatbot.start_conversation(name)
        speech_service.speak(initial_message)
        st.session_state.qa_pairs.append((initial_message, ""))  # Speak out the initial message
        st.write(initial_message)  # Display the initial greeting

    # Listen button
    if st.button('Listen'):
        user_input = speech_service.listen_once()  # Assumes this method returns recognized text
        if user_input:
            response = chatbot.generate_response(user_input)
            if st.session_state.qa_pairs:
                last_question, _ = st.session_state.qa_pairs[-1]
                st.session_state.qa_pairs[-1] = (last_question, user_input)
            st.write(f"You said: {user_input}")
            st.write(f"Interviewer: {response}")
            speech_service.speak(response)
            st.session_state.qa_pairs.append((response, ""))
        else:
            st.write("I didn't catch that. Please try speaking again.")

    # Quit Interview button
    if st.button("Clear Interview"):
        st.write("Interview concluded.")
        st.session_state.qa_pairs = [] 
       