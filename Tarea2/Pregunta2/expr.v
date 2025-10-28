
module main
// Calculadora de expresiones en notación PRE y POST
// Lenguaje: V 
// El programa puede evaluar o mostrar expresiones con +, -, *, /
// usando enteros. Soporta los comandos EVAL, MOSTRAR y SALIR.

import os

// Estructura de nodo para el árbol
// Cada nodo puede ser un número o un operador
enum Kind { num op }

struct Node {
	kind Kind
	val i64
	op string
	left &Node = unsafe { nil }
	right &Node = unsafe { nil }
}

// Separa la entrada en tokens usando espacios
fn tokenize(s string) []string {
	return s.split_any(' \t\r\n').filter(it.len > 0)
}

// Verifica si el token es un operador (+ - * /)
fn is_op(t string) bool {
	return t in ['+', '-', '*', '/']
}

// Estructura auxiliar para manejar los tokens en PRE
struct TStream {
	tokens []string
mut:
	i int
}

fn (mut ts TStream) next() ?string {
	if ts.i >= ts.tokens.len { return none }
	t := ts.tokens[ts.i]
	ts.i++
	return t
}

// --- Parser para expresiones en orden PRE (prefijo) ---
fn parse_prefix(mut ts TStream) &Node {
	t := ts.next() or { panic('Expresión prefix incompleta') }
	if is_op(t) {
		// si es operador, creo dos subárboles (izq y der)
		l := parse_prefix(mut ts)
		r := parse_prefix(mut ts)
		return &Node{ kind: .op, op: t, left: l, right: r }
	} else {
		// si no es operador, es número
		return &Node{ kind: .num, val: t.i64() }
	}
}

// --- Parser para expresiones POST (postfijo) ---
fn parse_postfix(tokens []string) &Node {
	mut st := []&Node{}
	for t in tokens {
		if is_op(t) {
			// los dos últimos son los operandos
			if st.len < 2 {
				panic('Expresión postfix incompleta')
			}
			r := st.pop()
			l := st.pop()
			st << &Node{ kind: .op, op: t, left: l, right: r }
		} else {
			// si es número, lo meto en la pila
			st << &Node{ kind: .num, val: t.i64() }
		}
	}
	if st.len != 1 {
		panic('Expresión POST inválida (sobran operandos)')
	}
	return st[0]
}

// --- Evalúa el árbol recursivamente ---
fn eval(n &Node) i64 {
	if n.kind == .num {
		return n.val
	}
	a := eval(n.left)
	b := eval(n.right)
	match n.op {
		'+' { return a + b }
		'-' { return a - b }
		'*' { return a * b }
		'/' { return a / b } // división entera
		else { panic('Operador desconocido') }
	}
}

// --- Funciones auxiliares para imprimir en forma infija ---
fn prec(op string) int {
	return if op in ['+', '-'] { 1 } else { 2 }
}

// Determina si un subárbol necesita paréntesis
fn needs_paren(parent_op string, child &Node, is_right bool) bool {
	if child.kind == .num { return false }
	cp := prec(child.op)
	pp := prec(parent_op)
	if cp < pp { return true }
	if cp > pp { return false }
	if !is_right { return false }
	// casos no asociativos
	match parent_op {
		'+' { return child.op == '-' }
		'-' { return child.op in ['+', '-'] }
		'*' { return child.op == '/' }
		'/' { return child.op in ['*', '/'] }
		else { return false }
	}
}

// Convierte el árbol a forma infija con paréntesis mínimos
fn to_infix(n &Node) string {
	if n.kind == .num { return n.val.str() }

	ls := to_infix(n.left)
	rs := to_infix(n.right)

	mut l := ls
	mut r := rs

	if needs_paren(n.op, n.left, false) {
		l = '(${ls})'
	}
	if needs_paren(n.op, n.right, true) {
		r = '(${rs})'
	}
	return '${l} ${n.op} ${r}'
}

// Decide si usar parser PRE o POST
fn parse(order string, expr_tokens []string) &Node {
	return match order {
		'PRE' {
			mut ts := TStream{ tokens: expr_tokens }
			mut root := parse_prefix(mut ts)
			if ts.i != ts.tokens.len {
				panic('Sobran tokens en PRE')
			}
			root
		}
		'POST' { parse_postfix(expr_tokens) }
		else { panic('Orden debe ser PRE o POST') }
	}
}

// --- Programa principal (REPL) ---
fn main() {
	println('Calculadora PRE/POST (+ - * /)')
	println('Comandos: EVAL/MOSTRAR PRE|POST <expr>  |  SALIR')

	for {
		line := os.input('> ').trim_space()

		if line.len == 0 { continue }
		if line.to_upper() == 'SALIR' { break }

		toks := tokenize(line)
		if toks.len < 3 {
			println('Entrada inválida. Ejemplos:')
			println('  EVAL PRE + * + 3 4 5 7')
			println('  MOSTRAR POST 8 3 - 8 4 4 + * +')
			continue
		}

		action := toks[0].to_upper()
		order := toks[1].to_upper()
		expr_toks := toks[2..]

		if order != 'PRE' && order != 'POST' {
			println('Orden inválida, usa PRE o POST.')
			continue
		}

		// construir árbol sintáctico
		root := parse(order, expr_toks)

		// ejecutar la acción
		match action {
			'EVAL' {
				println(eval(root))
			}
			'MOSTRAR' {
				println(to_infix(root))
			}
			else {
				println('Acción no reconocida.')
			}
		}
	}
}
