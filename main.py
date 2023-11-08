# pain and suffering

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pane import concat

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
    return {"message": concat("Hello", ", World!")}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080)
