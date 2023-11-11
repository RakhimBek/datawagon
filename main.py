# pain and suffering

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from stations import find_paths
from stations import find_stations
from stations import find_all_stations

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


@app.get("/api/stations/path")
async def stations_path(start=134, end=155, candidates_constraint=3):
    return find_paths(int(start), int(end), int(candidates_constraint))


@app.get("/api/stations/net")
async def stations(left, top, right, down):
    return find_stations(float(left), float(top), float(right), float(down))


@app.get("/api/stations")
async def stations():
    return find_all_stations()


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080)
