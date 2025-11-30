from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", groq_api_key=groq_api_key)

#Creating Prompt Template
system_template="Translate the following into {language}:"
prompt_template=ChatPromptTemplate.from_messages([
    ("system",system_template),
    ("user","{user_text}")
])
 
parser = StrOutputParser()

chain=prompt_template|model|parser

#App definition

app=FastAPI(title="Langchain server",
            version="1.0",
            description="demo of langchain runnable interfaces")

#Adding chain routes
add_routes(
    app,
    chain,
    path='/chaintu'
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)