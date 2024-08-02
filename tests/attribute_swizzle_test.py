import unittest
import sys
import os
from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple

# Assuming swizzle is a decorator in your project
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
import swizzle

# Vector class definition
@swizzle
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class TestVectorSwizzling(unittest.TestCase):
    
    def setUp(self):
        self.vector = Vector(1, 2, 3)
    
    def test_swizzle_yzx(self):
        self.assertEqual(self.vector.yzx, (2, 3, 1))

    def test_invalid_swizzle(self):
        with self.assertRaises(AttributeError):
            _ = self.vector.nonexistent_attribute

### 2. **XYZ Dataclass Swizzling Tests**

@dataclass
@swizzle
class XYZ:
    x: int
    y: int
    z: int

class TestXYZDataclassSwizzling(unittest.TestCase):
    
    def setUp(self):
        self.xyz = XYZ(1, 2, 3)
    
    def test_swizzle_yzx(self):
        self.assertEqual(self.xyz.yzx, (2, 3, 1))
    
    def test_invalid_swizzle(self):
        with self.assertRaises(AttributeError):
            _ = self.xyz.nonexistent_attribute

### 3. **XYZ IntEnum Meta Swizzling Tests**

@swizzle(meta=True)
class XYZEnumMeta(IntEnum):
    X = 1
    Y = 2
    Z = 3

class TestXYZEnumMetaSwizzling(unittest.TestCase):
    
    def test_swizzle_meta(self):
        self.assertEqual(XYZEnumMeta.YXZ, (XYZEnumMeta.Y, XYZEnumMeta.X, XYZEnumMeta.Z))

### 4. **XYZ NamedTuple Swizzling Tests**

@swizzle
class XYZNamedTuple(NamedTuple):
    x: int
    y: int
    z: int

class TestXYZNamedTupleSwizzling(unittest.TestCase):
    
    def setUp(self):
        self.xyz = XYZNamedTuple(1, 2, 3)
    
    def test_swizzle_yzx(self):
        self.assertEqual(self.xyz.yzx, (2, 3, 1))
    
    def test_invalid_swizzle(self):
        with self.assertRaises(AttributeError):
            _ = self.xyz.nonexistent_attribute

### 5. **Sequential Attribute Matching Tests**

@swizzle(meta=True)
class Test:
    x = 1
    y = 2
    z = 3
    xy = 4
    yz = 5
    xz = 6
    xyz = 7

class TestSequentialAttributeMatching(unittest.TestCase):
    
    def test_attribute_values(self):
        self.assertEqual(Test.xz, 6)
        self.assertEqual(Test.yz, 5)
    
    def test_composite_swizzle(self):
        self.assertEqual(Test.xyyz, (4, 5))
        self.assertEqual(Test.xyzx, (7, 1))

### 6. **Invalid Swizzle Requests Tests**

class TestInvalidSwizzleRequests(unittest.TestCase):
    
    def test_vector_invalid_swizzle(self):
        vector = Vector(1, 2, 3)
        with self.assertRaises(AttributeError):
            _ = vector.nonexistent_attribute
    
    def test_xyz_invalid_swizzle(self):
        xyz = XYZ(1, 2, 3)
        with self.assertRaises(AttributeError):
            _ = xyz.nonexistent_attribute
    
    def test_xyz_namedtuple_invalid_swizzle(self):
        xyz = XYZNamedTuple(1, 2, 3)
        with self.assertRaises(AttributeError):
            _ = xyz.nonexistent_attribute

if __name__ == "__main__":
    unittest.main()
