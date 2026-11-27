"""
Actividad 1 - Diseño Avanzado de Algoritmos
Subsecuencia común más larga (LCS) con tres enfoques:
  A) recursivo directo (sin memorizar)
  B) divide y conquista de Hirschberg
  C) programación dinámica tabular
"""
import sys

sys.setrecursionlimit(10000)


# ---------- Versión A: recursiva directa ----------
def lcs_recursiva(x, y):
    """Devuelve la LCS de x e y probando todas las ramas. Coste O(2^(m+n))."""
    def rec(i, j):
        if i == len(x) or j == len(y):
            return ""
        if x[i] == y[j]:
            return x[i] + rec(i + 1, j + 1)
        a = rec(i + 1, j)
        b = rec(i, j + 1)
        return a if len(a) >= len(b) else b
    return rec(0, 0)


# ---------- Versión C: programación dinámica tabular ----------
def lcs_dp(x, y):
    """Tabla L[m+1][n+1] y reconstrucción hacia atrás. O(m*n) tiempo y memoria."""
    m, n = len(x), len(y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        xi = x[i - 1]
        fila, ant = L[i], L[i - 1]
        for j in range(1, n + 1):
            if xi == y[j - 1]:
                fila[j] = ant[j - 1] + 1
            else:
                fila[j] = fila[j - 1] if fila[j - 1] > ant[j] else ant[j]
    # reconstrucción
    res = []
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            res.append(x[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(res))


# ---------- Versión B: Hirschberg ----------
def _ultima_fila(x, y):
    """Última fila de la tabla LCS guardando solo dos filas. Memoria O(n)."""
    prev = [0] * (len(y) + 1)
    for xi in x:
        cur = [0] * (len(y) + 1)
        for j in range(1, len(y) + 1):
            if xi == y[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = cur[j - 1] if cur[j - 1] > prev[j] else prev[j]
        prev = cur
    return prev


def lcs_hirschberg(x, y):
    """Divide x por la mitad y busca el mejor punto de corte en y."""
    m, n = len(x), len(y)
    if m == 0 or n == 0:
        return ""
    if m == 1:
        return x if x in y else ""
    mid = m // 2
    izq = _ultima_fila(x[:mid], y)
    der = _ultima_fila(x[mid:][::-1], y[::-1])
    mejor, k = -1, 0
    for j in range(n + 1):
        v = izq[j] + der[n - j]
        if v > mejor:
            mejor, k = v, j
    return lcs_hirschberg(x[:mid], y[:k]) + lcs_hirschberg(x[mid:], y[k:])


def es_subsecuencia(s, t):
    it = iter(t)
    return all(c in it for c in s)


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 2 else "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    b = sys.argv[2] if len(sys.argv) > 2 else "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    for nombre, f in (("DP", lcs_dp), ("Hirschberg", lcs_hirschberg)):
        r = f(a, b)
        print(f"{nombre:<11} len={len(r):3d}  {r}")
