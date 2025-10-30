import os

// Función que calcula la cantidad de pasos para llegar a 1
fn collatz_count(n u64) u32 {
	mut x := n         // variable mutable que representa el número actual
	mut steps := u32(0)   // contador de pasos

	for x != 1 {       // bucle que se repite mientras el número sea distinto de 1
		if x % 2 == 0 {       // si el número es par
			x /= 2             // se divide entre 2
		} else {              // si el número es impar
			x = 3 * x + 1      // se aplica la fórmula 3n + 1
		}
		steps++               // se incrementa el contador
	}
	return steps              // devuelve la cantidad total de pasos
}

// Programa principal
fn main() {
	input := os.input('Ingrese un número entero positivo: ').trim_space()
	n := input.u64()                     // conversión de texto a número sin signo
	println('Cantidad de pasos: ${collatz_count(n)}')
}
