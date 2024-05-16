import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("API_VERSION")
)

def coding_tab():
    st.header("Coding Interview Practice")
    languages = ["Python", "JavaScript", "Java", "C#", "C++", "Ruby", "Go", "Swift", "Kotlin", "PHP"]
    difficulties = ["Basic", "Beginner", "Easy", "Intermediate", "Advanced", "Expert"]

    language = st.selectbox("Choose a language:", languages)
    difficulty = st.selectbox("Choose a difficulty level:", difficulties)

    if st.button("Generate Question"):
        question = generate_question(language, difficulty)
        st.write("Generated Question:")
        st.write(question)

    user_code = st.text_area("Enter your code for evaluation:")
    if st.button("Evaluate Code"):
        evaluation_result = evaluate_code(question, user_code, language)
        st.write("Evaluation Result:")
        st.write(evaluation_result)


def generate_question(language, difficulty):
    system_message = f"Create a single coding question of {difficulty.lower()} difficulty for the programming language {language}. The question should be specific to typical tasks and challenges relevant to this language. It must strictly adhere to the selected difficulty level and be directly applicable to {language}. Only one question is required."
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
    question = response.choices[0].message.content
    return question

def evaluate_code(previous_question, user_code, language):
    language = language.capitalize()
    prompt = f"Question:\n{previous_question}\n\nAnswer in {language}:\n{user_code}\n\nEvaluate the above code for correctness and suggest improvements if any."
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
    evaluation = response.choices[0].message.content
    return evaluation
