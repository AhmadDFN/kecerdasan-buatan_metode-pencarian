edges = [
    ("Surabaya", "Mojokerto", 55),
    ("Surabaya", "Pasuruan", 60),
    ("Mojokerto", "Malang", 80),
    ("Pasuruan", "Malang", 60),
    ("Pasuruan", "Probolinggo", 40),
    ("Probolinggo", "Situbondo", 100),
    ("Probolinggo", "Lumajang", 65),
    ("Malang", "Lumajang", 85),
    ("Malang", "Blitar", 70),
    ("Lumajang", "Jember", 55),
    ("Jember", "Bondowoso", 35),
    ("Jember", "Banyuwangi", 95),
    ("Bondowoso", "Situbondo", 40),
    ("Situbondo", "Banyuwangi", 120)
]
graph = {}
for u, v, w in edges:
    graph.setdefault(u, []).append((v, w))
    graph.setdefault(v, []).append((u, w))

for city in graph:
    graph[city].sort(key=lambda x: x[0])
default_h = {
    "Surabaya": 210,
    "Mojokerto": 230,
    "Pasuruan": 175,
    "Malang": 195,
    "Probolinggo": 140,
    "Blitar": 245,
    "Lumajang": 130,
    "Situbondo": 70,
    "Bondowoso": 70,
    "Jember": 75,
    "Banyuwangi": 0
}


def reconstruct_path(parent, start, goal):
    path = []
    curr = goal
    total_dist = 0
    while curr is not None:
        path.append(curr)
        prev = parent.get(curr)
        if prev is not None:
            for nb, weight in graph[prev]:
                if nb == curr:
                    total_dist += weight
                    break
        curr = prev
    path.reverse()
    return path, total_dist


def print_header(title):
    print("=" * 95)
    print(f" {title}")
    print("=" * 95)
    print(f"{'Pop':<25} | {'Frontier sesudah':<42} | {'Explored sesudah'}")
    print("-" * 95)


def print_summary(path, dist, expansions):
    print("-" * 95)
    print(f"Jalur akhir     : {' -> '.join(path)}")
    print(f"Total jarak     : {dist} km")
    print(f"Jumlah ekspansi : {expansions}\n")


def run_bfs(start="Surabaya", goal="Banyuwangi"):
    print_header("NOMOR 3: BFS (Breadth-First Search)")
    frontier = [start]
    explored = []
    parent = {start: None}
    expansions = 0

    print(f"{'-':<25} | {str(frontier):<42} | {{}}")

    while frontier:
        curr = frontier.pop(0)
        explored.append(curr)
        expansions += 1

        if curr == goal:
            exp_str = "{" + ", ".join(explored) + "}"
            print(f"{curr:<25} | {str(frontier):<42} | {exp_str}")
            break
        for nb, _ in graph[curr]:
            if nb not in explored and nb not in frontier:
                frontier.append(nb)
                parent[nb] = curr

        exp_str = "{" + ", ".join(explored) + "}"
        print(f"{curr:<25} | {str(frontier):<42} | {exp_str}")

    path, dist = reconstruct_path(parent, start, goal)
    print_summary(path, dist, expansions)


def run_dfs(start="Surabaya", goal="Banyuwangi"):
    print_header("NOMOR 4: DFS (Depth-First Search - Stack: atas ke bawah)")
    stack = [start]
    explored = []
    parent = {start: None}
    expansions = 0

    print(f"{'-':<25} | {str(stack):<42} | {{}}")

    while stack:
        curr = stack.pop(0)
        explored.append(curr)
        expansions += 1

        if curr == goal:
            exp_str = "{" + ", ".join(explored) + "}"
            print(f"{curr:<25} | {str(stack):<42} | {exp_str}")
            break
        for nb, _ in reversed(graph[curr]):
            if nb not in explored and nb not in stack:
                stack.insert(0, nb)
                parent[nb] = curr

        exp_str = "{" + ", ".join(explored) + "}"
        print(f"{curr:<25} | {str(stack):<42} | {exp_str}")

    path, dist = reconstruct_path(parent, start, goal)
    print_summary(path, dist, expansions)


def run_ucs(start="Surabaya", goal="Banyuwangi"):
    print_header("NOMOR 5: UCS (Uniform Cost Search)")
    frontier = {start: (0, False)}
    explored = []
    parent = {start: None}
    expansions = 0

    print(f"{'-':<25} | {'[Surabaya(0)]':<42} | {{}}")

    while frontier:
        sorted_keys = sorted(frontier.keys(), key=lambda k: (frontier[k][0], k))
        curr = sorted_keys[0]
        g_curr, _ = frontier.pop(curr)
        for k in frontier:
            frontier[k] = (frontier[k][0], False)

        explored.append(curr)
        expansions += 1

        if curr == goal:
            f_list = [f"{k}({frontier[k][0]})" for k in sorted(frontier.keys(), key=lambda x: (frontier[x][0], x))]
            exp_str = "{" + ", ".join(explored) + "}"
            print(f"{f'{curr}({g_curr})':<25} | {'[' + ', '.join(f_list) + ']':<42} | {exp_str}")
            break

        for nb, weight in graph[curr]:
            new_g = g_curr + weight
            if nb not in explored and nb not in frontier:
                frontier[nb] = (new_g, False)
                parent[nb] = curr
            elif nb in frontier and new_g < frontier[nb][0]:
                frontier[nb] = (new_g, True)
                parent[nb] = curr

        f_list = []
        for k in sorted(frontier.keys(), key=lambda x: (frontier[x][0], x)):
            g_val, upd = frontier[k]
            label = f"{k}({g_val}, diperbarui)" if upd else f"{k}({g_val})"
            f_list.append(label)

        exp_str = "{" + ", ".join(explored) + "}"
        print(f"{f'{curr}({g_curr})':<25} | {'[' + ', '.join(f_list) + ']':<42} | {exp_str}")

    path, dist = reconstruct_path(parent, start, goal)
    print_summary(path, dist, expansions)
