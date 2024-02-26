from classes.graph import Graph
from classes.edge import Edge


def increase_weight(graph: Graph, visited: list[int]):
    # Checking if there was a previous path
    if visited is not None:
        # Doubling the weight for edges from previous path
        for id_v in visited:
            graph.edges[id_v].weight *= 2
            graph.edges[id_v].weight_slimit *= 2


def decrease_weight(graph: Graph, visited: list[int]):
    # Checking if there was a previous path
    if visited is not None:
        # Reversing the changes to the weight of previously visited edges
        for id_v in visited:
            graph.edges[id_v].weight /= 2
            graph.edges[id_v].weight_slimit /= 2
