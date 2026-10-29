ruas_jalan = [
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
graf = {}
for asal, tujuan, jarak in ruas_jalan:
    graf.setdefault(asal, []).append((tujuan, jarak))
    graf.setdefault(tujuan, []).append((asal, jarak))

for kota in graf:
    graf[kota].sort(key=lambda pasangan: pasangan[0])
heuristik_awal = {
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


def susun_jalur(induk, awal, tujuan):
    jalur = []
    sekarang = tujuan
    total_jarak = 0
    while sekarang is not None:
        jalur.append(sekarang)
        sebelumnya = induk.get(sekarang)
        if sebelumnya is not None:
            for tetangga, bobot in graf[sebelumnya]:
                if tetangga == sekarang:
                    total_jarak += bobot
                    break
        sekarang = sebelumnya
    jalur.reverse()
    return jalur, total_jarak


def cetak_kepala(judul):
    print("=" * 95)
    print(f" {judul}")
    print("=" * 95)
    print(f"{'Kota diproses':<25} | {'Daftar batas sesudah':<42} | {'Kota dikunjungi'}")
    print("-" * 95)


def cetak_ringkasan(jalur, jarak, jumlah_ekspansi):
    print("-" * 95)
    print(f"Jalur akhir     : {' -> '.join(jalur)}")
    print(f"Total jarak     : {jarak} km")
    print(f"Jumlah pemrosesan : {jumlah_ekspansi}\n")


def jalankan_bfs(awal="Surabaya", tujuan="Banyuwangi"):
    cetak_kepala("NOMOR 3: BFS (Breadth-First Search)")
    daftar_batas = [awal]
    sudah_dikunjungi = []
    induk = {awal: None}
    jumlah_ekspansi = 0

    print(f"{'-':<25} | {str(daftar_batas):<42} | {{}}")

    while daftar_batas:
        sekarang = daftar_batas.pop(0)
        sudah_dikunjungi.append(sekarang)
        jumlah_ekspansi += 1

        if sekarang == tujuan:
            teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
            print(f"{sekarang:<25} | {str(daftar_batas):<42} | {teks_dikunjungi}")
            break
        for tetangga, _ in graf[sekarang]:
            if tetangga not in sudah_dikunjungi and tetangga not in daftar_batas:
                daftar_batas.append(tetangga)
                induk[tetangga] = sekarang

        teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
        print(f"{sekarang:<25} | {str(daftar_batas):<42} | {teks_dikunjungi}")

    jalur, jarak = susun_jalur(induk, awal, tujuan)
    cetak_ringkasan(jalur, jarak, jumlah_ekspansi)


def jalankan_dfs(awal="Surabaya", tujuan="Banyuwangi"):
    cetak_kepala("NOMOR 4: DFS (Depth-First Search - Stack: atas ke bawah)")
    tumpukan = [awal]
    sudah_dikunjungi = []
    induk = {awal: None}
    jumlah_ekspansi = 0

    print(f"{'-':<25} | {str(tumpukan):<42} | {{}}")

    while tumpukan:
        sekarang = tumpukan.pop(0)
        sudah_dikunjungi.append(sekarang)
        jumlah_ekspansi += 1

        if sekarang == tujuan:
            teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
            print(f"{sekarang:<25} | {str(tumpukan):<42} | {teks_dikunjungi}")
            break
        for tetangga, _ in reversed(graf[sekarang]):
            if tetangga not in sudah_dikunjungi and tetangga not in tumpukan:
                tumpukan.insert(0, tetangga)
                induk[tetangga] = sekarang

        teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
        print(f"{sekarang:<25} | {str(tumpukan):<42} | {teks_dikunjungi}")

    jalur, jarak = susun_jalur(induk, awal, tujuan)
    cetak_ringkasan(jalur, jarak, jumlah_ekspansi)


def jalankan_ucs(awal="Surabaya", tujuan="Banyuwangi"):
    cetak_kepala("NOMOR 5: UCS (Uniform Cost Search)")
    daftar_batas = {awal: (0, False)}
    sudah_dikunjungi = []
    induk = {awal: None}
    jumlah_ekspansi = 0

    print(f"{'-':<25} | {'[Surabaya(0)]':<42} | {{}}")

    while daftar_batas:
        kunci_terurut = sorted(daftar_batas.keys(), key=lambda kota_depan: (daftar_batas[kota_depan][0], kota_depan))
        sekarang = kunci_terurut[0]
        biaya_sekarang, _ = daftar_batas.pop(sekarang)
        for kota_depan in daftar_batas:
            daftar_batas[kota_depan] = (daftar_batas[kota_depan][0], False)

        sudah_dikunjungi.append(sekarang)
        jumlah_ekspansi += 1

        if sekarang == tujuan:
            daftar_label = [f"{kota_depan}({daftar_batas[kota_depan][0]})" for kota_depan in sorted(daftar_batas.keys(), key=lambda pasangan: (daftar_batas[pasangan][0], pasangan))]
            teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
            print(f"{f'{sekarang}({biaya_sekarang})':<25} | {'[' + ', '.join(daftar_label) + ']':<42} | {teks_dikunjungi}")
            break

        for tetangga, bobot in graf[sekarang]:
            biaya_baru = biaya_sekarang + bobot
            if tetangga not in sudah_dikunjungi and tetangga not in daftar_batas:
                daftar_batas[tetangga] = (biaya_baru, False)
                induk[tetangga] = sekarang
            elif tetangga in daftar_batas and biaya_baru < daftar_batas[tetangga][0]:
                daftar_batas[tetangga] = (biaya_baru, True)
                induk[tetangga] = sekarang

        daftar_label = []
        for kota_depan in sorted(daftar_batas.keys(), key=lambda pasangan: (daftar_batas[pasangan][0], pasangan)):
            biaya, diperbarui = daftar_batas[kota_depan]
            teks_label = f"{kota_depan}({biaya}, diperbarui)" if diperbarui else f"{kota_depan}({biaya})"
            daftar_label.append(teks_label)

        teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
        print(f"{f'{sekarang}({biaya_sekarang})':<25} | {'[' + ', '.join(daftar_label) + ']':<42} | {teks_dikunjungi}")

    jalur, jarak = susun_jalur(induk, awal, tujuan)
    cetak_ringkasan(jalur, jarak, jumlah_ekspansi)
def jalankan_greedy(peta_heuristik, awal="Surabaya", tujuan="Banyuwangi"):
    cetak_kepala("NOMOR 6: Greedy Best-First Search")
    daftar_batas = [awal]
    sudah_dikunjungi = []
    induk = {awal: None}
    jumlah_ekspansi = 0

    print(f"{'-':<25} | {f'[{awal}({peta_heuristik[awal]})]':<42} | {{}}")

    while daftar_batas:
        daftar_batas.sort(key=lambda kota_depan: (peta_heuristik[kota_depan], kota_depan))
        sekarang = daftar_batas.pop(0)
        sudah_dikunjungi.append(sekarang)
        jumlah_ekspansi += 1

        if sekarang == tujuan:
            daftar_batas.sort(key=lambda kota_depan: (peta_heuristik[kota_depan], kota_depan))
            daftar_label = [f"{kota_depan}({peta_heuristik[kota_depan]})" for kota_depan in daftar_batas]
            teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
            print(f"{f'{sekarang}({peta_heuristik[sekarang]})':<25} | {'[' + ', '.join(daftar_label) + ']':<42} | {teks_dikunjungi}")
            break

        for tetangga, _ in graf[sekarang]:
            if tetangga not in sudah_dikunjungi and tetangga not in daftar_batas:
                daftar_batas.append(tetangga)
                induk[tetangga] = sekarang

        daftar_batas.sort(key=lambda kota_depan: (peta_heuristik[kota_depan], kota_depan))
        daftar_label = [f"{kota_depan}({peta_heuristik[kota_depan]})" for kota_depan in daftar_batas]
        teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
        print(f"{f'{sekarang}({peta_heuristik[sekarang]})':<25} | {'[' + ', '.join(daftar_label) + ']':<42} | {teks_dikunjungi}")

    jalur, jarak = susun_jalur(induk, awal, tujuan)
    cetak_ringkasan(jalur, jarak, jumlah_ekspansi)


def jalankan_astar(peta_heuristik, judul="NOMOR 7: Algoritma A*", awal="Surabaya", tujuan="Banyuwangi"):
    cetak_kepala(judul)
    daftar_batas = {awal: (0, False)}
    sudah_dikunjungi = []
    induk = {awal: None}
    jumlah_ekspansi = 0

    nilai_awal = 0 + peta_heuristik[awal]
    print(f"{'-':<25} | {f'[{awal}(0+{peta_heuristik[awal]}={nilai_awal})]':<42} | {{}}")

    while daftar_batas:
        kunci_terurut = sorted(daftar_batas.keys(), key=lambda kota_depan: (daftar_batas[kota_depan][0] + peta_heuristik[kota_depan], kota_depan))
        sekarang = kunci_terurut[0]
        biaya_sekarang, _ = daftar_batas.pop(sekarang)
        heuristik_sekarang = peta_heuristik[sekarang]
        nilai_sekarang = biaya_sekarang + heuristik_sekarang

        for kota_depan in daftar_batas:
            daftar_batas[kota_depan] = (daftar_batas[kota_depan][0], False)

        sudah_dikunjungi.append(sekarang)
        jumlah_ekspansi += 1

        label_diproses = f"{sekarang} (g={biaya_sekarang},h={heuristik_sekarang},f={nilai_sekarang})"

        if sekarang == tujuan:
            daftar_label = []
            for kota_depan in sorted(daftar_batas.keys(), key=lambda pasangan: (daftar_batas[pasangan][0] + peta_heuristik[pasangan], pasangan)):
                biaya_tetangga, _ = daftar_batas[kota_depan]
                heuristik_tetangga = peta_heuristik[kota_depan]
                daftar_label.append(f"{kota_depan}({biaya_tetangga}+{heuristik_tetangga}={biaya_tetangga+heuristik_tetangga})")
            teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
            print(f"{label_diproses:<25} | {'[' + ', '.join(daftar_label) + ']':<42} | {teks_dikunjungi}")
            break

        for tetangga, bobot in graf[sekarang]:
            biaya_baru = biaya_sekarang + bobot
            if tetangga not in sudah_dikunjungi and tetangga not in daftar_batas:
                daftar_batas[tetangga] = (biaya_baru, False)
                induk[tetangga] = sekarang
            elif tetangga in daftar_batas and biaya_baru < daftar_batas[tetangga][0]:
                daftar_batas[tetangga] = (biaya_baru, True)
                induk[tetangga] = sekarang

        daftar_label = []
        for kota_depan in sorted(daftar_batas.keys(), key=lambda pasangan: (daftar_batas[pasangan][0] + peta_heuristik[pasangan], pasangan)):
            biaya_tetangga, diperbarui = daftar_batas[kota_depan]
            heuristik_tetangga = peta_heuristik[kota_depan]
            nilai_tetangga = biaya_tetangga + heuristik_tetangga
            if diperbarui:
                daftar_label.append(f"{kota_depan}({biaya_tetangga}+{heuristik_tetangga}={nilai_tetangga}, diperbarui)")
            else:
                daftar_label.append(f"{kota_depan}({biaya_tetangga}+{heuristik_tetangga}={nilai_tetangga})")

        teks_dikunjungi = "{" + ", ".join(sudah_dikunjungi) + "}"
        print(f"{label_diproses:<25} | {'[' + ', '.join(daftar_label) + ']':<42} | {teks_dikunjungi}")

    jalur, jarak = susun_jalur(induk, awal, tujuan)
    cetak_ringkasan(jalur, jarak, jumlah_ekspansi)


if __name__ == "__main__":
    jalankan_bfs()
    jalankan_dfs()
    jalankan_ucs()
    jalankan_greedy(heuristik_awal)
    jalankan_astar(heuristik_awal, "NOMOR 7: Algoritma A* (Heuristik Standar)")
    heuristik_9a = {kota: 0 for kota in heuristik_awal}
    jalankan_astar(heuristik_9a, "NOMOR 9a: Eksperimen A* dengan Semua h(n) = 0")
    heuristik_9b = heuristik_awal.copy()
    heuristik_9b["Lumajang"] = 300
    jalankan_astar(heuristik_9b, "NOMOR 9b: Eksperimen A* dengan h(Lumajang) = 300")
    heuristik_9c = heuristik_awal.copy()
    heuristik_9c["Jember"] = 0
    jalankan_astar(heuristik_9c, "NOMOR 9c: Eksperimen A* dengan h(Jember) = 0")
