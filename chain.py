from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatOllama(model="llama3:8b")
llm.invoke("What is stock?")

prompt1 = ChatPromptTemplate.from_template("[{korean_input}] translate the question into English. Don't say anything else, just translate it.")
chain1 = (
    prompt1 
    | llm 
    | StrOutputParser()
)
message1 = chain1.invoke({"korean_input": "주식이 뭐야?"})
print(f'message1: {message1}') # What is a stock?

# 두번째 체인
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, professional assistant. answer the question in Korean"),
    ("user", "{input}")
])
chain2 = (
    {"input": chain1}
    | prompt2
    | llm
    | StrOutputParser()
)
message2 = chain2.invoke({"korean_input": "주식이 뭐야?"})
print(f'message2: {message2}')