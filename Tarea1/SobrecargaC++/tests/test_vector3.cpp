#include "../src/vector3.hpp"
#include <cassert>
#include <iostream>
#include <cmath>
#include <sstream>

#define EPS 1e-6 // Tolerancia para comparaciones de punto flotante

// Prueba de suma de vectores
void test_sum() {
    Vector3 a(1, 2, 3);
    Vector3 b(3, 2, 1);
    Vector3 result = a + b;
    assert(result.equals({4, 4, 4}, EPS));
    std::cout << "Suma correcta\n";
}

// Prueba de resta de vectores
void test_subtraction() {
    Vector3 a(5, 4, 3);
    Vector3 b(1, 2, 3);
    Vector3 result = a - b;
    assert(result.equals({4, 2, 0}, EPS));
    std::cout << "Resta correcta\n";
}

// Prueba de producto cruz
void test_cross() {
    Vector3 a(1, 0, 0);
    Vector3 b(0, 1, 0);
    Vector3 result = a * b;
    assert(result.equals({0, 0, 1}, EPS));
    std::cout << "Producto cruz correcto\n";
}

// Prueba de producto punto
void test_dot() {
    Vector3 a(1, 2, 3);
    Vector3 b(4, -5, 6);
    double result = a % b;
    assert(std::fabs(result - (1*4 + 2*(-5) + 3*6)) < EPS);
    std::cout << "Producto punto correcto\n";
}

// Prueba de norma de un vector
void test_norm() {
    Vector3 a(3, 4, 0);
    double norm = &a;
    assert(std::fabs(norm - 5.0) < EPS);
    std::cout << "Norma correcta\n";
}

// Prueba de operaciones con escalares
void test_scalar_operations() {
    Vector3 b(1, 2, 3);
    Vector3 result = b + 3.0;
    assert(result.equals({4, 5, 6}, EPS));
    result = b - 1.0;
    assert(result.equals({0, 1, 2}, EPS));
    result = b * 2.0;
    assert(result.equals({2, 4, 6}, EPS));
    result = b / 2.0;
    assert(result.equals({0.5, 1.0, 1.5}, EPS));
    std::cout << "Operaciones con escalares correctas\n";
}

// Prueba de constructores
void test_constructors() {
    Vector3 a;
    assert(a.equals({0, 0, 0}, EPS));
    Vector3 b(1.5, 2.5, 3.5);
    assert(b.equals({1.5, 2.5, 3.5}, EPS));
    std::cout << "Constructores correctos\n";
}

// Prueba de casos borde
void test_edge_cases() {
    Vector3 zero;
    Vector3 a(1, 2, 3);
    Vector3 result = a + zero;
    assert(result.equals(a, EPS));
    result = a - zero;
    assert(result.equals(a, EPS));
    result = a * zero;
    assert(result.equals(zero, EPS));
    double dot = a % zero;
    assert(std::fabs(dot - 0.0) < EPS);
    double norm = &zero;
    assert(std::fabs(norm - 0.0) < EPS);
    std::cout << "Casos edge correctos\n";
}

// Prueba con vectores negativos
void test_negative_vectors() {
    Vector3 a(-1, -2, -3);
    Vector3 b(-4, -5, -6);
    Vector3 result = a + b;
    assert(result.equals({-5, -7, -9}, EPS));
    double dot = a % b;
    assert(std::fabs(dot - (4 + 10 + 18)) < EPS);
    double norm = &a;
    assert(std::fabs(norm - std::sqrt(1+4+9)) < EPS);
    std::cout << "Vectores negativos correctos\n";
}

// Prueba de operaciones mixtas
void test_mixed_operations() {
    Vector3 a(1, 2, 3);
    Vector3 b(4, 5, 6);
    Vector3 c(7, 8, 9);
    Vector3 result = (a + b) * c;
    Vector3 expected = (Vector3(5, 7, 9)) * c;
    assert(result.equals(expected, EPS));
    result = (a * 2.0) + (b / 2.0);
    expected = Vector3(2, 4, 6) + Vector3(2, 2.5, 3);
    assert(result.equals(expected, EPS));
    std::cout << "Operaciones mixtas correctas\n";
}

