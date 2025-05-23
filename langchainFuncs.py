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
import pandas

chain = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-preview-04-17",
    api_key=st.secrets["GOOGLE_API_KEY"]
)

revenueData= '''
January: $8,520.50
February: $9,150.75
March: $11,200.30
April: $10,880.15
May: $12,550.90
June: $13,100.40
July: $12,850.65
August: $14,700.80
September: $16,300.20
October: $18,950.55
November: $25,400.70
December: $31,750.95
'''

messages = [
    SystemMessage(content="You are an ecommerce database agent. [DATA]: " + revenueData),
    HumanMessage(content="Please tell me the revenue figures for August?")
]

response = chain.invoke(messages)
print("Full LLM Response: ", response)
print("LLM Response Content: ", response.content)

