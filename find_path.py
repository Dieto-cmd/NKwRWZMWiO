import networkx as nx

MAX_JUMP = 5  # max jump distance in cubits

def find_path(graph, source, destination, max_distance=MAX_JUMP, weight='value'):
    """
    DFS - finds any path from source to destination
    using only edges with weight <= max_distance.
    Returns list of nodes forming the path, or [] if no path exists.
    """
    if source not in graph:
        raise nx.NodeNotFound(f"Node {source} doesn't exist")
    if destination not in graph:
        raise nx.NodeNotFound(f"Node {destination} doesn't exist")

    visited = set()

    def dfs(node, path):
        if node == destination:
            return path[:]
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                raw = graph.get_edge_data(node, neighbor) or {}
                # MultiGraph returns {key: data_dict}, Graph returns data_dict directly
                if raw and isinstance(next(iter(raw.values())), dict):
                    dist = min(d.get(weight, float('inf')) for d in raw.values())
                else:
                    dist = raw.get(weight, float('inf'))
                if dist <= max_distance:
                    path.append(neighbor)
                    result = dfs(neighbor, path)
                    if result is not None:
                        return result
                    path.pop()
        return None

    result = dfs(source, [source])
    return result if result is not None else []
