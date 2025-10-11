with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;
with Rotaciones; use Rotaciones;

procedure Main is
   W      : Unbounded_String := To_Unbounded_String("hola");
   Result : Unbounded_String;
begin
   -- Probamos rotaciones de 0 a 5
   for K in 0..5 loop
      Result := Rotar(W, K);
      Put_Line("rotar(""hola"", " & Natural'Image(K) & ") = """ & To_String(Result) & """");
   end loop;
end Main;
