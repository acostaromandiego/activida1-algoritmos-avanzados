"""Mide tiempo de CPU (process_time) y memoria pico (tracemalloc) de cada versión."""
import csv, random, time, tracemalloc, os
from lcs import lcs_recursiva, lcs_dp, lcs_hirschberg

random.seed(2025)
os.makedirs("resultados", exist_ok=True)

def cadena(n):
    return "".join(random.choice("ACGT") for _ in range(n))

def medir(f, x, y, rep=3):
    tiempos = []
    for _ in range(rep):
        t0 = time.process_time(); r = f(x, y); tiempos.append(time.process_time() - t0)
    tracemalloc.start(); f(x, y); _, pico = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return min(tiempos), pico / 1024, len(r)

filas = []
# Experimento 1: cinco parejas grandes (B y C)
for n in (100, 250, 500, 750, 1000):
    x, y = cadena(n), cadena(n)
    for nombre, f in (("B-Hirschberg", lcs_hirschberg), ("C-PD", lcs_dp)):
        t, mem, L = medir(f, x, y)
        filas.append(["grande", n, nombre, f"{t:.4f}", f"{mem:.1f}", L])
        print(filas[-1])

# Experimento 2: parejas pequeñas, donde la versión A todavía termina
for n in (8, 10, 12, 14, 16):
    x, y = cadena(n), cadena(n)
    for nombre, f in (("A-Recursiva", lcs_recursiva), ("B-Hirschberg", lcs_hirschberg), ("C-PD", lcs_dp)):
        t, mem, L = medir(f, x, y, rep=1 if nombre.startswith("A") else 5)
        filas.append(["pequeña", n, nombre, f"{t:.6f}", f"{mem:.1f}", L])
        print(filas[-1])

with open("resultados/mediciones.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["serie", "n", "version", "cpu_s", "mem_pico_KiB", "long_lcs"]); w.writerows(filas)

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    for v, est in (("B-Hirschberg", "o-"), ("C-PD", "s--")):
        d = [r for r in filas if r[0] == "grande" and r[2] == v]
        ax[0].plot([r[1] for r in d], [float(r[3]) for r in d], est, label=v)
        ax[1].plot([r[1] for r in d], [float(r[4]) / 1024 for r in d], est, label=v)
    ax[0].set_xlabel("n"); ax[0].set_ylabel("CPU (s)"); ax[0].set_title("Tiempo")
    ax[1].set_xlabel("n"); ax[1].set_ylabel("MiB"); ax[1].set_title("Memoria pico")
    for a in ax: a.grid(alpha=.3); a.legend()
    fig.tight_layout(); fig.savefig("resultados/grafica.png", dpi=160)
except ImportError:
    print("matplotlib no disponible: solo se genera el CSV")
