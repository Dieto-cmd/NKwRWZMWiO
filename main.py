import json
import networkx as nx
import matplotlib.pyplot as plt
import find_path

# Read the data from the json file
with open('input_node_link_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create networkx graph from the data
G = nx.node_link_graph(data, edges="links")

# Read the start and destination nodes
start = next((n for n, attr in G.nodes(data=True) if attr.get('start')), None)
end   = next((n for n, attr in G.nodes(data=True) if attr.get('end')), None)

# Error handling - no start/end node
if start is None:
    print(f"ERROR: No start node. Provide start node in the json file.")
    print("e.g {\"id\": \"A\", \"start\": true}")
    exit()
if end is None:
    print(f"ERROR: No end node. Provide destination in the json file. ")
    print("e.g {\"id\": \"E\", \"end\": true}")
    exit()

# TODO: Create an algorithm that calculates if the path
# with edges that have value of 5 or less exists. DFS is probably a good choice
# For now it's shortest path according to field "value"
path_edges = []
try:
    path = nx.shortest_path(G, source=start, target=end, weight='value')
    path_edges = list(zip(path, path[1:]))
    print(f"The path exists: {' -> '.join(path)}")
except nx.NetworkXNoPath:
    print(f"ERROR: There is no path between {start} and {end}")
    exit()
except nx.NodeNotFound as e:
    print(f"ERROR: There is no node such as: {e}")
    exit()

pos = nx.kamada_kawai_layout(G)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Node colors
def node_colors(highlight_path=False):
    colors = []
    for node in G.nodes():
        if node == start:
            colors.append('limegreen')
        elif node == end:
            colors.append('tomato')
        elif highlight_path and node in path:
            colors.append('orange')
        else:
            colors.append('skyblue')
    return colors

edge_labels = nx.get_edge_attributes(G, 'value')

draw_kwargs = dict(
    pos=pos, with_labels=True,
    node_size=500, font_size=10
)

# Graph no. 1: Original
ax1 = axes[0]
ax1.set_title("Original Graph")
nx.draw(G, ax=ax1, node_color=node_colors(False), **draw_kwargs)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1,
    font_color='red', font_size=16)

# Graph no.2: Highlighted path
ax2 = axes[1]
ax2.set_title(f"Highlighted path: {' → '.join(path)}")

# Path edges vs other
other_edges = [e for e in G.edges() if e not in path_edges and (e[1], e[0]) not in path_edges]

nx.draw(G, ax=ax2, node_color=node_colors(True), **draw_kwargs)
nx.draw_networkx_edges(G, pos, edgelist=path_edges,
    edge_color='orange', width=3, ax=ax2)
nx.draw_networkx_edges(G, pos, edgelist=other_edges,
    edge_color='lightgray', width=1, ax=ax2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax2,
    font_color='red', font_size=16)

plt.tight_layout()
plt.show()