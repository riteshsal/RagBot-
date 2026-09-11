from fastapi import FastAPI,UploadFile,File,Form,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import load_vectorstore
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from logger import logger


app=FastAPI(title="RagBot")

#allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def catch_exception_middleware(request:Request,call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500,content={"error":str(exc)})

@app.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"Received {len(files)} files, adding to Chroma")
        vectorstore = load_vectorstore(files)
        return {"message":"Files Processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500,content={"error":str(e)})
    
@app.post("/ask/")
async def ask_question(question:str=Form(...)):
    try:
        logger.info("user query:{question}")
        from langchain_chroma import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        from modules.load_vectorstore import PERSIST_DIR

        vectorstore=Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        )
        chain=get_llm_chain(vectorstore)
        result=query_chain(chain,question)
        logger.info("query succesful")
        return result
    except Exception as e:
        logger.exception("error processing question")
        return JSONResponse(status_code=500,content={"error":str(e)})


@app.get("/test")
async def test():
    return {"message":"Testing succesful.."}