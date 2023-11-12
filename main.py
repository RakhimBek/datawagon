# pain and suffering

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import DEBUG
from settings import HOST
from settings import PORT
from settings import PROJECT_NAME
from stations import find_all_stations
from stations import find_history
from stations import find_paths
from stations import find_stations
from trains import find_all_trains_at_station

app = FastAPI(
    title=PROJECT_NAME,
    debug=DEBUG,
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
    """
Возможные пути от стартовой до конечной станции
    :param start: стартовая станция
    :param end: конечная станция
    :param candidates_constraint: максимальное количество кандидатов
    :return:
    """
    return find_paths(int(start), int(end), int(candidates_constraint))


@app.get("/api/stations/net")
async def stations(left, top, right, down):
    """
Все станции в данном квадрате
    :param left:
    :param top:
    :param right:
    :param down:
    :return:
    """
    return find_stations(float(left), float(top), float(right), float(down))


@app.get("/api/stations")
async def stations():
    """
Все возможные станции
    :return: все возможный станции
    """
    return find_all_stations()


@app.get("/api/stations/hostory")
async def stations(wagon_id):
    """
Пройденные маршрут вагона
    :return: все возможный станции
    """
    return find_history(int(wagon_id))


@app.get("/api/trains")
async def stations(station, operdate='22-11-12'):
    """
Все поезда на данной станции
    :param station: номер станций
    :return: все поезда на данной станций
    """
    return find_all_trains_at_station(int(station), operdate)


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
