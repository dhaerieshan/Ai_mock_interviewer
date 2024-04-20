AI Mock Interview 
This project is an AI-driven mock interview platform designed to help freshers practice and prepare for interviews. The platform simulates real interview scenarios, evaluates responses, and provides feedback to improve the candidate's performance.

Description
The AI Mock Interview Platform utilizes advanced AI and speech processing technologies to create a realistic interview environment. It supports voice interactions where candidates can respond to questions verbally, and these responses are analyzed by the system to provide constructive feedback.

Features
Realistic Interview Simulation: Mimics actual interview scenarios to provide a real-life experience.
Voice Input and Response: Supports voice-based interactions, capturing and processing spoken responses.
Dynamic Questioning: The system dynamically adjusts the complexity and nature of questions based on the user's performance.
Feedback System: Offers detailed feedback on each session, including areas of strength and improvement suggestions *Feedback is generated in a doc file*.
Prerequisites
Before you begin, ensure you have met the following requirements:

You have Python 3.8+ installed on your machine.
You have access to the internet to install additional Python packages.
Installation
A step-by-step guide on how to get a development environment running:

Clone the repo:

git clone https://github.com/dhaerieshan/AI_Mock_Interview
Navigate to the project directory and install required packages:


pip install -r requirements.txt
Usage
Here's a quick example of how to run a mock interview session:

python
-------------------------------------------------------------------
from chatbot import Chatbot 

chatbot = Chatbot(position="Software Engineer") 

chatbot.start_conversation("John Doe")

-------------------------------------------------------------------
