import networkx as nx # for Exception handling only
def find_path(graph, source, destination, weight='value'):
    # validation - same as in nx
    if source not in graph:
        raise nx.NodeNotFound(f"Node {source} doesn't exist")
    if destination not in graph:
        raise nx.NodeNotFound(f"Node {destination} doesn't exist")
    
    # ACTUAL ALGORITHM HERE
    path = []
    # -------------------
    # -------------------

    # Return a node list
    return path