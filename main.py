from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 특정 도메인으로 제한하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 모델 인스턴스 생성
llm = ChatOllama(model="internlm2:latest")

# Pydantic 모델 정의
class InputMessage(BaseModel):
    english_input: str

# 첫 번째 체인 설정
prompt1 = ChatPromptTemplate.from_template("[{korean_input}] translate the question into English. Don't say anything else, just translate it.")
chain1 = (
    prompt1 
    | llm 
    | StrOutputParser()
)

# 두 번째 체인 설정
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a kind mathmetic teacher. "),
    ("user", "{input}")
])
chain2 = (
    prompt2
    | llm 
    | StrOutputParser()
)

# HTML 페이지 렌더링 엔드포인트
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API 엔드포인트 정의
@app.post("/translate")
async def translate(input_message: InputMessage):
    try:
        # 첫 번째 체인 처리
        # translated_message = chain1.invoke({"korean_input": input_message.korean_input})
        
        # 두 번째 체인 처리
        final_message = chain2.invoke({"input": input_message.english_input})
        
        return {
            "final_message": final_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


