from classes.graph import Graph


def elements_from_txt(path_nodes: str, path_edges: str):
    lines_n = open(path_nodes, "r")
    lines_e = open(path_edges, "r")
    nodes = []
    edges = []

    for line in lines_n:
        values = line.split(';')
        nodes.append([float(values[0]), float(values[1])])

    for line in lines_e:
        values = line.split(';')
        edges.append([int(values[0]), int(values[1]), float(values[2])])

    return nodes, edges
