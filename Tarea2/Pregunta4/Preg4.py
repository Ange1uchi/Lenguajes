from functools import lru_cache

# calcula a y b a partir de X, Y, Z
# ttomo (X+Y) mod 5 + 3 y (Y+Z) mod 5 + 3
def compute_alpha_beta(X: int, Y: int, Z: int) -> tuple[int, int]:
    a = ((X + Y) % 5) + 3
    b = ((Y + Z) % 5) + 3
    return a, b

# versión recursiva directa según la definición matemática
# esta es la traducción literal: si n < a*b devuelve n,
# sino suma F(n - b), F(n - 2b), ..., F(n - a*b)
# ojo: esta versión explota exponencialmente sin memo
def fab_recursive(n: int, a: int, b: int) -> int:
    if n < a * b:
        return n
    s = 0
    for i in range(1, a + 1):
        s += fab_recursive(n - b * i, a, b)
    return s

# misma recursión pero con memoización usando lru_cache
# esto convierte la exponencial en algo mucho más manejable
# nota: lru_cache guarda resultados por (n,a,b), si cambio a o b
# conviene limpiar la caché con fab_recursive_memo.cache_clear()
@lru_cache(maxsize=None)
def fab_recursive_memo(n: int, a: int, b: int) -> int:
    if n < a * b:
        return n
    # más compacto
    return sum(fab_recursive_memo(n - b * i, a, b) for i in range(1, a + 1))

# versión recursiva de cola que construye la secuencia con una cola
# en realidad Python no optimiza tail calls, así que lo hago iterativo pero
# con una función helper recursiva que simplemente itera añadiendo a dp.
# dp guarda los valores F(0)..F(k-1) y voy calculando el siguiente.
def fab_tail(n: int, a: int, b: int) -> int:
    base_len = a * b
    # inicializo dp con la base F(0)=0, F(1)=1, ..., F(base_len-1)=base_len-1
    dp = [k for k in range(min(n + 1, base_len))]
    if n < base_len:
        return dp[n]

    def helper(k: int) -> int:
        # k es el índice que vamos a calcular ahora; si ya pasamos n, devolvemos
        if k > n:
            return dp[n]
        # calculo F(k) sumando las a entradas anteriores que corresponden
        # a los saltos de tamaño b: F(k-b), F(k-2b), ..., F(k-ab)
        val = 0
        for i in range(1, a + 1):
            val += dp[k - b * i]
        dp.append(val)
        # llamo de nuevo para el siguiente índice; comoun bucle
        return helper(k + 1)

    return helper(base_len)

# versión iterativa con programación dinámica (bottom-up)
# esta es la más clara y eficiente en Python: construye dp[0..n]
def fab_iterative(n: int, a: int, b: int) -> int:
    base_len = a * b
    if n < base_len:
        return n
    # dp[k] guardará F(k)
    dp = [0] * (n + 1)
    # valores base
    for k in range(base_len):
        dp[k] = k
    # construyo hacia adelante usando la relación de recurrencia
    for k in range(base_len, n + 1):
        dp[k] = sum(dp[k - b * i] for i in range(1, a + 1))
    return dp[n]

if __name__ == "__main__":
    # ejemplos de uso, pocos y directos para probar que funciona
    # ejemplo: caso que equivale a Fibonacci clásico generalizado
    a, b = 2, 1
    n = 10
    print("Fibonacci generalizado (a=2,b=1):")
    print("  recursiva (memo) :", fab_recursive_memo(n, a, b))
    print("  tail-recursive   :", fab_tail(n, a, b))
    print("  iterativa        :", fab_iterative(n, a, b))

    # otro ejemplo con a=3, b=4
    a, b = 3, 4
    n = 20
    # limpio caché porque a y b cambiaron
    fab_recursive_memo.cache_clear()
    print("\nF_{3,4}(n):")
    print("  recursiva (memo) :", fab_recursive_memo(n, a, b))
    print("  tail-recursive   :", fab_tail(n, a, b))
    print("  iterativa        :", fab_iterative(n, a, b))

    # ejemplo usando X,Y,Z (descomentar para probar)
    # X, Y, Z = 7, 11, 5
    # a, b = compute_alpha_beta(X, Y, Z)
    # print(f"\nCon X={X}, Y={Y}, Z={Z} -> a={a}, b={b}")
    # print("F_{a,b}(n) iterativo:", fab_iterative(50, a, b))
