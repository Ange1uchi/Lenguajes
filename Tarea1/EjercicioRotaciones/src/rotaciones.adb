with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

package body Rotaciones is

   function Rotar(W : Unbounded_String; K : Natural) return Unbounded_String is
      N : Natural := Length(W);
      K_Normalized : Natural := (if N > 0 then K mod N else 0);
      First_Char : Character;
      Rest       : Unbounded_String;
   begin
      if K_Normalized = 0 or else N = 0 then
         return W;
      else
         -- Extraer primer carácter y resto
         First_Char := To_String(W)(1);
         Rest := To_Unbounded_String(To_String(W)(2..N));
         
         -- Concatenar: convertir Character a String antes de To_Unbounded_String
         return Rotar(Rest & To_Unbounded_String(String'(First_Char)), K_Normalized - 1);
      end if;
   end Rotar;

end Rotaciones;
