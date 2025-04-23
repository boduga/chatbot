import streamlit as st
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Use your Gemini API key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]

# Initialize the chat model
chat = ChatGoogleGenerativeAI(
    model="gemini-pro",  # Gemini 1.5 Pro; use "gemini-1.5-pro" if supported
    temperature=0.7,
    google_api_key=api_key
)

# UI
st.title("Gemini Chat with LangChain + Streamlit")

user_input = st.text_input("Ask Gemini something:")

if user_input:
    response = chat([HumanMessage(content=user_input)])
    st.write("Gemini says:")
    st.write(response.content)