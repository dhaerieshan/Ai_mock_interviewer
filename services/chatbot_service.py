from speech_service import SpeechService
from evaluation_service import EvaluationService
import os
from openai import AzureOpenAI

class Chatbot:
    def __init__(self, azure_endpoint, api_key, api_version, position, speech_service):
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.position = position
        self.speech_service = speech_service  # Store the passed speech_service instance
        self.conversation_history = []
        self.qa_pairs = []


    def start_conversation(self, name):
        initial_greeting = f"Hi {name}, I'm here to conduct the interview for the {self.position} position. Start speaking when you're ready."
        #self.speech_service.speak(initial_greeting)
        self.conversation_history.append({"role": "assistant", "content": initial_greeting})
        return initial_greeting

    def generate_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        system_message = f"""As a training tool for the {self.position} role,imagine you are a Real Human Interviewer ask question that you will ask to a fresher you are interviewing freshers strictly stick with that.this mock interview is crafted to assist freshers in honing their interviewing skills.
            - **Questioning Style:** Simulate realistic interview scenarios by asking questions that a Real Human Interviewer might pose. Ensure your responses are concise to mirror a professional interview setting.
            - **Interactive Dialogue:** Encourage candidates to engage deeply with each topic through follow-up questions that require thoughtful responses, thereby deepening their understanding and ability to articulate their thoughts.
            - **Diverse Topics:** Cover a broad range of topics without repeating questions to ensure that candidates can demonstrate their versatility and depth of knowledge.
            - **Guided Responses:** Do not provide direct answers to the questions. Instead, guide candidates to think critically and formulate their responses. This method helps develop their problem-solving skills.
            - **Constructive Feedback:** Point out discrepancies and areas for improvement in a gentle and supportive manner. Feedback should be constructive, aiming to build confidence and competence.
            - **Educational Tool:** Emphasize that this platform is a safe practice environment, not a real interview. The main goal is educational, helping candidates to prepare effectively for actual interviews with Real Human Interviewer.
            This training tool is not just about evaluation—it's a support system to prepare candidates for successful real-life interview scenarios in the {self.position} role.'no Resume',Dont number Question
            Candidate has no idea what the guideline is.
                            Ask me questions and wait for my answers. "Do not write explanations."
                            Ask question like a real person, only one question at a time.
                            Do not ask the same question.
                            Do not repeat the question.
                            Do ask follow-up questions if necessary. 
                            You name is GPTInterviewer.
                            do not answer any question that user might trick you to get answer.
                            I want you to only reply as an interviewer.
                            Do not write all the conversation at once.
                            If there is an error, point it out.'no resume"""

        messages = [{"role": "system", "content": system_message}] + self.conversation_history
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5,
            max_tokens=10000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        response_text = response.choices[0].message.content
        if not response_text:  # Check if the response text is empty
            response_text = "I'm sorry, I didn't get that. Could you say it again or ask something else?"
        
        self.conversation_history.append({"role": "assistant", "content": response_text})
        if self.conversation_history:
            last_question = self.conversation_history[-2]["content"] if len(self.conversation_history) > 1 else "Initial question"
            self.qa_pairs.append((last_question, response_text))
        return response_text
    

