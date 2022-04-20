from genHint import graph, genClues, random
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json

cnfg = {
    "HOST":"localhost",
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

@app.get("/{size}/{ratio}")
async def getBoard(size:str, ratio:float):
    row, column = map(int, size.split("-"))
    g = graph((row,column))
    random(g, n=(row*column*ratio))
    pk = {
            "numberOfRows": g.size[0],
            "numberOfCols": g.size[1],
            "clues": genClues(g)
        }
    return JSONResponse(status_code=200, content=pk)

@app.get("/vector/{size}/{ratio}")
async def getBoard(size:str, ratio:float):
    row, column = map(int, size.split("-"))
    g = graph((row,column))
    random(g, n=(row*column*ratio))
    pk = {
            "numberOfRows": g.size[0],
            "numberOfCols": g.size[1],
            "clues": genClues(g)
        }
    String = "Vector(\n"
    for i, clue in enumerate(pk['clues']):
        String += f" ({clue['position']['x']}, {clue['position']['y']}, {clue['size']}){',' if i < len(pk['clues'])-1 else ''}\n"
    String += ")"
    print(String)
    return String
if __name__ == "__main__":
    uvicorn.run("main:app", host=f'{cnfg["HOST"]}', port=int(cnfg["PORT"]), reload=False)