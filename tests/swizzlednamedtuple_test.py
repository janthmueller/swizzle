import unittest
import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from swizzle import swizzlednamedtuple

class Testswizzlednamedtuple(unittest.TestCase):

    def test_basic_namedtuple(self):
        Point = swizzlednamedtuple('Point', 'x y z')
        p = Point(1, 2, 3)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)
        self.assertEqual(repr(p), 'Point(x=1, y=2, z=3)')

    def test_rearranged_fields(self):
        Point = swizzlednamedtuple('Point', 'x y z', arrange_names='z x y')
        p = Point(1, 2, 3)
        self.assertEqual(p, (3, 1, 2))
        self.assertEqual(repr(p), 'Point(z=3, x=1, y=2)')

    def test_default_values(self):
        Point = swizzlednamedtuple('Point', 'x y z', defaults=(0, 0, 0))
        p = Point(1)
        self.assertEqual(p, (1, 0, 0))
        self.assertEqual(p.y, 0)
        self.assertEqual(repr(p), 'Point(x=1, y=0, z=0)')

    def test_rename_functionality(self):
        MyTuple = swizzlednamedtuple('MyTuple', 'class def x', rename=True)
        t = MyTuple(1, 2, 3)
        self.assertEqual(t._0, 1)
        self.assertEqual(t._1, 2)
        self.assertEqual(t.x, 3)
        self.assertEqual(repr(t), 'MyTuple(_0=1, _1=2, x=3)')

    def test_invalid_field_names(self):
        with self.assertRaises(ValueError):
            swizzlednamedtuple('MyTuple', 'class def x')

    def test_duplicate_field_names(self):
        with self.assertRaises(ValueError):
            swizzlednamedtuple('MyTuple', 'x y x')

    def test_incorrect_arrangement(self):
        with self.assertRaises(AssertionError):
            swizzlednamedtuple('Point', 'x y z', arrange_names='z y w')

    def test_replace_method(self):
        Point = swizzlednamedtuple('Point', 'x y z')
        p = Point(1, 2, 3)
        p_new = p._replace(y=5)
        self.assertEqual(p_new, (1, 5, 3))
        self.assertEqual(p_new.y, 5)

    def test_asdict_method(self):
        Point = swizzlednamedtuple('Point', 'x y z')
        p = Point(1, 2, 3)
        d = p._asdict()
        self.assertEqual(d, {'x': 1, 'y': 2, 'z': 3})

    def test_make_method(self):
        Point = swizzlednamedtuple('Point', 'x y z')
        p = Point._make([1, 2, 3])
        self.assertEqual(p, (1, 2, 3))

    def test_integration(self):
        MyTuple = swizzlednamedtuple('MyTuple', 'x y z', arrange_names='z x y z', rename=True, defaults=(0,0,2), seperator='')
        t = MyTuple(1)
        self.assertEqual(t, (2, 1, 0, 2))
        self.assertEqual(repr(t), 'MyTuple(z=2, x=1, y=0, z=2)')
        t_new = t._replace(y=5)
        print(t_new)
        self.assertEqual(t_new, (2, 1, 5, 2))
        self.assertEqual(t_new._asdict(), {'z': 2, 'x': 1, 'y': 5})

if __name__ == '__main__':
    unittest.main()

