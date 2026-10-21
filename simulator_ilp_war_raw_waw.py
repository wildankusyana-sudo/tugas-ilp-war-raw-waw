"""
Simulasi sederhana dependency WAR, RAW, dan WAW pada Instruction-Level Parallelism (ILP).
Jalankan dengan: python simulator_ilp_war_raw_waw.py
Tidak memerlukan library tambahan.
"""

def dependency_graph(instructions):
    """Mendeteksi dependency antarinstruksi berdasarkan register yang dibaca/ditulis."""
    edges = []
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            a, b = instructions[i], instructions[j]
            # RAW: instruksi sebelumnya menulis register yang dibaca instruksi berikutnya
            if a["write"] and a["write"] in b["read"]:
                edges.append((i + 1, j + 1, "RAW", a["write"]))
            # WAR: instruksi sebelumnya membaca register yang ditulis instruksi berikutnya
            if b["write"] and b["write"] in a["read"]:
                edges.append((i + 1, j + 1, "WAR", b["write"]))
            # WAW: kedua instruksi menulis register yang sama
            if a["write"] and a["write"] == b["write"]:
                edges.append((i + 1, j + 1, "WAW", a["write"]))
    return edges

def show_case(title, instructions):
    print("\\n" + "=" * 64)
    print(title)
    print("- Instruksi:")
    for i, inst in enumerate(instructions, start=1):
        print(f"  I{i}: {inst['text']}")
    print("- Dependency graph (arah panah: instruksi lebih awal -> berikutnya):")
    edges = dependency_graph(instructions)
    if not edges:
        print("  Tidak ditemukan dependency.")
    else:
        for src, dst, kind, reg in edges:
            print(f"  I{src} -> I{dst} [{kind}, register {reg}]")
    return edges

if __name__ == "__main__":
    # RAW: I1 menghasilkan R1 yang kemudian dibaca I2
    raw = [
        {"text": "R1 = R2 + R3", "read": {"R2", "R3"}, "write": "R1"},
        {"text": "R4 = R1 * R5", "read": {"R1", "R5"}, "write": "R4"},
    ]
    show_case("1. READ AFTER WRITE (RAW) — true dependency", raw)

    # WAR: I1 perlu membaca nilai lama R2 sebelum I2 menulis R2
    war = [
        {"text": "R1 = R2 + R3", "read": {"R2", "R3"}, "write": "R1"},
        {"text": "R2 = R4 + R5", "read": {"R4", "R5"}, "write": "R2"},
    ]
    show_case("2. WRITE AFTER READ (WAR) — anti-dependency", war)

    # WAW: kedua instruksi menulis R1; urutan penulisan harus dipertahankan
    waw = [
        {"text": "R1 = R2 + R3", "read": {"R2", "R3"}, "write": "R1"},
        {"text": "R1 = R4 * R5", "read": {"R4", "R5"}, "write": "R1"},
    ]
    show_case("3. WRITE AFTER WRITE (WAW) — output dependency", waw)
