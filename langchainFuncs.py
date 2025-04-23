import streamlit as st
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Use your Gemini API key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]

# Initialize the chat model
chain = ChatGoogleGenerativeAI(
    model="gemini-pro",  # Gemini 1.5 Pro; use "gemini-1.5-pro" if supported
    temperature=0.7,
    google_api_key=api_key
)
