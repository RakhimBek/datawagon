import random
from pydantic import BaseModel


# описание вагона
class Wagen(BaseModel):
    operdate: str  # дата операции; работы с вагоном
    num: int  # номер вагона
    destination: int  # пункт назначения вагона


# описание поезда
class Train(BaseModel):
    index: int  # индекс вагона
    num: int  # номер вагона
    departure: int  # пункт исходного отправления поезда
    destination: int  # пункт назначения поезда
    dislocation: int  # текущая позиция
    wagens: list  # список вагонов


def find_all_trains_at_station(station):
    return [
        random_train(station),
        random_train(station),
        random_train(station),
        random_train(station),
        random_train(station),
    ]


def random_train(station):
    return Train(
        index=random.randint(10, 30),
        num=random.randint(10, 30),
        departure=random.randint(10, 30),
        destination=random.randint(10, 30),
        dislocation=station,
        wagens=[
            Wagen(operdate='22-11-12', num=1, destination=random.randint(10, 30)),
            Wagen(operdate='22-11-12', num=1, destination=random.randint(10, 30)),
            Wagen(operdate='22-21-12', num=1, destination=random.randint(10, 30)),
            Wagen(operdate='22-21-22', num=1, destination=random.randint(10, 30)),
            Wagen(operdate='22-21-32', num=1, destination=random.randint(10, 30)),
        ]
    )
