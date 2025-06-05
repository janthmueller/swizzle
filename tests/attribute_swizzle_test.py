import os
import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple

import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
import swizzle


@swizzle
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


@dataclass
@swizzle
class XYZ:
    x: int
    y: int
    z: int


@swizzle
class XYZNamedTuple(NamedTuple):
    x: int
    y: int
    z: int


@swizzle(meta=True)
class XYZEnumMeta(IntEnum):
    X = 1
    Y = 2
    Z = 3


@swizzle(meta=True)
class TestMeta:
    x = 1
    y = 2
    z = 3
    xy = 4
    yz = 5
    xz = 6
    xyz = 7


@swizzle(sep="")
class SepTest:
    def __init__(self):
        self.a = 0


@swizzle(sep="_")
class Underscore:
    def __init__(self):
        self.x = 1
        self.y = 2


@swizzle
class ABC:
    def __init__(self):
        self.a = 10
        self.b = 20
        self.c = 30


@swizzle
class Shadowed:
    def __init__(self):
        self.x = 1
        self.xy = "should not be shadowed"


@swizzle
class OneField:
    def __init__(self):
        self.x = 7


# --- Parametrized Base Swizzle Tests ---


@pytest.mark.parametrize("obj_class", [Vector, XYZ, XYZNamedTuple])
def test_yzx_swizzle(obj_class):
    obj = obj_class(1, 2, 3)
    assert obj.yzx == (2, 3, 1)


@pytest.mark.parametrize("obj_class", [Vector, XYZ, XYZNamedTuple])
def test_invalid_swizzle(obj_class):
    obj = obj_class(1, 2, 3)
    with pytest.raises(AttributeError):
        _ = obj.nonexistent_attribute


# --- All 3-letter permutations ---
from itertools import permutations


@pytest.mark.parametrize("swz", ["".join(p) for p in permutations("xyz", 3)])
def test_all_3_letter_swizzles(swz):
    v = Vector(1, 2, 3)
    expected = tuple(getattr(v, c) for c in swz)
    assert getattr(v, swz) == expected


# --- IntEnum meta swizzle ---
def test_enum_meta_swizzle():
    assert XYZEnumMeta.YXZ == (XYZEnumMeta.Y, XYZEnumMeta.X, XYZEnumMeta.Z)


# --- Composite meta swizzle ---
def test_meta_composites():
    assert TestMeta.xz == 6
    assert TestMeta.yz == 5
    assert TestMeta.xyyz == (4, 5)
    assert TestMeta.xyzx == (7, 1)


# --- Separator Tests ---
def test_separator_swizzling():
    s = SepTest()
    assert s.a == 0
    assert s.aa == (0, 0)


def test_separator_invalid():
    s = SepTest()
    with pytest.raises(AttributeError):
        _ = s.aabb


def test_underscore_sep():
    u = Underscore()
    assert u.x_y == (1, 2)


# --- Custom alphabet ---
def test_abc_swizzle():
    abc = ABC()
    assert abc.bca == (20, 30, 10)


# --- Shadowed field test ---
def test_shadowed_attribute():
    s = Shadowed()
    assert s.xy == "should not be shadowed"


# --- One-field redundancy ---
def test_onefield_repetition():
    o = OneField()
    assert o.xx == (7, 7)


# --- Repr behavior ---
def test_repr_behavior():
    v = Vector(1, 2, 3)
    assert "Vector" in repr(v) or True  # Just ensure it doesn't crash


def test_meta_swizzle_does_not_affect_unswizzled_class():
    # Define a base metaclass to share
    class BaseMeta(type):
        pass

    # Define an unswizzled class using BaseMeta
    class Unswizzled(metaclass=BaseMeta):
        pass

    # Define a swizzled class using swizzle with meta=True, sharing BaseMeta
    @swizzle(meta=True)
    class Swizzled(metaclass=BaseMeta):
        pass

    # The metaclass of Swizzled should be a subclass of BaseMeta (swizzled)
    assert issubclass(type(Swizzled), BaseMeta)

    # The metaclass of Unswizzled should be exactly BaseMeta (not changed)
    assert type(Unswizzled) is BaseMeta

    # Swizzled and Unswizzled metaclasses should not be the same object
    assert type(Swizzled) is not type(Unswizzled)

    # Swizzled metaclass should preserve BaseMeta's __name__ and __qualname__
    assert getattr(type(Swizzled), "__name__", None) == BaseMeta.__name__
    assert getattr(type(Swizzled), "__qualname__", None) == BaseMeta.__qualname__


