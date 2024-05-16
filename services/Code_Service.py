import streamlit as st
from openai import AzureOpenAI
import os

def coding_tab():
    # Ensure these are defined inside the function or passed appropriately
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("API_VERSION")
    )

    def generate_question(language, difficulty):
        system_message = f"Create a coding question of {difficulty} difficulty for {language}."
        messages = [{"role": "system", "content": system_message}]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].message.content

    def evaluate_code(previous_question, user_code, language):
        prompt = f"Question:\n{previous_question}\n\nAnswer in {language}:\n{user_code}\n\nEvaluate the above code."
        messages = [{"role": "system", "content": prompt}]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].message.content

    st.subheader('Generate and Evaluate Coding Questions')

    languages = ["Python", "JavaScript", "Java", "C#", "C++", "Ruby", "Go", "Swift", "Kotlin", "PHP"]
    difficulties = ["Basic", "Beginner", "Easy", "Intermediate", "Advanced", "Expert"]
    language = st.selectbox("Choose a language:", languages)
    difficulty = st.selectbox("Choose a difficulty level:", difficulties)

    if st.button("Generate Question"):
        question = generate_question(language, difficulty)
        st.session_state.question = question  # Save question in session state to use later in evaluation
        st.write("Generated Question:")
        st.write(question)

    if 'question' in st.session_state and st.session_state.question:
        user_code = st.text_area("Enter your code for evaluation:")
        if st.button("Evaluate Code"):
            evaluation_result = evaluate_code(st.session_state.question, user_code, language)
            st.write("Evaluation Result:")
            st.write(evaluation_result)
