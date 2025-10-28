module main
// expr_test.v — pruebas unitarias para expr.v

// Helpers para evitar repetir código en los tests
fn assert_eval(order string, expr string, want i64) {
	toks := tokenize(expr)
	root := parse(order, toks)
	got := eval(root)
	assert got == want, 'EVAL $order $expr => got $got, want $want'
}

fn assert_infix(order string, expr string, want string) {
	toks := tokenize(expr)
	root := parse(order, toks)
	got := to_infix(root)
	assert got == want, 'MOSTRAR $order $expr => got "$got", want "$want"'
}

// ===== Casos del enunciado =====
fn test_eval_enunciado_1() {
	assert_eval('PRE', '+ * + 3 4 5 7', 42)
}
fn test_mostrar_enunciado_1() {
	assert_infix('PRE', '+ * + 3 4 5 7', '(3 + 4) * 5 + 7')
}
fn test_eval_enunciado_2() {
	assert_eval('POST', '8 3 - 8 4 4 + * +', 69)
}
fn test_mostrar_enunciado_2() {
	assert_infix('POST', '8 3 - 8 4 4 + * +', '8 - 3 + 8 * (4 + 4)')
}

// ===== Precedencia y asociatividad  =====
fn test_mostrar_precedencia_sin_parentesis_extras() {
	assert_infix('PRE', '+ 5 * 3 4', '5 + 3 * 4') // * tiene mayor precedencia
}
fn test_mostrar_misma_precedencia_no_asociativa_requiere_parentesis() {
	// (8 - 3) - 2  vs  8 - (3 - 2)
	assert_infix('PRE', '- - 8 3 2', '8 - 3 - 2')   // Por asociatividad a izquierda, esto ya significa (8 - 3) - 2 entonces es correcto no poner paréntesis
	assert_infix('PRE', '- 8 - 3 2', '8 - (3 - 2)')   // hijo derecho '-'
}
fn test_mostrar_division_no_asociativa() {
	// (12 / 3) / 2  vs  12 / (3 / 2)
	assert_infix('PRE', '/ / 12 3 2', '12 / 3 / 2')  // Por asociatividad a izquierda, esto ya significa (12 / 3) / 2 entonces es correcto no poner paréntesis
	assert_infix('PRE', '/ 12 / 3 2', '12 / (3 / 2)') // hijo derecho '/'
}
fn test_mostrar_mixta_mas_menos_y_por_div() {
	assert_infix('PRE', '+ - 8 3 * 8 + 4 4', '8 - 3 + 8 * (4 + 4)')
}

// ===== Evaluación adicional =====
fn test_eval_anidado() {
	assert_eval('PRE', '- * 10 + 1 1 5', 15) // (10*(1+1)) - 5
}
fn test_eval_division_entera() {
	assert_eval('PRE', '/ * 10 4 2', 20)     // (10*4)/2 = 20
}

// ===== Postfix más largo =====
fn test_postfix_largo_eval_y_mostrar() {
	assert_infix('POST', '5 1 2 + 4 * + 3 -', '5 + (1 + 2) * 4 - 3')
	assert_eval('POST', '5 1 2 + 4 * + 3 -', 14)
}
