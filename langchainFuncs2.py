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

# prompts
retrieval_prompt = PromptTemplate.from_template(
    '''
Based on the following input: '{input}', create the appropriate query to filter and return results from a python dataframe (df.query()).
The dataframe contains the following columns: '{columns}'. Only return the query string without any additional text.
'''
)
retrieval_prompt = retrieval_prompt.partial(
    columns=(df.columns)
)

#chain
retrieval_prompt | llm | StrOutputParser()

