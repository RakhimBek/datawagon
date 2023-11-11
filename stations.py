import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pydantic import BaseModel

from stations_dao import fetch_stations
from stations_dao import fetch_stations_net


def show(network, graph):
    network.draw(graph, pos=nx.spring_layout(graph), node_size=2)
    plt.savefig("Graph.png", format="PNG")


class Station(BaseModel):
    id: int
    latitude: float
    longitude: float


class Edge(BaseModel):
    start: Station
    end: Station
    distance: float


def find(start_station_id, end_station_id):
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
        graph.add_edge(start, end, distance=distance)

    try:
        edged_paths = []
        for simple_path in nx.all_simple_paths(graph, source=start_station_id, target=end_station_id):
            edged_path = []
            left = simple_path[0]
            for right in simple_path[1:]:
                distance = graph.get_edge_data(left, right)
                edged_path.append(Edge(
                    start=stations.get(left),
                    end=stations.get(right),
                    distance=distance['distance']
                ))

                left = right
            edged_paths.append(edged_path)

        return edged_paths

    except Exception as e:
        print(f"No paths. {e}")
        return {}


if __name__ == "__main__":
    find(7741, 22294)
