# This is a simple example of using LangChain with Google Gemini to query a database
# and retrieve information about revenue figures for an ecommerce business.
# It uses the LangChain library to create a chain of messages and invoke the model.

# Import necessary libraries
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda, RunnablePassthrough
import pandas as pd


df = pd.read_csv("100-trans.csv")
print(df.head())


llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-preview-04-17",
    api_key=st.secrets["GOOGLE_API_KEY"]
)

