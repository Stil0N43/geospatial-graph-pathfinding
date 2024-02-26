from algorithms.reconstruct_path import reconstruct_path
from algorithms.alter_weight import increase_weight, decrease_weight
from classes.graph import Graph
from classes.priority_queue import PriorityQueue


def dijkstra(start_id: int, end_id: int, graph: Graph, use_weight_slimit: bool, edges_went_through=None):
    increase_weight(graph, edges_went_through)
    considered = PriorityQueue()
    came_from: dict[int, (int, int)] = {}

    graph.nodes[start_id].g = 0
    came_from[start_id] = [-1]
    considered.put(start_id, graph.nodes[start_id].g)

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
                # print(f"Adding - from {curr_id} to {next_id}, with cost {new_cost}")
                considered.put(next_id, new_cost)

    decrease_weight(graph, edges_went_through)
    return reconstruct_path(came_from, start_id, end_id)
