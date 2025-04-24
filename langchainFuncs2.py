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

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-preview-04-17",
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# # prompts
# retrieval_prompt = PromptTemplate.from_template(
# '''
# Based on the following input: '{input_text}', create the appropriate query to filter and return results from a python dataframe (df.query()).
# The dataframe contains the following columns: '{col_vals}'. Only return the query string without any additional text.'''
# )
# retrieval_prompt = retrieval_prompt.partial(col_vals=(df.columns))

# # chain
# chain = retrieval_prompt | llm | StrOutputParser()
# # run
# user_input = {"input_text": "Please give me  the total sales in the month of January."}
# response = chain.invoke(user_input)
# print(response)



messages = [
    SystemMessage(content="You are an ecommerce database agent. [DATA]: " + df.values.tolist().__str__()),
    HumanMessage(content="Please tell me the revenue figures for January?")
]

response = llm.invoke(messages)
print("Full LLM Response: ", response)
print("LLM Response Content: ", response.content)