#ifndef VECTOR3_HPP
#define VECTOR3_HPP

#include <cmath>      // Para funciones matematicas como sqrt y fabs
#include <iostream>   // Para std::ostream

// Clase que representa un vector en 3D
class Vector3 {
public:
    double x, y, z; // Componentes del vector

    // Constructor por defecto: inicializa todo en 0
    Vector3() : x(0), y(0), z(0) {}

    // Constructor con parametros
    Vector3(double x_, double y_, double z_) : x(x_), y(y_), z(z_) {}

    // --- Operaciones con escalares (solo por la derecha) ---

    // Suma escalar: suma un escalar a cada componente
    Vector3 operator+(double scalar) const {
        return {x + scalar, y + scalar, z + scalar};
    }

    // Multiplicacion escalar: multiplica cada componente por un escalar
    Vector3 operator*(double scalar) const {
        return {x * scalar, y * scalar, z * scalar};
    }

    // Division escalar: divide cada componente por un escalar
    Vector3 operator/(double scalar) const {
        return {x / scalar, y / scalar, z / scalar};
    }

    // Resta escalar: resta un escalar a cada componente
    Vector3 operator-(double scalar) const {
        return {x - scalar, y - scalar, z - scalar};
    }

    // --- Operaciones entre vectores ---

    // Suma vectorial: suma componente a componente
    Vector3 operator+(const Vector3& other) const {
        return {x + other.x, y + other.y, z + other.z};
    }

    // Producto cruz (operador *): calcula el producto vectorial
    Vector3 operator*(const Vector3& other) const {
        return {
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        };
    }

    // Resta vectorial: resta componente a componente
    Vector3 operator-(const Vector3& other) const {
        return {x - other.x, y - other.y, z - other.z};
    }

    // Producto punto (operador %): calcula el producto escalar
    double operator%(const Vector3& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    // Norma (operador &): calcula la magnitud del vector
    double operator&() const {
        return std::sqrt(x * x + y * y + z * z);
    }

    // --- Comparacion con tolerancia ---

    // Compara dos vectores con una tolerancia (por si hay errores de punto flotante)
    bool equals(const Vector3& other, double eps = 1e-6) const {
        return std::fabs(x - other.x) < eps &&
               std::fabs(y - other.y) < eps &&
               std::fabs(z - other.z) < eps;
    }

    // --- Mostrar vector ---

    // Sobrecarga del operador << para imprimir el vector facilmente
    friend std::ostream& operator<<(std::ostream& os, const Vector3& v) {
        os << "(" << v.x << ", " << v.y << ", " << v.z << ")";
        return os;
    }
};

#endif
