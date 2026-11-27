# Subsecuencia común más larga (LCS): recursiva, Hirschberg y programación dinámica

Actividad 1 de la asignatura **Diseño Avanzado de Algoritmos**.
Autor: Diego Acosta Román

## 1. Descripción del problema

Dadas dos cadenas X (longitud m) e Y (longitud n), la subsecuencia común más larga (LCS)
es la secuencia más larga de símbolos que aparece en las dos cadenas en el mismo orden,
aunque no estén seguidos.

Ejemplo: para `ABCBDAB` y `BDCABA` una LCS es `BCBA` (longitud 4). Puede haber varias
soluciones distintas con la misma longitud, por ejemplo `BDAB` también es válida.

El objetivo de la actividad es resolver este problema con tres técnicas diferentes,
analizar su complejidad de forma teórica y comprobar con experimentos si los resultados
reales coinciden con lo esperado.

## 2. Idea común a las tres versiones

Las tres versiones parten de la misma recurrencia. Si el símbolo actual coincide en las
dos cadenas, forma parte de la LCS y se avanza en ambas. Si no coincide, nos quedamos con
el mejor resultado entre quitar un símbolo de X o quitarlo de Y:

    L(i,j) = 0                         si i = 0 o j = 0
    L(i,j) = L(i-1,j-1) + 1            si x[i] = y[j]
    L(i,j) = max(L(i-1,j), L(i,j-1))   en otro caso

Esto se puede hacer porque el problema cumple el principio de optimalidad: una LCS óptima
contiene LCS óptimas de los prefijos.

## 3. Versiones implementadas

### 3.1. Versión A: recursiva directa (Tema 1)

Función `lcs_recursiva`. Aplica la recurrencia tal cual, sin guardar resultados. Cuando
los símbolos no coinciden hace dos llamadas, y muchos subproblemas se calculan una y otra
vez.

- Recurrencia en el peor caso: T(k) = 2T(k-1) + c, con k = m + n
- Tiempo: Θ(2^(m+n)), exponencial
- Memoria: O(m+n), solo la pila de recursión

Solo es viable para cadenas muy cortas, por eso en los experimentos se mide únicamente
con tamaños de 8 a 16 símbolos.

### 3.2. Versión B: Hirschberg, divide y conquista (Tema 2)

Función `lcs_hirschberg`. Pasos:

1. **Dividir:** se parte X por la mitad.
2. Con la función `_ultima_fila`, que solo guarda dos filas de la tabla, se calcula la
   última fila para la primera mitad de X frente a Y, y para la segunda mitad invertida
   frente a Y invertida.
3. El punto k de Y que maximiza la suma de ambas filas indica dónde cortar Y.
4. **Resolver:** se llama recursivamente con (X1, Y[:k]) y (X2, Y[k:]).
5. **Combinar:** se concatenan las dos soluciones.

- Tiempo: O(mn). Cada nivel cuesta la mitad que el anterior, así que el total queda
  en unas 2·mn operaciones.
- Memoria: O(m+n). Es su gran ventaja frente a la versión C.

### 3.3. Versión C: programación dinámica tabular (Tema 3)

Función `lcs_dp`. Rellena una tabla `L[m+1][n+1]` por filas, de modo que cada celda se
calcula una sola vez a partir de sus vecinas. Después reconstruye la secuencia recorriendo
la tabla hacia atrás desde `L[m][n]`.

- Tiempo: O(mn)
- Memoria: O(mn), por la tabla completa

Como comprobación, con las cadenas del Entrenamiento 3 del Tema 3 devuelve
`GTCGTCGGAAGCCGGCCGAA` (longitud 20), igual que el material de la asignatura.

## 4. Estructura del repositorio

    lcs/
    ├── lcs.py            Las tres versiones y un ejemplo ejecutable
    ├── tests.py          Juego de pruebas (206 casos)
    ├── experimentos.py   Mediciones de tiempo y memoria
    ├── Makefile          Ejecución con un único comando
    ├── README.md         Este archivo
    └── resultados/       Se genera al ejecutar los experimentos
        ├── mediciones.csv
        └── grafica.png

No se ha usado ninguna librería que resuelva la LCS; todo el código es propio.