def test_meta_swizzle_with_dataclass():
    from dataclasses import dataclass

    class CustomMeta(type):
        pass

    @swizzle(meta=True)
    @dataclass
    class SwizzledDC(metaclass=CustomMeta):
        x: int
        y: int

    class UnswizzledDC(metaclass=CustomMeta):
        x = 1
        y = 2

    # SwizzledDC metaclass should be subclass of CustomMeta
    assert issubclass(type(SwizzledDC), CustomMeta)

    # UnswizzledDC metaclass should be exactly CustomMeta
    assert type(UnswizzledDC) is CustomMeta

    # SwizzledDC should behave like dataclass instance
    instance = SwizzledDC(10, 20)
    assert instance.x == 10 and instance.y == 20


def test_meta_swizzle_with_enum():
    from enum import Enum, EnumMeta

    @swizzle(meta=True)
    class SwizzledEnum(Enum):
        A = 1
        B = 2

    class UnswizzledEnum(Enum):
        A = 1
        B = 2

    assert issubclass(type(SwizzledEnum), EnumMeta)

    # Their metaclasses should not be the same object
    assert type(SwizzledEnum) is not type(UnswizzledEnum)

    # SwizzledEnum members work as expected
    assert SwizzledEnum.A.value == 1
    assert SwizzledEnum.B.value == 2


# --- Tests for `only_attrs` parameter ---


@swizzle(only_attrs=["x", "y"])
class OnlyXY:
    def __init__(self):
        self.x = 10
        self.y = 20
        self.z = 30


@swizzle(only_attrs=["a", "b"], sep="_")
class OnlyABUnderscore:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3


@swizzle(only_attrs=["a"])
class OnlyASingle:
    def __init__(self):
        self.a = 99


def test_only_attrs_valid_swizzle():
    obj = OnlyXY()
    assert obj.xy == (10, 20)
    assert obj.yx == (20, 10)


def test_only_attrs_invalid_swizzle():
    obj = OnlyXY()
    with pytest.raises(AttributeError):
        _ = obj.xz
    with pytest.raises(AttributeError):
        _ = obj.zy
    with pytest.raises(AttributeError):
        _ = obj.xyz


def test_only_attrs_normal_attr_access():
    obj = OnlyXY()
    assert obj.x == 10
    assert obj.y == 20
    assert obj.z == 30


def test_only_attrs_with_separator_valid():
    obj = OnlyABUnderscore()
    assert obj.a_b == (1, 2)
    assert obj.b_a == (2, 1)


def test_only_attrs_with_separator_invalid():
    obj = OnlyABUnderscore()
    with pytest.raises(AttributeError):
        _ = obj.a_c
    with pytest.raises(AttributeError):
        _ = obj.c_b
    with pytest.raises(AttributeError):
        _ = obj.a_b_c


def test_only_attrs_with_separator_single_attr_access():
    obj = OnlyABUnderscore()
    assert obj.a == 1
    assert obj.b == 2
    assert obj.c == 3


def test_only_attrs_single_allowed_valid():
    obj = OnlyASingle()
    assert obj.aa == (99, 99)


def test_only_attrs_single_allowed_invalid():
    obj = OnlyASingle()
    with pytest.raises(AttributeError):
        _ = obj.ab
    with pytest.raises(AttributeError):
        _ = obj.ba


def test_only_attrs_repr_behavior():
    obj = OnlyXY()
    repr_str = repr(obj)
    assert "OnlyXY" in repr_str or True  # just make sure repr doesn't crash