def run_greedy(h_map, start="Surabaya", goal="Banyuwangi"):
    print_header("NOMOR 6: Greedy Best-First Search")
    frontier = [start]
    explored = []
    parent = {start: None}
    expansions = 0

    print(f"{'-':<25} | {f'[{start}({h_map[start]})]':<42} | {{}}")

    while frontier:
        frontier.sort(key=lambda k: (h_map[k], k))
        curr = frontier.pop(0)
        explored.append(curr)
        expansions += 1

        if curr == goal:
            frontier.sort(key=lambda k: (h_map[k], k))
            f_list = [f"{k}({h_map[k]})" for k in frontier]
            exp_str = "{" + ", ".join(explored) + "}"
            print(f"{f'{curr}({h_map[curr]})':<25} | {'[' + ', '.join(f_list) + ']':<42} | {exp_str}")
            break

        for nb, _ in graph[curr]:
            if nb not in explored and nb not in frontier:
                frontier.append(nb)
                parent[nb] = curr

        frontier.sort(key=lambda k: (h_map[k], k))
        f_list = [f"{k}({h_map[k]})" for k in frontier]
        exp_str = "{" + ", ".join(explored) + "}"
        print(f"{f'{curr}({h_map[curr]})':<25} | {'[' + ', '.join(f_list) + ']':<42} | {exp_str}")

    path, dist = reconstruct_path(parent, start, goal)
    print_summary(path, dist, expansions)


def run_astar(h_map, title="NOMOR 7: Algoritma A*", start="Surabaya", goal="Banyuwangi"):
    print_header(title)
    frontier = {start: (0, False)}
    explored = []
    parent = {start: None}
    expansions = 0

    f_start = 0 + h_map[start]
    print(f"{'-':<25} | {f'[{start}(0+{h_map[start]}={f_start})]':<42} | {{}}")

    while frontier:
        sorted_keys = sorted(frontier.keys(), key=lambda k: (frontier[k][0] + h_map[k], k))
        curr = sorted_keys[0]
        g_curr, _ = frontier.pop(curr)
        h_curr = h_map[curr]
        f_curr = g_curr + h_curr

        for k in frontier:
            frontier[k] = (frontier[k][0], False)

        explored.append(curr)
        expansions += 1

        pop_label = f"{curr} (g={g_curr},h={h_curr},f={f_curr})"

        if curr == goal:
            f_list = []
            for k in sorted(frontier.keys(), key=lambda x: (frontier[x][0] + h_map[x], x)):
                gk, _ = frontier[k]
                hk = h_map[k]
                f_list.append(f"{k}({gk}+{hk}={gk+hk})")
            exp_str = "{" + ", ".join(explored) + "}"
            print(f"{pop_label:<25} | {'[' + ', '.join(f_list) + ']':<42} | {exp_str}")
            break

        for nb, weight in graph[curr]:
            new_g = g_curr + weight
            if nb not in explored and nb not in frontier:
                frontier[nb] = (new_g, False)
                parent[nb] = curr
            elif nb in frontier and new_g < frontier[nb][0]:
                frontier[nb] = (new_g, True)
                parent[nb] = curr

        f_list = []
        for k in sorted(frontier.keys(), key=lambda x: (frontier[x][0] + h_map[x], x)):
            gk, upd = frontier[k]
            hk = h_map[k]
            fk = gk + hk
            if upd:
                f_list.append(f"{k}({gk}+{hk}={fk}, diperbarui)")
            else:
                f_list.append(f"{k}({gk}+{hk}={fk})")

        exp_str = "{" + ", ".join(explored) + "}"
        print(f"{pop_label:<25} | {'[' + ', '.join(f_list) + ']':<42} | {exp_str}")

    path, dist = reconstruct_path(parent, start, goal)
    print_summary(path, dist, expansions)


if __name__ == "__main__":
    run_bfs()
    run_dfs()
    run_ucs()
    run_greedy(default_h)
    run_astar(default_h, "NOMOR 7: Algoritma A* (Heuristik Standar)")
    h_9a = {city: 0 for city in default_h}
    run_astar(h_9a, "NOMOR 9a: Eksperimen A* dengan Semua h(n) = 0")
    h_9b = default_h.copy()
    h_9b["Lumajang"] = 300
    run_astar(h_9b, "NOMOR 9b: Eksperimen A* dengan h(Lumajang) = 300")
    h_9c = default_h.copy()
    h_9c["Jember"] = 0
    run_astar(h_9c, "NOMOR 9c: Eksperimen A* dengan h(Jember) = 0")
