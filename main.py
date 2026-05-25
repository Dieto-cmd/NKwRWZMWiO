import json
import networkx as nx
import matplotlib.pyplot as plt
from find_path import find_path, MAX_JUMP

# Read the data from the json file
with open('input_node_link_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create networkx graph from the data
G = nx.node_link_graph(data, edges="links")

# Read the start and destination nodes
start = next((n for n, attr in G.nodes(data=True) if attr.get('start')), None)
end   = next((n for n, attr in G.nodes(data=True) if attr.get('end')), None)

if start is None:
    print("ERROR: No start node. Provide start node in the json file.")
    print('e.g. {"id": "A", "start": true}')
    exit()
if end is None:
    print("ERROR: No end node. Provide end node in the json file.")
    print('e.g. {"id": "E", "end": true}')
    exit()

# DFS: find any path using only edges with distance <= MAX_JUMP cubits
try:
    path = find_path(G, start, end, max_distance=MAX_JUMP)
except nx.NodeNotFound as e:
    print(f"ERROR: Node not found: {e}")
    exit()

path_edges = []
if path:
    path_edges = list(zip(path, path[1:]))
    print(f"Path exists: {' -> '.join(str(n) for n in path)}")
else:
    print(f"No path from {start} to {end} with max jump {MAX_JUMP} cubits.")

# ---------- Visualization ----------
pos = nx.kamada_kawai_layout(G)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

def node_colors(highlight_path=False):
    colors = []
    for node in G.nodes():
        if node == start:
            colors.append('limegreen')
        elif node == end:
            colors.append('tomato')
        elif highlight_path and path and node in path:
            colors.append('orange')
        else:
            colors.append('skyblue')
    return colors

edge_labels = nx.get_edge_attributes(G, 'value')

# Separate traversable (<=MAX_JUMP) from blocked (>MAX_JUMP) edges
traversable = [(u, v) for u, v, d in G.edges(data=True) if d.get('value', 0) <= MAX_JUMP]
blocked     = [(u, v) for u, v, d in G.edges(data=True) if d.get('value', 0) > MAX_JUMP]

# Graph 1: all edges, blocked ones dashed orange
ax1 = axes[0]
ax1.set_title(f"Graph (dashed = too far, max jump = {MAX_JUMP} cubits)")
nx.draw_networkx_nodes(G, pos, node_color=node_colors(False), node_size=500, ax=ax1)
nx.draw_networkx_labels(G, pos, ax=ax1, font_size=10)
nx.draw_networkx_edges(G, pos, edgelist=traversable, edge_color='steelblue', width=1.5, ax=ax1)
nx.draw_networkx_edges(G, pos, edgelist=blocked, edge_color='orange', width=1.5,
                       style='dashed', ax=ax1)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1,
                              font_color='red', font_size=14)

# Graph 2: highlight found path
ax2 = axes[1]
if path:
    ax2.set_title(f"Path: {' → '.join(str(n) for n in path)}")
else:
    ax2.set_title("No valid path found")

other_edges = [e for e in G.edges()
               if e not in path_edges and (e[1], e[0]) not in path_edges]

nx.draw_networkx_nodes(G, pos, node_color=node_colors(True), node_size=500, ax=ax2)
nx.draw_networkx_labels(G, pos, ax=ax2, font_size=10)
nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                       edge_color='darkorange', width=3, ax=ax2)
nx.draw_networkx_edges(G, pos, edgelist=other_edges,
                       edge_color='lightgray', width=1, ax=ax2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax2,
                              font_color='red', font_size=14)

plt.tight_layout()
plt.show()
