// Implementación del algoritmo Mergesort en V
fn mergesort(mut a []int) {
	if a.len <= 1 {
		return
	}

	// Se divide el arreglo en dos mitades
	mid := a.len / 2
	mut left := a[..mid]
	mut right := a[mid..]

	// Ordenar recursivamente ambas mitades
	mergesort(mut left)
	mergesort(mut right)

	// Combinar los resultados en 'a'
	mut i := 0
	mut j := 0
	mut k := 0

	for i < left.len && j < right.len {
		if left[i] <= right[j] {
			a[k] = left[i]
			i++
		} else {
			a[k] = right[j]
			j++
		}
		k++
	}

	// Copiar los elementos restantes
	for i < left.len {
		a[k] = left[i]
		i++
		k++
	}
	for j < right.len {
		a[k] = right[j]
		j++
		k++
	}
}

fn main() {
	mut datos := [235, 124, 15, 1, 654, 4, 23, 9, 0, 87]
	println('Arreglo original: $datos')
	mergesort(mut datos)
	println('Arreglo ordenado:  $datos')
}

