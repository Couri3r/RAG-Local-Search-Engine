from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from .qa_system import RAGSystem
from contextlib import asynccontextmanager
import os
from .vector_store import build_index



ml_models = {}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI):

    try:
        ml_models["rag_system"] = RAGSystem()

    except Exception as e:
        logger.error("Failed to load")


    
    yield
        

app = FastAPI(lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class SearchQuery(BaseModel):
    query:str
    k: int = 4

class SearchResponse(BaseModel):
    answer:str
    sources:list[str]

class IndexedFilesResponse(BaseModel):
    files: list[str]


class DirectoryPath(BaseModel):
    directory_path: str

class ReindexResponse(BaseModel):
    message: str
    indexed_files: list[str]    

rag_system = None


@app.get("/")
def read_root():
    return {"status": "API is running"}


@app.post("/search", response_model=SearchResponse)
def search_documents(search_query: SearchQuery):
    rag_system = ml_models.get("rag_system")

    if not rag_system.index or not rag_system.metadata:
        return {
            "answer": "The search index is empty. Please use the sidebar to re-index a directory first.",
            "sources": []
        }
    

    result = rag_system.ask(query=search_query.query, k = search_query.k)
    return result


@app.get("/indexed-files")
def get_indexed_files():
    rag_system = ml_models.get("rag_system")

    


    all_source_paths = [chunk['source'] for chunk in rag_system.metadata]

    unique_paths = set(all_source_paths)

    unique_filenames = {os.path.basename(path) for path in unique_paths}

    sorted_files = sorted(list(unique_filenames))

    return({"files": sorted_files})


@app.post("/reindex",response_model=ReindexResponse)
def reindex_directory(path: DirectoryPath):

    directory = path.directory_path


    try:

        indexed_files = build_index(directory)

        if not indexed_files:

            raise HTTPException(status_code=404, detail=f"no proccessable files were found in directory: {directory}")

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    ml_models["rag_system"] = RAGSystem()

    return {
            "message": f"Successfully re-indexed {len(indexed_files)} files.",
            "indexed_files": indexed_files
        }   