import unittest
import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from swizzle import swizzledtuple

class Testswizzledtuple(unittest.TestCase):

    def test_basic_namedtuple(self):
        Point = swizzledtuple('Point', 'x y z')
        p = Point(1, 2, 3)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)
        self.assertEqual(repr(p), 'Point(x=1, y=2, z=3)')

    def test_rearranged_fields(self):
        Point = swizzledtuple('Point', 'x y z', arrange_names='z x y')
        p = Point(1, 2, 3)
        self.assertEqual(p, (3, 1, 2))
        self.assertEqual(repr(p), 'Point(z=3, x=1, y=2)')

    def test_default_values(self):
        Point = swizzledtuple('Point', 'x y z', defaults=(0, 0, 0))
        p = Point(1)
        self.assertEqual(p, (1, 0, 0))
        self.assertEqual(p.y, 0)
        self.assertEqual(repr(p), 'Point(x=1, y=0, z=0)')

    def test_rename_functionality(self):
        MyTuple = swizzledtuple('MyTuple', 'class def x', rename=True)
        t = MyTuple(1, 2, 3)
        self.assertEqual(t._0, 1)
        self.assertEqual(t._1, 2)
        self.assertEqual(t.x, 3)
        self.assertEqual(repr(t), 'MyTuple(_0=1, _1=2, x=3)')

    def test_invalid_field_names(self):
        with self.assertRaises(ValueError):
            swizzledtuple('MyTuple', 'class def x')

    def test_duplicate_field_names(self):
        with self.assertRaises(ValueError):
            swizzledtuple('MyTuple', 'x y x')

    def test_incorrect_arrangement(self):
        with self.assertRaises(AssertionError):
            swizzledtuple('Point', 'x y z', arrange_names='z y w')

    def test_replace_method(self):
        Point = swizzledtuple('Point', 'x y z')
        p = Point(1, 2, 3)
        p_new = p._replace(y=5)
        self.assertEqual(p_new, (1, 5, 3))
        self.assertEqual(p_new.y, 5)

    def test_asdict_method(self):
        Point = swizzledtuple('Point', 'x y z')
        p = Point(1, 2, 3)
        d = p._asdict()
        self.assertEqual(d, {'x': 1, 'y': 2, 'z': 3})

    def test_make_method(self):
        Point = swizzledtuple('Point', 'x y z')
        p = Point._make([1, 2, 3])
        self.assertEqual(p, (1, 2, 3))

    def test_integration(self):
        MyTuple = swizzledtuple('MyTuple', 'x y z', arrange_names='z x y z', rename=True, defaults=(0,0,2), sep='')
        t = MyTuple(1)
        self.assertEqual(t, (2, 1, 0, 2))
        self.assertEqual(repr(t), 'MyTuple(z=2, x=1, y=0, z=2)')
        t_new = t._replace(y=5)
        print(t_new)
        self.assertEqual(t_new, (2, 1, 5, 2))
        self.assertEqual(t_new._asdict(), {'z': 2, 'x': 1, 'y': 5})

class TestSwizzledTupleGetItem(unittest.TestCase):
    def setUp(self):
        self.Vector = swizzledtuple('Vector', 'x y z', arrange_names='y z x x')
        self.v = self.Vector(1, 2, 3)  # y=2, z=3, x=1, x=1

    def test_getitem_index(self):
        self.assertEqual(self.v[0], 2)  # y
        self.assertEqual(self.v[1], 3)  # z
        self.assertEqual(self.v[2], 1)  # x
        self.assertEqual(self.v[3], 1)  # x again (duplicate field)

    def test_getitem_slice(self):
        sliced = self.v[1:3]
        self.assertIsInstance(sliced, tuple)  # Should be a swizzledtuple subclass of tuple
        self.assertEqual(len(sliced), 2)
        self.assertEqual(sliced, (3,1))

        self.assertEqual(sliced[0], 3)  # z
        self.assertEqual(sliced[1], 1)  # x

    def test_getitem_full_slice(self):
        full_slice = self.v[:]
        self.assertIsInstance(full_slice, tuple)
        self.assertEqual(full_slice, self.v)

    def test_getitem_empty_slice(self):
        empty_slice = self.v[2:2]
        self.assertIsInstance(empty_slice, tuple)
        self.assertEqual(len(empty_slice), 0)

    def test_getitem_invalid_index(self):
        with self.assertRaises(IndexError):
            _ = self.v[10]  # Out of range

    def test_getitem_invalid_slice(self):
        negative_slice = self.v[::-1]
        self.assertIsInstance(negative_slice, tuple)
        self.assertEqual(negative_slice, (1, 1, 3, 2))  # reversed values

if __name__ == '__main__':
    unittest.main()

