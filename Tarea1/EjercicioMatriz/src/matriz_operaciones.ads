package Matriz_Operaciones is
   -- Tipo de matriz dinámica
   type Matriz_Dinamica is array (Positive range <>, Positive range <>) of Integer;

   -- Función para calcular A * A^T
   function Producto_Transpuesta(A : Matriz_Dinamica; N : Positive) return Matriz_Dinamica;

   -- Procedimiento para imprimir matrices
   procedure Imprimir_Matriz(M : Matriz_Dinamica; N : Positive);
end Matriz_Operaciones;
