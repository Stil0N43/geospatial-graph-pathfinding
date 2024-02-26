import geopandas as gpd
from shapely.geometry import Point

from classes.graph import Graph


def road_class_to_weight(rclass: str) -> float:
    speed_limit: float = 140

    if rclass == "A" or rclass == "I":  # autostrada lub inna
        speed_limit = 140
    elif rclass == "S":  # ekspresowa
        speed_limit = 130
    elif rclass == "GP":  # główna ruchu przyspieszonego
        speed_limit = 110
    elif rclass == "G":  # główna
        speed_limit = 100
    elif rclass == "Z":  # zbiorcza
        speed_limit = 80
    elif rclass == "L":  # lokalna
        speed_limit = 60
    elif rclass == "D":  # zbiorcza
        speed_limit = 30

    return speed_limit

def elements_from_shp(path: str):
    shp = gpd.read_file(path)
    shp = shp.set_crs("EPSG:2180", allow_override=True)
    shp['length'] = shp.length
    shp["speed_limit"] = shp['klasaDrogi'].apply(road_class_to_weight)
    shp['first_pnt'] = shp.apply(lambda x: x['geometry'].coords[0], axis=1)
    shp['last_pnt'] = shp.apply(lambda x: x['geometry'].coords[-1], axis=1)
    shp_edges = shp[['first_pnt', 'last_pnt', 'length', 'speed_limit']].copy()
    edges_geometry = shp['geometry'].copy()
    edges = shp_edges.values.tolist()

    nodes = []
    for i, edge in enumerate(edges):
        start = edge[0]
        end = edge[1]
        if start not in nodes:
            nodes.append(start)
            edges[i][0] = len(nodes) - 1
        else:
            edges[i][0] = nodes.index(start)

        if end not in nodes:
            nodes.append(end)
            edges[i][1] = len(nodes) - 1
        else:
            edges[i][1] = nodes.index(end)

    return nodes, edges, edges_geometry

def create_ends_shp(nodes_geometry: list, graph: Graph, end_id: int, start_id: int):
    ids = []
    geom = []
    neighbours = []
    for i in [end_id,start_id]:
        ids.append(i)
        geom.append(Point(nodes_geometry[i][0], nodes_geometry[i][1]))
        neighbours.append(str(graph.nodes[i].neighbors))

    return gpd.GeoDataFrame({'id': ids, 'neighbours': neighbours}, geometry=geom, crs="EPSG:2180")

def create_nodes_shp(nodes_geometry: list, graph: Graph):
    ids = []
    geom = []
    neighbours = []
    for i,n in enumerate(nodes_geometry):
        ids.append(i)
        geom.append(Point(n[0],n[1]))
        neighbours.append(str(graph.nodes[i].neighbors))

    return gpd.GeoDataFrame({'id': ids, 'neighbours': neighbours}, geometry=geom, crs="EPSG:2180")

def create_edges_shp(edges_geometry: list, graph: Graph):
    ids = []
    geom = []
    starts = []
    ends = []
    weights = []
    for i,winning_edge in enumerate(edges_geometry):
        ids.append(i)
        geom.append(winning_edge)
        starts.append(graph.edges[i].start_node)
        ends.append(graph.edges[i].end_node)
        weights.append(graph.edges[i].weight)

    return gpd.GeoDataFrame({'id': ids, 'end node': ends, 'start node': starts, 'weights': weights, 'geometry': geom}, crs="EPSG:2180")


def create_result_shp(edges_geometry: list, path_parts: list):
    path = []
    for winning_edge in path_parts:
        path.append(edges_geometry[winning_edge])

    # path_geo = linemerge(path)
    shortest_path = gpd.GeoDataFrame(geometry=path, crs="EPSG:2180")
    return shortest_path

def create_result_nodes_shp(nodes_geometry: list, path_parts: list):
    path = []
    for winning_node in path_parts:
        path.append(Point(nodes_geometry[winning_node][0],nodes_geometry[winning_node][1]))

    # path_geo = linemerge(path)
    shortest_path = gpd.GeoDataFrame(geometry=path, crs="EPSG:2180")
    return shortest_path