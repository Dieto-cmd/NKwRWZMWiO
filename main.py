import json, sys, math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from find_path import find_path, MAX_JUMP

def error(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)

def validate(data, filepath):
    if not isinstance(data, dict):
        error(f"'{filepath}': plik musi zawierać obiekt JSON, nie {type(data).__name__}")

    # river_width
    if 'river_width' not in data:
        error("brak pola 'river_width'")
    rw = data['river_width']
    if not isinstance(rw, (int, float)) or isinstance(rw, bool):
        error(f"'river_width' musi być liczbą, otrzymano: {rw!r}")
    if rw <= 0:
        error(f"'river_width' musi być dodatnie, otrzymano: {rw}")

    # max_jump (opcjonalne)
    if 'max_jump' in data:
        mj = data['max_jump']
        if not isinstance(mj, (int, float)) or isinstance(mj, bool):
            error(f"'max_jump' musi być liczbą, otrzymano: {mj!r}")
        if mj <= 0:
            error(f"'max_jump' musi być dodatnie, otrzymano: {mj}")

    # crocodiles
    if 'crocodiles' not in data:
        error("brak pola 'crocodiles'")
    crocs = data['crocodiles']
    if not isinstance(crocs, list):
        error(f"'crocodiles' musi być listą, otrzymano: {type(crocs).__name__}")
    if len(crocs) == 0:
        error("'crocodiles' nie może być pustą listą")

    seen_ids = set()
    for i, c in enumerate(crocs):
        prefix = f"krokodyl nr {i+1}"
        if not isinstance(c, dict):
            error(f"{prefix}: oczekiwano obiektu, otrzymano: {c!r}")

        # id
        if 'id' not in c:
            error(f"{prefix}: brak pola 'id'")
        cid = c['id']
        if not isinstance(cid, (str, int, float)) or isinstance(cid, bool):
            error(f"{prefix}: 'id' musi być tekstem lub liczbą, otrzymano: {cid!r}")
        cid_str = str(cid)
        if cid_str in ('START', 'END'):
            error(f"{prefix}: 'id' nie może być 'START' ani 'END' (zarezerwowane)")
        if cid_str in seen_ids:
            error(f"{prefix}: duplikat 'id' = {cid!r}")
        seen_ids.add(cid_str)

        # x
        if 'x' not in c:
            error(f"{prefix} (id={cid!r}): brak pola 'x'")
        x = c['x']
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            error(f"{prefix} (id={cid!r}): 'x' musi być liczbą, otrzymano: {x!r}")
        if x < 1 or x >= (rw-1):
            error(f"{prefix} (id={cid!r}): 'x' musi być w zakresie (1, {(rw-1)}), otrzymano: {x}")

        # y
        if 'y' not in c:
            error(f"{prefix} (id={cid!r}): brak pola 'y'")
        y = c['y']
        if not isinstance(y, (int, float)) or isinstance(y, bool):
            error(f"{prefix} (id={cid!r}): 'y' musi być liczbą, otrzymano: {y!r}")

# ---- Load & validate ----
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input_coords.json'

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    error(f"plik '{input_file}' nie istnieje")
except json.JSONDecodeError as e:
    error(f"nieprawidłowy JSON w '{input_file}': {e}")

validate(data, input_file)

river_width = data['river_width']
max_jump    = data.get('max_jump', MAX_JUMP)
crocs       = data['crocodiles']

# ---- Build graph from coordinates ----
G = nx.Graph()
for c in crocs:
    G.add_node(c['id'], x=c['x'], y=c['y'])

ys = [c['y'] for c in crocs]
mid_y = (max(ys) + min(ys)) / 2
G.add_node('START', x=0,           y=mid_y)
G.add_node('END',   x=river_width, y=mid_y)

# bank-to-croc distances (perpendicular to bank)
for c in crocs:
    G.add_edge('START', c['id'], value=round(c['x'],               2))
    G.add_edge(c['id'], 'END',   value=round(river_width - c['x'], 2))

# croc-to-croc Euclidean distances
for i in range(len(crocs)):
    for j in range(i + 1, len(crocs)):
        c1, c2 = crocs[i], crocs[j]
        dist = math.sqrt((c2['x']-c1['x'])**2 + (c2['y']-c1['y'])**2)
        G.add_edge(c1['id'], c2['id'], value=round(dist, 2))

# ---- DFS ----
path = find_path(G, 'START', 'END', max_distance=max_jump)
path_set = set()
if path:
    for i in range(len(path) - 1):
        path_set.add((path[i],   path[i+1]))
        path_set.add((path[i+1], path[i]))
    print(f"Path: {' -> '.join(path)}")
else:
    print(f"No path across the river (max jump: {max_jump} cubits)")

# ---- Visualization ----
MARGIN  = 2.0
y_min   = min(ys) - MARGIN
y_max   = max(ys) + MARGIN
bank_w  = max(river_width * 0.04, 0.8)

