import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith tracking
os.environ['LANGSMITH_API_KEY']=os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_TRACING']="true"
os.environ["LANGSMITH_PROJECT"]="Q&A Chatbot with OPENAI"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful user. Please response to the user queries"),
        ("user","Question{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    llm=ChatOpenAI(model=llm, api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


## Title of the app
st.image("chatbot.png", width=100)
st.title("💬 Chatbot by Elis")
st.subheader("Q&A Chatbot with OpenAI")

## Sidebar Settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your OpenAI API Key", type="password")

## Drop down
llm=st.sidebar.selectbox("Select an OpenAI Model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

## Adjust sliders
temperature=st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens=st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=70)

## Main interface
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")    