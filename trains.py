import random
from pydantic import BaseModel
from stations_dao import fetch_dislocations


# описание вагона
class Wagon(BaseModel):
    operdate: str  # дата операции; работы с вагоном
    train_num: int  # номер вагона
    dislocation: int  # текущая позиция вагона (совпадает с позиция поезда его несущего)
    destination: int  # пункт назначения вагона


# описание поезда
class Train(BaseModel):
    index: str  # индекс вагона
    num: str  # номер поезда
    departure: int  # пункт исходного отправления поезда
    destination: int  # пункт назначения поезда
    dislocation: int  # текущая позиция
    wagens: list  # список вагонов


# @unsed @deprecated
def find_all_trains_at_station_still_too_slow(station):
    """
Поиск поездов в данной станции

    :param station:
    :return:
    """
    print('!!!!')
    dislocations = fetch_dislocations()
    print(dislocations)

    wagons = {}
    for disl in dislocations:
        trainnum = disl[7]  # TRAINNUM
        wagons[trainnum] = []

    for disl in dislocations:
        wagnum = disl[0]  # WAGNUM
        operdate = disl[1]  # OPERDATE
        stdisl = disl[2]  # STDISL
        stdest = disl[3]  # STDEST
        trainnum = disl[7]  # TRAINNUM

        wagons[trainnum].append(Wagon(
            train_num=trainnum, operdate=operdate, num=wagnum, dislocation=stdisl, destination=stdest
        ))

    trains = {}
    for disl in dislocations:
        trainindex = disl[4]  # TRAININDEX
        departure = disl[5]  # DEPARTURE
        destination = disl[6]  # DESTINATION
        trainnum = disl[7]  # TRAINNUM

        trains[trainnum] = Train(
            index=trainindex,
            num=trainnum,
            departure=departure,
            destination=destination,
            dislocation=station,
            wagens=wagons[trainnum]
        )

    return trains.values()


def find_all_trains_at_station(station):

    return [
        random_train(station),
        random_train(station),
        random_train(station),
        random_train(station),
        random_train(station),
    ]


def random_train(station):
    num = str(random.randint(10, 30))
    departure = random.randint(10, 30)
    destination = random.randint(10, 30)
    return Train(
        index=f"{departure}-{num}-{destination}",
        num=num,
        departure=departure,
        destination=destination,
        dislocation=station,
        wagens=[
            Wagon(train_num=num, operdate='22-11-12', num=1, dislocation=station, destination=random.randint(10, 30)),
            Wagon(train_num=num, operdate='22-11-12', num=1, dislocation=station, destination=random.randint(10, 30)),
            Wagon(train_num=num, operdate='22-21-12', num=1, dislocation=station, destination=random.randint(10, 30)),
            Wagon(train_num=num, operdate='22-21-22', num=1, dislocation=station, destination=random.randint(10, 30)),
            Wagon(train_num=num, operdate='22-21-32', num=1, dislocation=station, destination=random.randint(10, 30)),
        ]
    )
