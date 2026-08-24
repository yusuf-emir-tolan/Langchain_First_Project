from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from fastapi import FastAPI
from langserve import add_routes
load_dotenv()
model = ChatGroq(model="qwen/qwen3.6-27b",temperature=0.3)

parser = StrOutputParser()

systemprompt = "Translate the fallowing into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", systemprompt),("user","{text}")
    ]
)
app = FastAPI(
    title="Translate the following into {language}",
    description="Translate the following into {language}",
    version="0.0.1",

)
chain = prompt_template | model | parser
add_routes(
    app,
    chain,
    path= "/chain"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)