with Ada.Text_IO; use Ada.Text_IO;

package body Matriz_Operaciones is

   function Producto_Transpuesta(A : Matriz_Dinamica; N : Positive) return Matriz_Dinamica is
      B : Matriz_Dinamica(1..N, 1..N);
   begin
      for I in 1..N loop
         for J in 1..N loop
            B(I,J) := 0;
            for K in 1..N loop
               B(I,J) := B(I,J) + A(I,K) * A(J,K);
            end loop;
         end loop;
      end loop;
      return B;
   end Producto_Transpuesta;

   procedure Imprimir_Matriz(M : Matriz_Dinamica; N : Positive) is
   begin
      for I in 1..N loop
         for J in 1..N loop
            Put(M(I,J)'Img & " ");
         end loop;
         New_Line;
      end loop;
   end Imprimir_Matriz;

end Matriz_Operaciones;
