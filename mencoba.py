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


def shortest_distances(goal):
    distances = {goal: 0}
    frontier = [(0, goal)]
    while frontier:
        frontier.sort()
        cost, city = frontier.pop(0)
        if cost > distances[city]:
            continue
        for neighbor, weight in graph[city]:
            new_cost = cost + weight
            if new_cost < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_cost
                frontier.append((new_cost, neighbor))
    return distances


def check_heuristic(h_map):
    actual = shortest_distances("Banyuwangi")
    bad_edges = []
    bad_cities = []
    for city_a, city_b, distance in edges:
        if abs(h_map[city_a] - h_map[city_b]) > distance:
            bad_edges.append((city_a, city_b, distance))
    for city, h_value in h_map.items():
        if h_value > actual[city]:
            bad_cities.append((city, h_value, actual[city]))
    return actual, bad_edges, bad_cities


def print_heuristic_check(title, h_map):
    actual, bad_edges, bad_cities = check_heuristic(h_map)
    print(f"\n{title}")
    print("Pemeriksaan tiap jalan:")
    for city_a, city_b, distance in edges:
        difference = abs(h_map[city_a] - h_map[city_b])
        print(f"  {city_a} - {city_b}: selisih h={difference}, jarak={distance}")
    print(f"Admissible : {'Ya' if not bad_cities else 'Tidak'}")
    print(f"Consistent : {'Ya' if not bad_edges else 'Tidak'}")
    if bad_cities:
        print("Kota yang melanggar admissible:")
        for city, h_value, real_cost in bad_cities:
            print(f"  {city}: h={h_value}, h*={real_cost}")
    if bad_edges:
        print("Jalan yang melanggar consistency:")
        for city_a, city_b, distance in bad_edges:
            difference = abs(h_map[city_a] - h_map[city_b])
            print(f"  {city_a} - {city_b}: selisih h={difference}, jarak={distance}")
    return actual


def run_nomor_1():
    print("\nNOMOR 1: PEMODELAN DAN RUANG SOLUSI")
    print("State: kota yang sedang ditempati truk")
    print("Initial state: Surabaya")
    print("Aksi: berpindah ke kota tetangga melalui jalan yang tersedia")
    print("Path cost: jumlah jarak jalan yang dilalui")
    print("Goal test: kota saat ini adalah Banyuwangi")
    routes = {
        "A": ["Surabaya", "Pasuruan", "Probolinggo", "Situbondo", "Banyuwangi"],
        "B": ["Surabaya", "Pasuruan", "Probolinggo", "Lumajang", "Jember", "Banyuwangi"],
        "C": ["Surabaya", "Pasuruan", "Malang", "Lumajang", "Jember", "Banyuwangi"],
        "D": ["Surabaya", "Mojokerto", "Malang", "Lumajang", "Jember", "Banyuwangi"],
    }
    for name, path in routes.items():
        _, distance = reconstruct_path(dict(zip(path[1:], path[:-1])), path[0], path[-1])
        print(f"Jalur {name}: {' -> '.join(path)} | {len(path)-1} ruas | {distance} km")
    print("Ruas paling sedikit: Jalur A (4 ruas)")
    print("Jarak paling pendek: Jalur B (315 km)")


def run_nomor_2():
    print("\nNOMOR 2: PEMERIKSAAN HEURISTIK")
    actual = print_heuristic_check("Heuristik standar", default_h)
    for city in ["Jember", "Situbondo", "Lumajang"]:
        print(f"h*({city}) = {actual[city]} km; h({city}) = {default_h[city]} km")
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
    return path, dist, expansions, explored


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
    return path, dist, expansions, explored


