"""Juego de pruebas: las tres versiones deben dar la misma longitud y una subsecuencia válida."""
import random
from lcs import lcs_recursiva, lcs_dp, lcs_hirschberg, es_subsecuencia

casos = [("", ""), ("A", ""), ("ABC", "ABC"), ("ABC", "DEF"),
         ("ABCBDAB", "BDCABA"), ("AGGTAB", "GXTXAYB")]
random.seed(7)
for _ in range(200):
    casos.append(("".join(random.choice("ACGT") for _ in range(random.randint(0, 10))),
                  "".join(random.choice("ACGT") for _ in range(random.randint(0, 10)))))

for x, y in casos:
    a, b, c = lcs_recursiva(x, y), lcs_dp(x, y), lcs_hirschberg(x, y)
    assert len(a) == len(b) == len(c), (x, y, a, b, c)
    for r in (a, b, c):
        assert es_subsecuencia(r, x) and es_subsecuencia(r, y)
assert len(lcs_dp("ABCBDAB", "BDCABA")) == 4
print(f"OK: {len(casos)} casos superados")
