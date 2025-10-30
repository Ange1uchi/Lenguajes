from fab import compute_alpha_beta, fab_recursive_memo, fab_tail, fab_iterative

a,b = compute_alpha_beta(4,3,6)
print(f"Probando F_{{{a},{b}}}(n)")

for n in range(a*b, a*b+600, 10):
    fab_recursive_memo.cache_clear()
    v1 = fab_recursive_memo(n,a,b)
    v2 = fab_tail(n,a,b)
    v3 = fab_iterative(n,a,b)
    assert v1==v2==v3, f"Error en n={n}: {v1},{v2},{v3}"

print("Todos los n probados son iguales.")
