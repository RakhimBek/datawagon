# pain and suffering

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from stations import find

app = FastAPI(
    title='wishfulmap',
    debug=True,
    version='1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/api/stations")
async def root():
    result = find(7741, 22308)
    print(result)
    return result


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080)
