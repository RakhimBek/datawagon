import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pydantic import BaseModel


def show(network, graph):
    network.draw(graph, pos=nx.spring_layout(graph), node_size=2)
    plt.savefig("Graph.png", format="PNG")


# disl_hackaton.xlsx
# PEREGON_HACKATON.xlsx
# STATION_COORDS_HACKATON.xlsx


# path='~/Downloads/STATION_COORDS_HACKATON.xlsx'

# class Edge:
#    def __init__(self, start, end):
#        self.start = start
#        self.end = end
#
#    def __eq__(self, other):
#        return self.start == other.end and self.end == other.start
#
#    def __hash__(self):
#        return hash(tuple(sorted(self.__dict__.items())))


class Station(BaseModel):
    id: int
    latitude: float
    longitude: float


class Item(BaseModel):
    start: Station
    end: Station
    length: float


def find(start_station_id, end_station_id):
    # todo: setting file

    # tood: to database
    stations_path = '~/Downloads/STATION_COORDS_HACKATON.xlsx'
    peregon_path = '~/Downloads/PEREGON_HACKATON.xlsx'

    stations = {}
    with pd.ExcelFile(stations_path) as xls:
        # for sheet_name in xls.sheet_names:
        #    print(sheet_name)

        stations_df = pd.read_excel(xls, "Sheet 1")
        for index, row in stations_df.iterrows():
            station_id = row['ST_ID']
            latitude = row['LATITUDE']
            longitude = row['LONGITUDE']
            stations[station_id] = (latitude, longitude)

    # todo: write data to database
    with pd.ExcelFile(peregon_path) as xls:
        # for sheet_name in xls.sheet_names:
        #    print(sheet_name)

        df = pd.read_excel(xls, "Sheet 1")

        # graph = nx.DiGraph()
        graph = nx.Graph()
        ind = 0
        # edges = set()
        for index, row in df.iterrows():
            start = row['START_CODE']
            end = row['END_CODE']
            length = row['LEN']

            # print(f"{start} - {end}")
            # edge = Edge(start, end)
            # if edges.__contains__(edge):
            #    pass
            # else:
            #    edges.add(edge)

            # if ind < 100:
            ind += 1
            graph.add_edge(start, end, len=length)

        try:
            edged_paths = []
            for simple_path in nx.all_simple_paths(graph, source=start_station_id, target=end_station_id):
                edged_path = []
                left = simple_path[0]
                for right in simple_path[1:]:
                    # print(graph.get_edge_data(left, right))
                    start_station = stations.get(left)
                    end_station = stations.get(right)
                    edged_path.append(Item(
                        start=Station(id = left, longitude=start_station[0], latitude=start_station[1]),
                        end=Station(id = right, longitude=end_station[0], latitude=end_station[1]),
                        length=length
                    ))

                    left = right
                edged_paths.append(edged_path)

            return edged_paths

        except Exception as e:
            print(f"No paths. {e}")
            return {}


if __name__ == "__main__":
    find(7741, 22294)