def run_ucs(start="Surabaya", goal="Banyuwangi"):
    print_header("NOMOR 5: UCS (Uniform Cost Search)")
    frontier = {start: (0, False)}
    explored = []
    parent = {start: None}
    expansions = 0
    updates = []

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
                updates.append((nb, frontier[nb][0], new_g, curr))
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
    print("Pembaruan biaya:")
    for city, old_cost, new_cost, via in updates:
        print(f"  {city}: {old_cost} menjadi {new_cost} melalui {via}")
    return path, dist, expansions, explored


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
    return path, dist, expansions, explored


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
    return path, dist, expansions, explored


if __name__ == "__main__":
    run_nomor_1()
    run_nomor_2()
    hasil_bfs = run_bfs()
    hasil_dfs = run_dfs()
    hasil_ucs = run_ucs()
    print("BFS menemukan jalur dengan jumlah ruas minimum, tetapi belum tentu jaraknya paling pendek.")
    print(f"Jarak BFS: {hasil_bfs[1]} km; jarak minimum menurut UCS: {hasil_ucs[1]} km.")
    print("DFS mengambil Mojokerto lebih dulu karena tetangga alfabet pertama diletakkan di atas stack.")
    print(f"Jalur DFS yang ditemukan: {' -> '.join(hasil_dfs[0])} ({hasil_dfs[1]} km).")
    hasil_greedy = run_greedy(default_h)
    print("Greedy hanya melihat h(n), sehingga dapat memilih jalur yang tampak dekat tetapi jarak akhirnya lebih panjang.")
    print(f"Jarak Greedy: {hasil_greedy[1]} km; jarak minimum menurut UCS: {hasil_ucs[1]} km.")
    hasil_astar = run_astar(default_h, "NOMOR 7: Algoritma A* (Heuristik Standar)")
    tidak_diperluas = sorted(set(hasil_ucs[3]) - set(hasil_astar[3]))
    print("\nKota yang diperluas UCS tetapi tidak diperluas A*:", ", ".join(tidak_diperluas))
    print("Kota-kota itu tidak diambil sebelum goal karena nilai f pada jalur menuju Banyuwangi lebih kecil.")
    print("\nNOMOR 8: PERBANDINGAN")
    print(f"{'Algoritma':<10} {'Jalur':<65} {'Jarak':>8} {'Ekspansi':>10} {'Optimal?'}")
    hasil_semua = [
        ("BFS", hasil_bfs), ("DFS", hasil_dfs), ("UCS", hasil_ucs),
        ("Greedy", hasil_greedy), ("A*", hasil_astar)
    ]
    for nama, hasil in hasil_semua:
        path, distance, expansions, _ = hasil
        status = "Ya" if distance == hasil_ucs[1] else "Tidak"
        print(f"{nama:<10} {' -> '.join(path):<65} {distance:>5} km {expansions:>10} {status}")
    print("Rekomendasi: Saya memilih A* untuk rute ini karena hasilnya mencapai jarak minimum.")
    print(f"A* memproses {hasil_astar[2]} kota, sedangkan UCS memproses {hasil_ucs[2]} kota.")
    print("Heuristik standar pada data ini konsisten dan tidak melebihi jarak sebenarnya ke tujuan.")
    print("Jika nilai heuristik tidak tersedia atau belum diperiksa, UCS tetap menjadi pilihan yang aman untuk mencari jarak minimum.")
    h_9a = {city: 0 for city in default_h}
    run_astar(h_9a, "NOMOR 9a: Eksperimen A* dengan Semua h(n) = 0")
    print_heuristic_check("Pemeriksaan NOMOR 9a", h_9a)
    h_9b = default_h.copy()
    h_9b["Lumajang"] = 300
    run_astar(h_9b, "NOMOR 9b: Eksperimen A* dengan h(Lumajang) = 300")
    print_heuristic_check("Pemeriksaan NOMOR 9b", h_9b)
    h_9c = default_h.copy()
    h_9c["Jember"] = 0
    run_astar(h_9c, "NOMOR 9c: Eksperimen A* dengan h(Jember) = 0")
    print_heuristic_check("Pemeriksaan NOMOR 9c", h_9c)

