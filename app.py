# !pip install -U google-genai
# !pip install -q gradio

#importing necessary packages
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
import gradio as gr

#uses client class to create an instance (for interacting with gemini api)
load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))


# system prompt personalities to send instructions to LLM to behave like
personalities = {
  "Friendly":
  "You are a friendly, enthusiastic, and highly encouraging Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding",
  "Academic":
  "You are a strictly academic, highly detailed, and professional university Professor. Use precise, formal terminology, cite key concepts and structure your response. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding"
}

#uses client object for communicating to gemini LLM

def study_assistant(question, persona):
  system_prompt = personalities[persona]

  response = client.models.generate_content(
      model = "gemini-2.5-flash",
      config = types.GenerateContentConfig(
          system_instruction = system_prompt,
          temperature = 0.4,
          max_output_tokens = 2000
      ),
      contents = question
  )

  return response.text 

#building UI to Above LLM application using Pyhton package Gradio

demo = gr.Interface(
    fn = study_assistant,
    inputs = [gr.Textbox(lines = 3, placeholder = "Ask a Question", label="Question"),
              gr.Radio(choices = list(personalities.keys()), value = "Friendly", label = "personalities")],
    outputs = gr.Textbox(lines = 7, label = "Response"),
    title = "Study Assistant",
    description = "Ask a question and get an ans from your AI study assistant with a choosen personality"
)

demo.launch(debug=True)
