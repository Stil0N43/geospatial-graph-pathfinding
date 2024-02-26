import math

import geopandas as gpd
from shapely.geometry import Point

from algorithms.reconstruct_path import reconstruct_path
from algorithms.alter_weight import increase_weight, decrease_weight

from classes.graph import Graph
from classes.node import Node
from classes.priority_queue import PriorityQueue


def heuristic(curr_pnt: Node, end_pnt: Node):
    to_meters: float = 1
    diff_x: float = abs(curr_pnt.x - end_pnt.x) * to_meters
    diff_y: float = abs(curr_pnt.y - end_pnt.y) * to_meters
    distance: float = math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))
    return distance


def heuristic_geo(curr_pnt: Node, end_pnt: Node):
    current_point = gpd.GeoSeries([Point(curr_pnt.x, curr_pnt.y)], crs="EPSG:2180")
    end_point = gpd.GeoSeries([Point(end_pnt.x, end_pnt.y)], crs="EPSG:2180")
    return current_point.distance(end_point).item()


def a_star(start_id: int, end_id: int, graph: Graph, use_weight_slimit: bool, edges_went_through=None):
    increase_weight(graph, edges_went_through)
    considered = PriorityQueue()
    came_from: dict[int, (int, int)] = {}

    graph.nodes[start_id].g = 0
    graph.nodes[start_id].f = heuristic_geo(graph.nodes[start_id], graph.nodes[end_id])
    came_from[start_id] = [-1]
    considered.put(start_id, graph.nodes[start_id].f)

    while not considered.empty():

        curr_id = considered.get()

        if curr_id == end_id:
            break

        for edge_id in graph.nodes[curr_id].neighbors:
            next_id = graph.edges[edge_id].end_node
            if curr_id == next_id:
                next_id = graph.edges[edge_id].start_node

            new_weight: float
            if use_weight_slimit:
                new_weight = graph.edges[edge_id].weight_slimit
            else:
                new_weight = graph.edges[edge_id].weight

            new_cost = graph.nodes[curr_id].g + new_weight

            if next_id not in came_from or new_cost < graph.nodes[next_id].g:
                came_from[next_id] = [curr_id, edge_id]
                graph.nodes[next_id].g = new_cost
                graph.nodes[next_id].f = new_cost + heuristic_geo(graph.nodes[next_id], graph.nodes[end_id])
                # print(f"Adding - from {curr_id} to {next_id}, with cost {new_cost} and heuristic {heuristic_geo(graph.nodes[next_id], graph.nodes[end_id])}")
                considered.put(next_id, graph.nodes[next_id].f)

    decrease_weight(graph, edges_went_through)
    return reconstruct_path(came_from, start_id, end_id)
