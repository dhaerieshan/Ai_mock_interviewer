import os
import base64
from dotenv import load_dotenv
import streamlit as st
from services.evaluation_service import EvaluationService
    

# Load environment variables
load_dotenv()

# Initialize the evaluation service
evaluation_service = EvaluationService(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("API_VERSION")
)

def get_binary_file_downloader_html(filename):
    """Generate HTML download link for the given filename stored on the server."""
    with open(filename, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Word file</a>'
    return href

def eva_tab():
    st.title("Interview Evaluation Generator")

    if "qa_pairs" in st.session_state:
        valid_qa_pairs = [pair for pair in st.session_state.qa_pairs if pair[1].strip()]  # Filter pairs to include only those with non-empty answers

        if valid_qa_pairs:
            st.header("Review and Evaluate Questions and Answers")
            for i, (question, answer) in enumerate(valid_qa_pairs):
                st.text(f"Question {i+1}: {question}")
                st.text_area(f"Answer {i+1}:", value=answer, height=100)

            if st.button("Evaluate"):
                evaluation = evaluation_service.evaluate_interview(st.session_state.qa_pairs)
                filename = "interview_evaluation.docx"  # Define a filename for the saved report
                evaluation_service.save_evaluation_to_doc(evaluation, filename)  # Assuming this function saves the evaluation to a doc file
                st.success("Evaluation Generated Successfully!")
                st.subheader("Evaluation:")
                #st.write(evaluation)
                # Generate and display download link
                st.markdown(get_binary_file_downloader_html(filename), unsafe_allow_html=True)
        else:
            st.error("No valid QA pairs to evaluate. Please conduct an interview and ensure questions are answered.")
    else:
        st.error("No QA pairs loaded. Please conduct an interview in the chatbot tab first.")