fig, ax = plt.subplots(figsize=(14, 7))

# Water
ax.add_patch(mpatches.Rectangle(
    (0, y_min), river_width, y_max - y_min,
    fc='#d6eaf8', ec='none', zorder=0))

# Banks
for bx, fc, label in [
    (-bank_w,     '#2e7d32', 'START'),
    (river_width, '#c62828', 'META'),
]:
    ax.add_patch(mpatches.Rectangle(
        (bx, y_min), bank_w, y_max - y_min,
        fc=fc, ec='none', zorder=1))
    ax.text(bx + bank_w/2, (y_min + y_max)/2, label,
        ha='center', va='center', fontsize=10, fontweight='bold',
        color='white', rotation=90, zorder=2)

# Croc-to-croc edges
for u, v, d in G.edges(data=True):
    if 'START' in (u, v) or 'END' in (u, v):
        continue
    val  = d['value']
    pu   = (G.nodes[u]['x'], G.nodes[u]['y'])
    pv   = (G.nodes[v]['x'], G.nodes[v]['y'])
    on_path = (u, v) in path_set
    if on_path:
        ax.plot([pu[0], pv[0]], [pu[1], pv[1]],
            color='darkorange', lw=3.5, zorder=4, solid_capstyle='round')
        mx, my = (pu[0]+pv[0])/2, (pu[1]+pv[1])/2
        ax.text(mx, my + 0.3, f'{val}',
            ha='center', fontsize=8, color='darkorange', fontweight='bold', zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.8))
    elif val <= max_jump:
        ax.plot([pu[0], pv[0]], [pu[1], pv[1]],
            color='#1565c0', lw=1.2, alpha=0.45, zorder=2)

# Bank-to-croc edges
for c in crocs:
    cx, cy = c['x'], c['y']
    cid    = c['id']
    left_d  = round(cx,               2)
    right_d = round(river_width - cx, 2)

    for x0, x1, dist, key_pair in [
        (0,           cx,           left_d,  ('START', cid)),
        (cx,          river_width,  right_d, (cid,    'END')),
    ]:
        on_path = key_pair in path_set
        if on_path:
            ax.annotate('', xy=(x1, cy), xytext=(x0, cy),
                arrowprops=dict(arrowstyle='->', color='darkorange',
                                lw=2.5, mutation_scale=15), zorder=4)
            ax.text((x0+x1)/2, cy + 0.35, f'{dist}',
                ha='center', fontsize=8, color='darkorange', fontweight='bold', zorder=6,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.8))
        elif dist <= max_jump:
            ax.plot([x0, x1], [cy, cy], color='#1565c0', lw=1.2, alpha=0.45, zorder=2)
            ax.text((x0+x1)/2, cy + 0.35, f'{dist}',
                ha='center', fontsize=7, color='#1565c0', alpha=0.7, zorder=3)

# Crocodiles
for c in crocs:
    on_path_node = path and c['id'] in path
    fc = 'darkorange' if on_path_node else '#388e3c'
    ax.scatter(c['x'], c['y'], s=700, color=fc, zorder=7,
        edgecolors='white', linewidths=2)
    ax.text(c['x'], c['y'], c['id'],
        ha='center', va='center', fontsize=9, fontweight='bold',
        color='white', zorder=8)

# Axes
ax.set_xlim(-bank_w - 0.3, river_width + bank_w + 0.3)
ax.set_ylim(y_min - 0.2,   y_max + 0.2)
ax.set_xlabel('Odległość od lewego brzegu [łokcie]', fontsize=11)
ax.set_ylabel('Pozycja wzdłuż rzeki [łokcie]',       fontsize=11)
ax.set_xticks(range(0, river_width + 1, 2))
ax.grid(True, axis='x', alpha=0.15, color='navy', zorder=1)

title = (
    f"Ścieżka: {' → '.join(n for n in path if n not in ('START','END'))}"
    if path else "Brak drogi przez rzekę"
)
ax.set_title(title, fontsize=13, fontweight='bold', pad=12)

legend_elements = [
    mpatches.Patch(fc='#d6eaf8', ec='steelblue',  label='Rzeka Nil'),
    mpatches.Patch(fc='#2e7d32',                   label='Brzeg startowy'),
    mpatches.Patch(fc='#c62828',                   label='Brzeg docelowy'),
    plt.Line2D([0],[0], color='#1565c0', lw=1.5, alpha=0.7,
        label=f'Osiągalny skok (≤ {max_jump} łokci)'),
    plt.Line2D([0],[0], color='darkorange', lw=3.5,
        label='Znaleziona ścieżka'),
    mpatches.Patch(fc='#388e3c',   label='Krokodyl'),
    mpatches.Patch(fc='darkorange', label='Krokodyl na ścieżce'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.92)

plt.tight_layout()
plt.show()