// Prueba de vectores ortogonales
void test_orthogonal_vectors() {
    Vector3 a(1, 0, 0);
    Vector3 b(0, 1, 0);
    Vector3 c(0, 0, 1);
    assert(std::fabs(a % b) < EPS);
    assert(std::fabs(a % c) < EPS);
    assert(std::fabs(b % c) < EPS);
    std::cout << "Vectores ortogonales correctos\n";
}

// Prueba del operador de salida
void test_output_operator() {
    Vector3 a(1.5, 2.5, 3.5);
    std::cout << "Vector a: " << a << std::endl;
    std::cout << "Operador de salida correcto\n";
}

// Prueba de equals con tolerancia
void test_equals_tolerance() {
    Vector3 a(1.0, 2.0, 3.0);
    Vector3 b(1.0000005, 2.0000005, 3.0000005);
    Vector3 c(1.1, 2.1, 3.1);
    assert(a.equals(b));
    assert(!a.equals(c));
    assert(a.equals(c, 0.2));
    std::cout << "Tolerancia en equals correcta\n";
}

// Prueba de operaciones de asignacion
void test_assignment_operations() {
    Vector3 a(1, 2, 3);
    Vector3 b(4, 5, 6);
    Vector3 c = a + b - a;
    assert(c.equals(b, EPS));
    Vector3 d = a * 2.0 + b / 2.0;
    Vector3 expected = Vector3(2, 4, 6) + Vector3(2, 2.5, 3);
    assert(d.equals(expected, EPS));
    std::cout << "Operaciones de asignacion correctas\n";
}

// Prueba de vectores paralelos
void test_parallel_vectors() {
    Vector3 a(2, 4, 6);
    Vector3 b(1, 2, 3);
    Vector3 cross = a * b;
    assert(cross.equals(Vector3(0, 0, 0), EPS));
    double dot = a % b;
    double expected_dot = 2*1 + 4*2 + 6*3;
    assert(std::fabs(dot - expected_dot) < EPS);
    std::cout << "Vectores paralelos correctos\n";
}

// Prueba de vectores unitarios
void test_unit_vectors() {
    Vector3 a(1, 0, 0);
    Vector3 b(0, 1, 0);
    Vector3 c(0, 0, 1);
    assert(std::fabs(&a - 1.0) < EPS);
    assert(std::fabs(&b - 1.0) < EPS);
    assert(std::fabs(&c - 1.0) < EPS);
    std::cout << "Vectores unitarios correctos\n";
}

// Prueba con numeros grandes
void test_large_numbers() {
    Vector3 a(1e6, 2e6, 3e6);
    Vector3 b(4e6, 5e6, 6e6);
    Vector3 sum = a + b;
    assert(sum.equals({5e6, 7e6, 9e6}, 1.0));
    double dot = a % b;
    double expected_dot = 1e6*4e6 + 2e6*5e6 + 3e6*6e6;
    assert(std::fabs(dot - expected_dot) < 1e6);
    std::cout << "Numeros grandes correctos\n";
}

// Prueba con numeros pequenos
void test_small_numbers() {
    Vector3 a(1e-6, 2e-6, 3e-6);
    Vector3 b(4e-6, 5e-6, 6e-6);
    Vector3 sum = a + b;
    assert(sum.equals({5e-6, 7e-6, 9e-6}, 1e-10));
    double norm = &a;
    double expected_norm = std::sqrt(1e-12 + 4e-12 + 9e-12);
    assert(std::fabs(norm - expected_norm) < 1e-10);
    std::cout << "Numeros pequenos correctos\n";
}

// main desordenado, igual funciona
int main() {
    test_constructors();
    test_sum();
    test_subtraction();
    test_cross();
    test_dot();
    test_norm();
    test_scalar_operations();
    test_edge_cases();
    test_negative_vectors();
    test_mixed_operations();
    test_orthogonal_vectors();
    test_output_operator();
    test_equals_tolerance();
    test_assignment_operations();
    test_parallel_vectors();
    test_unit_vectors();
    test_large_numbers();
    test_small_numbers();

    // Mensaje final
    std::cout << "\nTodas las pruebas pasaron correctamente\n";
    return 0;
}
