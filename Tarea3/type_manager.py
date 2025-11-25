#!/usr/bin/env python3
"""
Simulador de manejador de tipos de datos.

Soporta:
- ATOMICO <nombre> <representacion> <alineacion>
- STRUCT <nombre> <tipo>...
- UNION  <nombre> <tipo>...
- DESCRIBIR <nombre>
- LISTAR
- AYUDA
- SALIR
Angel Valero
Materia: CI3641 - Lenguajes de Programación I
"""

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional



#  Modelo de información

@dataclass
class LayoutInfo:
    """Información de layout de un tipo bajo una estrategia dada."""
    size: int
    alignment: int
    wasted: int
    internal_padding: int = 0
    final_padding: int = 0


class TypeInfo(ABC):
    """Clase base para todos los tipos manejados por el simulador."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def layout_unpacked(self) -> LayoutInfo:
        """Layout normal (sin empaquetar)."""
        ...

    @abstractmethod
    def layout_packed(self) -> LayoutInfo:
        """Layout empaquetado (alineación 1, sin padding)."""
        ...

    @abstractmethod
    def layout_optimal(self) -> LayoutInfo:
        """Layout reordenando campos de forma óptima."""
        ...

    @abstractmethod
    def kind(self) -> str:
        """Devuelve 'atomico', 'struct' o 'union'."""
        ...


class AtomicType(TypeInfo):
    """Tipo atómico: tamaño fijo y alineación fija."""

    def __init__(self, name: str, size: int, alignment: int):
        super().__init__(name)
        if size <= 0 or alignment <= 0:
            raise ValueError("Tamaño y alineación deben ser positivos")
        self._size = size
        self._alignment = alignment

    def layout_unpacked(self) -> LayoutInfo:
        # Sin padding para un atómico aislado.
        return LayoutInfo(
            size=self._size,
            alignment=self._alignment,
            wasted=0,
            internal_padding=0,
            final_padding=0,
        )

    def layout_packed(self) -> LayoutInfo:
        # Empaquetado: alineación 1, sin desperdicio extra.
        return LayoutInfo(
            size=self._size,
            alignment=1,
            wasted=0,
            internal_padding=0,
            final_padding=0,
        )

    def layout_optimal(self) -> LayoutInfo:
        # No aplica reordenamiento; igual al normal.
        return self.layout_unpacked()

    def kind(self) -> str:
        return "atomico"

    @property
    def size(self) -> int:
        return self._size

    @property
    def alignment(self) -> int:
        return self._alignment


class StructType(TypeInfo):
    """Registro (struct) compuesto por una lista de tipos."""

    def __init__(self, name: str, fields: List[TypeInfo]):
        super().__init__(name)
        if not fields:
            raise ValueError("Un struct debe tener al menos un campo")
        self.fields = fields

    def _compute_layout(
        self,
        field_alignments: Optional[List[int]] = None,
        reorder: bool = False,
    ) -> LayoutInfo:
        """
        Calcula layout generico de un struct.

        - field_alignments=None -> usar alignment de cada campo.
        - reorder=True -> reordenar campos por alineación descendente
          (solo tiene sentido cuando field_alignments es None).
        """
        if field_alignments is not None and len(field_alignments) != len(self.fields):
            raise ValueError("field_alignments debe tener mismo tamaño que fields")

        # Determinar el orden de los campos
        if reorder:
            # Reordenar por alineación descendente (layout óptimo)
            indexed_fields = list(enumerate(self.fields))
            indexed_fields.sort(
                key=lambda p: p[1].alignment if isinstance(p[1], AtomicType) else p[1].layout_unpacked().alignment,
                reverse=True,
            )
            order = [idx for idx, _ in indexed_fields]
        else:
            order = list(range(len(self.fields)))

        offset = 0
        internal_padding = 0

        # Alineación estructural = max alineación de campos (en caso normal/óptimo)
        if field_alignments is None:
            field_align_values = []
            for f in self.fields:
                if isinstance(f, AtomicType):
                    field_align_values.append(f.alignment)
                else:
                    field_align_values.append(f.layout_unpacked().alignment)
        else:
            field_align_values = field_alignments

        struct_alignment = max(field_align_values) if field_align_values else 1

        for idx in order:
            field = self.fields[idx]
            if field_alignments is None:
                # Alineaciones reales
                if isinstance(field, AtomicType):
                    align = field.alignment
                    size = field.size
                else:
                    lu = field.layout_unpacked()
                    align = lu.alignment
                    size = lu.size
            else:
                align = field_align_values[idx]
                if isinstance(field, AtomicType):
                    size = field.size
                else:
                    size = field.layout_unpacked().size

            # Mover offset al siguiente múltiplo de 'align'
            if align > 0:
                aligned_offset = ((offset + align - 1) // align) * align
            else:
                aligned_offset = offset
            pad = aligned_offset - offset
            internal_padding += pad
            offset = aligned_offset + size

        # Padding final para ajustar al múltiplo de struct_alignment
        if struct_alignment > 0:
            final_size = ((offset + struct_alignment - 1) // struct_alignment) * struct_alignment
        else:
            final_size = offset
        final_padding = final_size - offset

        total_wasted = internal_padding + final_padding

        return LayoutInfo(
            size=final_size,
            alignment=struct_alignment,
            wasted=total_wasted,
            internal_padding=internal_padding,
            final_padding=final_padding,
        )

    def layout_unpacked(self) -> LayoutInfo:
        # Layout normal usando las alineaciones reales de cada campo.
        return self._compute_layout(field_alignments=None, reorder=False)

    def layout_packed(self) -> LayoutInfo:
        # Empaquetado: se asume alineación = 1 para todos los campos y para el struct.
        # No hay padding interno ni final.
        total_size = 0
        for f in self.fields:
            if isinstance(f, AtomicType):
                total_size += f.size
            else:
                total_size += f.layout_unpacked().size

        return LayoutInfo(
            size=total_size,
            alignment=1,
            wasted=0,
            internal_padding=0,
            final_padding=0,
        )

    def layout_optimal(self) -> LayoutInfo:
        # Reordenamiento óptimo: ordenamos campos por alineación descendente.
        return self._compute_layout(field_alignments=None, reorder=True)

    def kind(self) -> str:
        return "struct"


class UnionType(TypeInfo):
    """Registro variante (union): todos los campos comienzan en offset 0."""

    def __init__(self, name: str, options: List[TypeInfo]):
        super().__init__(name)
        if not options:
            raise ValueError("Una union debe tener al menos una alternativa")
        self.options = options

    def _max_size_and_alignment_unpacked(self) -> Tuple[int, int]:
        max_size = 0
        max_align = 1
        for t in self.options:
            if isinstance(t, AtomicType):
                size = t.size
                align = t.alignment
            else:
                lu = t.layout_unpacked()
                size = lu.size
                align = lu.alignment
            max_size = max(max_size, size)
            max_align = max(max_align, align)
        return max_size, max_align

    def layout_unpacked(self) -> LayoutInfo:
        max_size, max_align = self._max_size_and_alignment_unpacked()
        # Ajustar tamaño al múltiplo de la alineación
        if max_align > 0:
            final_size = ((max_size + max_align - 1) // max_align) * max_align
        else:
            final_size = max_size
        wasted = final_size - max_size
        return LayoutInfo(
            size=final_size,
            alignment=max_align,
            wasted=wasted,
            internal_padding=0,
            final_padding=wasted,
        )

    def layout_packed(self) -> LayoutInfo:
        max_size, _ = self._max_size_and_alignment_unpacked()
        # Empaquetado: alineación 1, sin desperdicio extra.
        return LayoutInfo(
            size=max_size,
            alignment=1,
            wasted=0,
            internal_padding=0,
            final_padding=0,
        )

    def layout_optimal(self) -> LayoutInfo:
        # No tiene mucho sentido reordenar campos en una union,
        # así que igual que sin empaquetar.
        return self.layout_unpacked()

    def kind(self) -> str:
        return "union"


#  Manejador de tipos y comandos CLI
class TypeManager:
    """Maneja la tabla global de tipos y los comandos del usuario."""

    RESERVED_NAMES = {"ATOMICO", "STRUCT", "UNION", "DESCRIBIR", "SALIR", "AYUDA", "LISTAR"}

    def __init__(self):
        self.types: Dict[str, TypeInfo] = {}

    def _validate_type_name(self, name: str) -> None:
        if not name.isidentifier():
            raise ValueError(f"Nombre de tipo inválido: '{name}'. Debe ser un identificador válido.")
        if name.upper() in self.RESERVED_NAMES:
            raise ValueError(f"El nombre '{name}' está reservado como comando.")
        if name in self.types:
            raise ValueError(f"El tipo '{name}' ya está definido")

    @staticmethod
    def _validate_size_and_alignment(size: int, alignment: int) -> None:
        if size <= 0:
            raise ValueError("El tamaño debe ser positivo.")
        if alignment <= 0:
            raise ValueError("La alineación debe ser positiva.")

        def is_power_of_two(n: int) -> bool:
            return (n & (n - 1) == 0)

        if not is_power_of_two(alignment):
            raise ValueError(
                f"La alineación {alignment} no es potencia de 2. "
                f"En arquitecturas reales, la alineación típica es potencia de 2."
            )

    def add_atomic(self, name: str, size: int, alignment: int) -> None:
        self._validate_type_name(name)
        # Validación de tamaño/alineación aquí también, por si se usa sin el REPL
        self._validate_size_and_alignment(size, alignment)
        self.types[name] = AtomicType(name, size, alignment)

    def add_struct(self, name: str, field_names: List[str]) -> None:
        self._validate_type_name(name)
        if not field_names:
            raise ValueError("Un struct debe tener al menos un tipo de campo")
        fields: List[TypeInfo] = []
        for fn in field_names:
            t = self.types.get(fn)
            if t is None:
                raise ValueError(f"Tipo de campo '{fn}' no está definido")
            fields.append(t)
        self.types[name] = StructType(name, fields)

    def add_union(self, name: str, option_names: List[str]) -> None:
        self._validate_type_name(name)
        if not option_names:
            raise ValueError("Una union debe tener al menos un tipo")
        options: List[TypeInfo] = []
        for on in option_names:
            t = self.types.get(on)
            if t is None:
                raise ValueError(f"Tipo de alternativa '{on}' no está definido")
            options.append(t)
        self.types[name] = UnionType(name, options)

    def describe(self, name: str) -> str:
        t = self.types.get(name)
        if t is None:
            raise ValueError(f"El tipo '{name}' no está definido")

        lu = t.layout_unpacked()
        lp = t.layout_packed()
        lo = t.layout_optimal()

        lines: List[str] = []
        lines.append(f"Tipo: {name}")
        lines.append(f"Clase: {t.kind()}")
        lines.append("")
        lines.append("--- Sin empaquetar ---")
        lines.append(f"Tamaño: {lu.size} bytes")
        lines.append(f"Alineación: {lu.alignment} bytes")
        lines.append(f"Bytes desperdiciados: {lu.wasted} bytes")
        lines.append("")
        lines.append("--- Empaquetado ---")
        lines.append(f"Tamaño: {lp.size} bytes")
        lines.append(f"Alineación: {lp.alignment} bytes")
        lines.append(f"Bytes desperdiciados: {lp.wasted} bytes")
        lines.append("")
        lines.append("--- Reordenamiento óptimo ---")
        lines.append(f"Tamaño: {lo.size} bytes")
        lines.append(f"Alineación: {lo.alignment} bytes")
        lines.append(f"Bytes desperdiciados: {lo.wasted} bytes")

        return "\n".join(lines)


def repl():  # pragma: no cover
    """
    Bucle interactivo sencillo.
    Lee comandos hasta 'SALIR'.
    """
    manager = TypeManager()
    print("Simulador de tipos de datos. Escriba SALIR para terminar.")
    print("Comandos: ATOMICO, STRUCT, UNION, DESCRIBIR, LISTAR, AYUDA, SALIR")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue

        parts = line.split()
        cmd = parts[0].upper()

        try:
            if cmd == "SALIR":
                print("Saliendo del simulador.")
                break

            elif cmd == "AYUDA":
                print("Comandos disponibles:")
                print("  ATOMICO <nombre> <representacion> <alineacion>")
                print("  STRUCT  <nombre> <tipo1> <tipo2> ...")
                print("  UNION   <nombre> <tipo1> <tipo2> ...")
                print("  DESCRIBIR <nombre>")
                print("  LISTAR  (muestra todos los tipos definidos)")
                print("  SALIR")

            elif cmd == "LISTAR":
                if not manager.types:
                    print("No hay tipos definidos.")
                else:
                    print("Tipos definidos:")
                    for name, t in manager.types.items():
                        print(f"  {name} ({t.kind()})")

            elif cmd == "ATOMICO":
                if len(parts) != 4:
                    print("Uso: ATOMICO <nombre> <representacion> <alineacion>")
                    continue
                name = parts[1]
                size = int(parts[2])
                alignment = int(parts[3])

                # Validación de tamaño y alineación
                TypeManager._validate_size_and_alignment(size, alignment)

                manager.add_atomic(name, size, alignment)
                print(f"Tipo atómico '{name}' registrado.")

            elif cmd == "STRUCT":
                if len(parts) < 3:
                    print("Uso: STRUCT <nombre> <tipo1> <tipo2> ...")
                    continue
                name = parts[1]
                field_names = parts[2:]
                manager.add_struct(name, field_names)
                print(f"Struct '{name}' registrado.")

            elif cmd == "UNION":
                if len(parts) < 3:
                    print("Uso: UNION <nombre> <tipo1> <tipo2> ...")
                    continue
                name = parts[1]
                option_names = parts[2:]
                manager.add_union(name, option_names)
                print(f"Union '{name}' registrada.")

            elif cmd == "DESCRIBIR":
                if len(parts) != 2:
                    print("Uso: DESCRIBIR <nombre>")
                    continue
                name = parts[1]
                desc = manager.describe(name)
                print(desc)

            else:
                print("Comando no reconocido. Use AYUDA para ver los comandos disponibles.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


if __name__ == "__main__":  # pragma: no cover
    repl()
