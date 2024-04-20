
from speech_service import SpeechService
from evaluation_service import EvaluationService
import os
from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()

class Chatbot:
    def __init__(self, azure_endpoint, api_key, api_version, position):
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.position = position
        self.evaluation_service = EvaluationService(api_key, api_version, azure_endpoint)
        self.speech_service = SpeechService()
        self.conversation_history = []
        self.qa_pairs = []

    def start_conversation(self, name):
        initial_greeting = f"Hi {name}, I'm here to conduct the interview for the {self.position} position. Start speaking when you're ready."
        self.speech_service.speak(initial_greeting)
        self.conversation_history.append({"role": "assistant", "content": initial_greeting})
        
        while True:
            print("Press 'Enter' to respond or 'Q' to quit...")
            user_choice = input()  # Capture user input

            if user_choice.lower() == 'q':
                print("Interview concluded.")
                break

            user_input = self.speech_service.listen_once()
            if user_input is None:
                print("No speech could be recognized. Please try speaking again.")
                continue  # Skip processing and go back to listening

            user_input = user_input.strip().lower()
            if user_input == 'quit':
                print("Interview concluded.")
                break

            response = self.generate_response(user_input)
            self.speech_service.speak(response)

    def generate_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        system_message = f"""As a training tool for the {self.position} role,imagine you are a project manager ask question that you will ask to a fresher for the resource you looking for in them.it is not a interviw for a project manager until it is stated explisitly in position. this mock interview is crafted to assist freshers in honing their interviewing skills. The exercises are specifically designed to align with what project managers look for in candidates for project roles.
            - **Questioning Style:** Simulate realistic interview scenarios by asking questions that a project manager might pose. Ensure your responses are concise to mirror a professional interview setting.
            - **Interactive Dialogue:** Encourage candidates to engage deeply with each topic through follow-up questions that require thoughtful responses, thereby deepening their understanding and ability to articulate their thoughts.
            - **Diverse Topics:** Cover a broad range of topics without repeating questions to ensure that candidates can demonstrate their versatility and depth of knowledge.
            - **Guided Responses:** Do not provide direct answers to the questions. Instead, guide candidates to think critically and formulate their responses. This method helps develop their problem-solving skills, which are crucial in project management.
            - **Constructive Feedback:** Point out discrepancies and areas for improvement in a gentle and supportive manner. Feedback should be constructive, aiming to build confidence and competence.
            - **Educational Tool:** Emphasize that this platform is a safe practice environment, not a real interview. The main goal is educational, helping candidates to prepare effectively for actual interviews with project managers.
            This training tool is not just about evaluation—it's a support system to prepare candidates for successful real-life interview scenarios in the {self.position} role.'no Resume',Dont number Question
            Candidate has no idea what the guideline is.
                            Ask me questions and wait for my answers. Do not write explanations.
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
            max_tokens=1000,
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
    

    def conduct_evaluation(self):
        evaluation = self.evaluation_service.evaluate_interview(self.qa_pairs)
        self.evaluation_service.save_evaluation_to_doc(evaluation)
        print("Evaluation completed and saved.")

if __name__ == "__main__":
    # Setup parameters (could also be loaded from env vars or a config file)
    name = input("Enter your name: ")
    position = input("Enter position: ")
    chatbot = Chatbot(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("API_VERSION"),
        position=position,
    )
    chatbot.start_conversation(name)
    chatbot.conduct_evaluation()