## 5. Requisitos

- Python 3.8 o superior
- matplotlib (opcional, solo para generar la gráfica):

      pip install matplotlib

Si matplotlib no está instalado, los experimentos se ejecutan igual y solo se genera
el CSV.

## 6. Cómo ejecutarlo

### Con un único comando (Linux / Mac, o Windows con make)

    make

Ejecuta primero las pruebas y después los experimentos.

### En Windows con PowerShell

    cd ruta\a\la\carpeta\lcs
    py tests.py
    py experimentos.py
    py lcs.py ABCBDAB BDCABA

### Otros comandos

    make test     solo las pruebas
    make exp      solo los experimentos
    make demo     ejemplo del Tema 3
    python lcs.py CADENA1 CADENA2    LCS de dos cadenas cualquiera

## 7. Pruebas

`tests.py` comprueba 206 casos:

- Casos límite: cadenas vacías, cadenas iguales y cadenas sin símbolos en común.
- Ejemplos conocidos con resultado verificado a mano (`ABCBDAB` / `BDCABA` da longitud 4).
- 200 parejas aleatorias sobre el alfabeto {A, C, G, T} de hasta 10 símbolos.

Para cada caso se verifica que:

1. Las tres versiones devuelven la misma longitud.
2. El resultado es realmente una subsecuencia de las dos cadenas.

No se compara el texto exacto, porque puede haber varias LCS válidas.

Salida esperada:

    OK: 206 casos superados

## 8. Diseño de los experimentos

- **Datos:** cadenas aleatorias sobre {A, C, G, T}, simulando secuencias de ADN, con
  semilla fija (2025) para que los resultados se puedan repetir.
- **Serie grande:** cinco parejas de 100, 250, 500, 750 y 1000 símbolos, con las
  versiones B y C.
- **Serie pequeña:** cinco parejas de 8, 10, 12, 14 y 16 símbolos, con las tres
  versiones. Es la única forma de medir la versión A, ya que con tamaños grandes no
  terminaría.
- **Tiempo:** tiempo de CPU con `time.process_time()`. En Windows este reloj solo avanza
  cada 15,6 ms aproximadamente, así que cada algoritmo se repite hasta acumular al menos
  0,2 s y se divide entre el número de repeticiones. De varias rondas se toma el mínimo,
  para reducir el ruido del sistema.
- **Memoria:** pico de memoria medido con `tracemalloc`.

Los resultados se guardan en `resultados/mediciones.csv` con las columnas:

    serie, n, version, cpu_s, mem_pico_KiB, long_lcs

y en `resultados/grafica.png` se dibujan el tiempo y la memoria de B y C frente a n.

## 9. Resultados esperados

Los tiempos exactos dependen del equipo, pero la tendencia debe ser la siguiente:

- **C es la más rápida**, y B tarda aproximadamente el doble, como se predice en el
  análisis teórico.
- **Al duplicar n** (de 500 a 1000), el tiempo de B y C se multiplica por unas 4 veces,
  lo que encaja con O(mn).
- **La memoria de C crece de forma cuadrática** (varios MiB con n = 1000), mientras que
  la de B se mantiene en unas decenas de KiB.
- **La versión A crece de forma exponencial:** con solo 16 símbolos ya tarda una parte
  apreciable de segundo.

## 10. Conclusiones

- La versión recursiva es la más fácil de escribir, pero repite subproblemas y su coste
  es exponencial. Solo sirve para entender el problema.
- La programación dinámica elimina esa repetición y es la opción más rápida para
  cadenas de tamaño medio, a cambio de ocupar O(mn) de memoria.
- Hirschberg mantiene el tiempo O(mn) y reduce la memoria a O(m+n), así que es la
  mejor opción cuando las cadenas son tan largas que la tabla no cabe en memoria.

## 11. Referencias

- Guerequeta, R. y Vallecillo, A. (1998). *Técnicas de diseño de algoritmos*.
  Universidad de Málaga.
- Hirschberg, D. S. (1975). A linear space algorithm for computing maximal common
  subsequences. *Communications of the ACM*, 18(6), 341-343.
- UNIR. Diseño Avanzado de Algoritmos, Temas 1, 2 y 3.
