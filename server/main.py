import os

from algorithms.a_star import a_star
from algorithms.dijkstra import dijkstra
from classes.edge import Edge
from classes.graph import Graph
from classes.node import Node
from shp_utilites import elements_from_shp, create_result_nodes_shp, create_result_shp, create_nodes_shp, create_edges_shp, create_ends_shp

if __name__ == '__main__':
    # Input
    shp_path = os.path.abspath("database/geodata/test.shp")
    start_node = 0
    end_node = 4

    # Creating graph
    graph_test = Graph()
    nodes, edges, edges_geometry = elements_from_shp(shp_path)
    for node in nodes:
        Node(graph_test, float(node[0]), float(node[1]))

    for edge in edges:
        Edge(graph_test, int(edge[0]), int(edge[1]), float(edge[2]), float(edge[3]))

    # Calculating paths using appropriate algorithms
    path_d = dijkstra(start_node, end_node, graph_test, False)
    path_a = a_star(start_node, end_node, graph_test, False)

    # Creating .shp files with path consisting of separate linestring
    create_ends_shp(nodes, graph_test, start_node, end_node).to_file(f"database/geodata/path_ends_{start_node}_{end_node}.shp")
    create_result_nodes_shp(nodes, path_d).to_file(f"database/geodata/path_test_d_{start_node}_{end_node}.shp")
    create_result_nodes_shp(nodes, path_a).to_file(f"database/geodata/path_test_a_{start_node}_{end_node}.shp")

    # Creating .shp containing all nodes and edges of the graph
    #create_nodes_shp(nodes, graph_test).to_file(f"database/geodata/all_nodes_big.shp")
    #create_edges_shp(edges_geometry, graph_test).to_file(f"database/geodata/all_edges_big.shp")

    # Printing list of edge's id which make path and its cost
    #print(f"Dijikstra: shortest path from node {start_node} to node {end_node} = {path_d} with cost {graph_test.nodes[end_node].g}")
    #print(f"A*:        shortest path from node {start_node} to node {end_node} = {path_a} with cost {graph_test.nodes[end_node].g}")