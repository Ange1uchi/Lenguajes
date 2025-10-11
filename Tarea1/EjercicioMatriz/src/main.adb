with Ada.Text_IO; use Ada.Text_IO;
with Matriz_Operaciones; use Matriz_Operaciones;

procedure Main is
   -- Tamaño de la matriz (Hay que modificar este valor si se cambia la matriz A)
   N : constant Positive := 5;

   -- Declaramos la matriz A usando el tipo del paquete
   A : Matriz_Dinamica := (
   1 => (3,  5,  7,  2,  6),
   2 => (1,  4,  9,  8,  3),
   3 => (2,  6,  5,  7,  4),
   4 => (8,  3,  1,  9,  2),
   5 => (4,  7,  2,  5,  8)
   );


   B : Matriz_Dinamica(1..N, 1..N);
begin
   -- Calculamos A * A^T
   B := Producto_Transpuesta(A, N);

   -- Mostramos la matriz resultante
   Put_Line("Matriz A * A^T:");
   Imprimir_Matriz(B, N);
end Main;
