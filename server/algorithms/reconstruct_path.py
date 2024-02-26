def reconstruct_path(came_from: dict, start_id: int, end_id: int):
    curr_id = end_id

    path = []
    path_edges = []
    if curr_id not in came_from:
        return path, path_edges

    while curr_id != start_id:
        path.append(curr_id)
        curr_id, edge_id = came_from[curr_id]
        path_edges.append(edge_id)
    path.append(curr_id)
    path.reverse()
    path_edges.reverse()

    return path, path_edges
