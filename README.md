# Actividad 1. Diseño, análisis y comparación de algoritmos: la subsecuencia común más larga (LCS)
 
**Asignatura:** Diseño Avanzado de Algoritmos
**Autor:** Diego Acosta Román
 
Código de la Actividad 1: tres versiones del algoritmo de la LCS (recursiva directa,
Hirschberg y programación dinámica), con sus pruebas y los experimentos de tiempo y
memoria. El análisis teórico y la discusión de resultados están en la memoria (PDF).
 
## Contenido
 
| Archivo | Descripción |
|---|---|
| `lcs.py` | Las tres versiones: `lcs_recursiva`, `lcs_hirschberg` y `lcs_dp` |
| `tests.py` | Juego de pruebas (206 casos) |
| `experimentos.py` | Mide tiempo de CPU y memoria pico de cada versión |
| `Makefile` | Ejecuta pruebas y experimentos con un único comando |
| `resultados/` | Se crea al ejecutar los experimentos (`mediciones.csv` y `grafica.png`) |
 
No se usa ninguna librería que resuelva la LCS.
 
## Requisitos
 
- Python 3.8 o superior
- matplotlib (opcional, solo para la gráfica)
 
pip install matplotlib
 
## Ejecución
 
Con un único comando (Linux, Mac o Windows con `make` instalado):
 
make
 
Lanza primero las pruebas y después los experimentos.
 
En Windows con PowerShell, desde la carpeta del proyecto:
 
py tests.py
py experimentos.py
 
Otros usos:
 
make test solo las pruebas
make exp solo los experimentos
make demo ejemplo del Tema 3
python lcs.py CADENA1 CADENA2 LCS de dos cadenas cualquiera
 
## Resultados
 
Salida esperada de las pruebas:
 
OK: 206 casos superados
 
Los experimentos generan:
 
- `resultados/mediciones.csv`, con las columnas `serie, n, version, cpu_s, mem_pico_KiB, long_lcs`
- `resultados/grafica.png`, con el tiempo y la memoria de las versiones B y C frente a n
 
Las cadenas se generan con semilla fija (2025), así que los datos son siempre los mismos.
Los tiempos dependen del equipo en el que se ejecute.

