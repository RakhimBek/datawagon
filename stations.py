import random
from functools import reduce

import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel

from stations_dao import fetch_stations
from stations_dao import fetch_stations_net


def show(network, graph):
    network.draw(graph, pos=nx.spring_layout(graph), node_size=2)
    plt.savefig("Graph.png", format="PNG")

# описание станции
class Station(BaseModel):
    id: int  # идентификатор станции
    latitude: float  # широта
    longitude: float  # долгота


# ребро
class Edge(BaseModel):
    start: Station  # стартовая станция
    end: Station  # станция прибытия
    distance: float  # расстояние между станциями в км


# todo: broken fixme!
def find_stations(left, top, right, down):
    stations = {}
    for row in fetch_stations():
        station_id = row[0]
        latitude = row[1]
        longitude = row[2]
        if is_inside(left, top, right, down, longitude, latitude):
            stations[station_id] = Station(id=station_id, longitude=float(longitude), latitude=float(latitude))

    edges = []
    for row in fetch_stations_net():
        start_id = row[0]
        end_id = row[1]
        # todo: make sql instead of this
        if stations.keys().__contains__(start_id) and stations.keys().__contains__(end_id):
            edges.append(Edge(start=stations.get(start_id), end=stations.get(end_id), distance=row[2]))


def find_all_stations():
    """
Получить список сех станции
    :return:
    """
    stations = []
    for row in fetch_stations():
        station_id = row[0]
        latitude = row[1]
        longitude = row[2]
        if longitude != None and latitude != None:
            stations.append(Station(id=station_id, longitude=float(longitude), latitude=float(latitude)))

    return stations


def find_history(wagon_id):
    """
Получить список сех станции
    :return:
    """
    stations = []
    for i in range(2, 10):
        stations.append(Station(
            id=random.randint(10, 20),
            longitude=float(random.random() * i),
            latitude=float(random.random() * i)
        ))

    return stations


# left, right - longitude
# top, down - latitude
def is_inside(left, top, right, down, point_longitude, point_latitude):
    return point_longitude != None and point_latitude != None and left > point_longitude and point_longitude < right and point_latitude > down and point_latitude < top;


def find_paths(start_station_id, end_station_id, paths_constraint):
    """
Поиск возможных путей между двумя станциями
    :param start_station_id: стартовая станция
    :param end_station_id: конечная станция
    :param paths_constraint: максимальное число маршрутов для поиска
    :return: коллекция маршрутов
    """
    stations = {}
    for row in fetch_stations():
        station_id = row[0]
        latitude = row[1]
        longitude = row[2]
        if latitude != None and longitude != None:
            stations[station_id] = Station(id=station_id, longitude=float(longitude), latitude=float(latitude))
        else:
            print(f"failed to init station: {station_id}")

    graph = nx.Graph()
    for row in fetch_stations_net():
        start = row[0]
        end = row[1]
        distance = row[2]
        if (start in stations.keys() and end in stations.keys()):
            graph.add_edge(start, end, distance=distance)

    try:
        edged_paths = []
        for simple_path in nx.all_simple_paths(graph, source=start_station_id, target=end_station_id):
            edged_path = []
            left = simple_path[0]
            for right in simple_path[1:]:
                distance = graph.get_edge_data(left, right)
                start = stations.get(left)
                end = stations.get(right)

                if start != None and end != None:
                    edged_path.append(Edge(
                        start=start,
                        end=end,
                        distance=distance['distance']
                    ))
                else:
                    print(f"Impossible! {left}|{start} - {end}")

                left = right

            edged_paths.append({
                "stations": edged_path,
                "distance": reduce(lambda l, r: l + r.distance, edged_path, 0)
            })

            if len(edged_paths) >= paths_constraint:
                return edged_paths

        return edged_paths

    except Exception as e:
        print(f"No paths. {e}")
        return {}


# Для нахождения вершин с множеством различных путей
def find_plural_paths():
    stations = set()
    for row in fetch_stations():
        station_id = row[0]
        stations.add(station_id)

    graph = nx.Graph()
    ids = set()

    for row in fetch_stations_net():
        start = row[0]
        end = row[1]

        if (start in stations and end in stations):
            ids.add(start)
            ids.add(end)
            graph.add_edge(start, end)

    for left in ids:
        for right in ids:
            paths = list(nx.all_simple_paths(graph, source=left, target=right))
            if len(paths) > 7:
                print(f"--> {left} -- {right}")
                break


if __name__ == "__main__":
    find_plural_paths()
