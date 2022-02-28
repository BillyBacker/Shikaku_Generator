from genHint import graph, genClues, random
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json

cnfg = {
    "HOST":"0.0.0.0",
    "PORT":"9001"
}

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{size}")
async def getBoard(size:str):
    row, column = map(int, size.split("-"))
    g = graph((row,column))
    random(g)
    pk = {
            "numberOfRows": g.size[0],
            "numberOfCols": g.size[1],
            "clues": genClues(g)
        }
    return JSONResponse(status_code=200, content=pk)

if __name__ == "__main__":
    uvicorn.run("main:app", host=f'{cnfg["HOST"]}', port=int(cnfg["PORT"]), reload=False)