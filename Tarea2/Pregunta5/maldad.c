#include <stdio.h>

#ifdef __cplusplus ///Si el compilador detecta que el código se está compilando como C++,
  #include <cmath> // entonces incluye <cmath> en lugar de <math.h>.
  using std::log;   
  using std::floor;
#else
  #include <math.h> // Si no (o sea, si es C u Objective-C), usa <math.h> normalmente.
#endif

double tribonacci(double n) {
    if (n >= 0 && n < 3) {
        return n;
    }
    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3);
}

double factorial(double n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

double comb(double n, double k) {
    return factorial(n) / (factorial(k) * factorial(n - k));
}

double logaritmo2(double x) {
    return log(x) / log(2.0);
}

double narayana(double n, double k) {
    return (1.0 / n) * comb(n, k) * comb(n, k - 1);
}

double maldad(double n) {
    int index = (int)floor(logaritmo2(narayana(n, (int)logaritmo2(n)))) + 1;
    return tribonacci(index);
}

int main(void) {
    int n;
    printf("Ingresa un numero: ");
    scanf("%d", &n);
    printf("%f", maldad(n));
    return 0;
}
