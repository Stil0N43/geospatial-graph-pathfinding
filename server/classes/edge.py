from classes.graph import Graph


class Edge:
    def __init__(self, graph: Graph, start_node: int, end_node: int, weight: float, weight_slimit: float, direction: int = 0, id: int = 0):
        self.id = len(graph.edges)
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.weight_slimit = weight_slimit

        graph.edges.append(self)
        if direction != 1:
            graph.nodes[end_node].add_neighbor(self.id)
        if direction != 2:
            graph.nodes[start_node].add_neighbor(self.id)

    def __str__(self):
        return f"[{self.id}, {self.start_node}, {self.end_node}, {self.weight}]"
