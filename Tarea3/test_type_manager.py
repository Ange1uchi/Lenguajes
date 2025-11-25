import unittest
from type_manager import (
    AtomicType,
    StructType,
    UnionType,
    TypeManager,
)


class TestAtomicType(unittest.TestCase):
    def test_atomic_layouts(self):
        t = AtomicType("int", 4, 4)
        lu = t.layout_unpacked()
        lp = t.layout_packed()
        lo = t.layout_optimal()

        self.assertEqual(lu.size, 4)
        self.assertEqual(lu.alignment, 4)
        self.assertEqual(lu.wasted, 0)

        self.assertEqual(lp.size, 4)
        self.assertEqual(lp.alignment, 1)
        self.assertEqual(lp.wasted, 0)

        # Óptimo = normal para tipos atómicos
        self.assertEqual(lo.size, lu.size)
        self.assertEqual(lo.alignment, lu.alignment)


class TestStructType(unittest.TestCase):
    def test_simple_struct_char_int(self):
        # char: tamaño 1, alineación 2
        # int: tamaño 4, alineación 4
        char = AtomicType("char", 1, 2)
        integer = AtomicType("int", 4, 4)
        s = StructType("foo", [char, integer])

        lu = s.layout_unpacked()
        lp = s.layout_packed()
        lo = s.layout_optimal()

        # Layout normal (sin empaquetar):
        # offset char = 0
        # offset int = alineado a 4 => offset 4
        # tamaño "crudo" = 4 + 4 = 8
        # alineación struct = max(2,4) = 4 -> tamaño final 8
        # padding interno = 3 (entre char e int)
        self.assertEqual(lu.size, 8)
        self.assertEqual(lu.alignment, 4)
        self.assertEqual(lu.internal_padding, 3)
        self.assertEqual(lu.wasted, 3 + lu.final_padding)

        # Empaquetado:
        # tamaño = 1 + 4 = 5, alineación 1
        self.assertEqual(lp.size, 5)
        self.assertEqual(lp.alignment, 1)
        self.assertEqual(lp.wasted, 0)

        # Óptimo: orden por alineación descendente -> int, char
        # offset int = 0
        # offset char = siguiente múltiplo de 2 => 4
        # tamaño crudo = 4 + 1 = 5 ; alineación struct = 4 => tamaño final = 8
        self.assertEqual(lo.size, 8)
        self.assertEqual(lo.alignment, 4)
        self.assertGreaterEqual(lu.wasted, lo.wasted)

    def test_struct_with_three_fields(self):
        a = AtomicType("a", 1, 1)
        b = AtomicType("b", 2, 2)
        c = AtomicType("c", 4, 4)
        s = StructType("s", [a, b, c])

        lu = s.layout_unpacked()
        lo = s.layout_optimal()
        # El reordenado óptimo no debe ser peor que el normal
        self.assertLessEqual(lo.wasted, lu.wasted)


class TestUnionType(unittest.TestCase):
    def test_union_simple(self):
        a = AtomicType("a", 1, 1)
        b = AtomicType("b", 4, 4)
        u = UnionType("u", [a, b])

        lu = u.layout_unpacked()
        lp = u.layout_packed()
        lo = u.layout_optimal()

        # Unpacked:
        # max_size = 4, max_align = 4
        # tamaño final = 4, desperdicio = 0
        self.assertEqual(lu.size, 4)
        self.assertEqual(lu.alignment, 4)
        self.assertEqual(lu.wasted, 0)

        # Packed:
        self.assertEqual(lp.size, 4)
        self.assertEqual(lp.alignment, 1)
        self.assertEqual(lp.wasted, 0)

        # Óptimo = normal
        self.assertEqual(lo.size, lu.size)
        self.assertEqual(lo.alignment, lu.alignment)


class TestTypeManager(unittest.TestCase):
    def test_manager_define_and_describe(self):
        tm = TypeManager()
        tm.add_atomic("char", 1, 2)
        tm.add_atomic("int", 4, 4)

        tm.add_struct("foo", ["char", "int"])
        desc = tm.describe("foo")
        self.assertIn("Tipo: foo", desc)
        self.assertIn("Sin empaquetar", desc)
        self.assertIn("Empaquetado", desc)
        self.assertIn("Reordenamiento óptimo", desc)

    def test_manager_errors(self):
        tm = TypeManager()
        tm.add_atomic("int", 4, 4)
        with self.assertRaises(ValueError):
            tm.add_atomic("int", 2, 2)  # redefinición

        with self.assertRaises(ValueError):
            tm.add_struct("s", ["no_definido"])

        with self.assertRaises(ValueError):
            tm.describe("no_existe")

class TestTypeManagerValidations(unittest.TestCase):

    def test_invalid_type_name_reserved(self):
        tm = TypeManager()
        with self.assertRaises(ValueError):
            tm.add_atomic("ATOMICO", 1, 2)

    def test_invalid_type_name_not_identifier(self):
        tm = TypeManager()
        with self.assertRaises(ValueError):
            tm.add_atomic("123tipo", 1, 2)

    def test_alignment_not_power_of_two(self):
        tm = TypeManager()
        with self.assertRaises(ValueError):
            tm.add_atomic("weird", 3, 3)  # 3 no es potencia de 2

    def test_invalid_size(self):
        tm = TypeManager()
        with self.assertRaises(ValueError):
            tm.add_atomic("bad", -1, 4)

    def test_invalid_alignment(self):
        tm = TypeManager()
        with self.assertRaises(ValueError):
            tm.add_atomic("bad2", 4, 0)

    def test_struct_with_undefined_type(self):
        tm = TypeManager()
        tm.add_atomic("int", 4, 4)
        with self.assertRaises(ValueError):
            tm.add_struct("s", ["int", "noexiste"])

    def test_union_with_undefined_option(self):
        tm = TypeManager()
        tm.add_atomic("int", 4, 4)
        with self.assertRaises(ValueError):
            tm.add_union("u", ["int", "nada"])


if __name__ == "__main__":
    unittest.main()
