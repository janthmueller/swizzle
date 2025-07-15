import os
import sys

import pytest

# Ensure root directory is on path
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from swizzle import swizzledtuple


def test_basic_namedtuple():
    Point = swizzledtuple("Point", "x y z")
    p = Point(1, 2, 3)
    assert p.x == 1
    assert p.y == 2
    assert p.z == 3
    assert repr(p) == "Point(x=1, y=2, z=3)"


def test_rearranged_fields():
    Point = swizzledtuple("Point", "x y z", arrange_names="z x y")
    p = Point(1, 2, 3)
    assert p == (3, 1, 2)
    assert repr(p) == "Point(z=3, x=1, y=2)"


def test_default_values():
    Point = swizzledtuple("Point", "x y z", defaults=(0, 0, 0))
    p = Point(1)
    assert p == (1, 0, 0)
    assert p.y == 0
    assert repr(p) == "Point(x=1, y=0, z=0)"


def test_rename_functionality():
    MyTuple = swizzledtuple("MyTuple", "class def x", rename=True)
    t = MyTuple(1, 2, 3)
    assert t._0 == 1
    assert t._1 == 2
    assert t.x == 3
    assert repr(t) == "MyTuple(_0=1, _1=2, x=3)"


def test_invalid_field_names():
    with pytest.raises(ValueError):
        swizzledtuple("MyTuple", "class def x")


def test_duplicate_field_names():
    with pytest.raises(ValueError):
        swizzledtuple("MyTuple", "x y x")


def test_incorrect_arrangement():
    with pytest.raises(AssertionError):
        swizzledtuple("Point", "x y z", arrange_names="z y w")


def test_replace_method():
    Point = swizzledtuple("Point", "x y z")
    p = Point(1, 2, 3)
    p_new = p._replace(y=5)
    assert p_new == (1, 5, 3)
    assert p_new.y == 5


def test_asdict_method():
    Point = swizzledtuple("Point", "x y z")
    p = Point(1, 2, 3)
    d = p._asdict()
    assert d == {"x": 1, "y": 2, "z": 3}


def test_make_method():
    Point = swizzledtuple("Point", "x y z")
    p = Point._make([1, 2, 3])
    assert p == (1, 2, 3)


def test_integration():
    MyTuple = swizzledtuple(
        "MyTuple",
        "x y z",
        arrange_names="z x y z",
        rename=True,
        defaults=(0, 0, 2),
        sep="",
    )
    t = MyTuple(1)
    assert t == (2, 1, 0, 2)
    assert repr(t) == "MyTuple(z=2, x=1, y=0, z=2)"
    t_new = t._replace(y=5)
    assert t_new == (2, 1, 5, 2)
    assert t_new._asdict() == {"z": 2, "x": 1, "y": 5}


def test_attribute_access_single_field_returns_value():
    T = swizzledtuple("T", "x y z")
    t = T(1, 2, 3)
    assert t.x == 1
    assert t.y == 2
    assert t.z == 3


def test_attribute_access_multi_swizzle_returns_tuple():
    T = swizzledtuple("T", "x y z")
    t = T(1, 2, 3)
    yzx = t.yzx
    assert yzx == (2, 3, 1)
    assert yzx.x == 1
    assert yzx.y == 2
    assert yzx.z == 3


def test_attribute_access_sep_variant():
    T = swizzledtuple("T", "x y z", sep="_")
    t = T(4, 5, 6)
    swz = t.x_y_z
    assert swz == (4, 5, 6)
    assert swz.x == 4
    assert swz.y == 5
    assert swz.z == 6


def test_attribute_access_prefix_ambiguity():
    T = swizzledtuple("T", "a aa aaa")
    t = T(1, 2, 3)
    val = t.aaa
    assert val == 3
    swz = t.aaaaa  # longest match first: aaa + aa
    assert swz == (3, 2)
    assert swz.aaa == 3
    assert swz.aa == 2


def test_longest_prefix_first_resolution():
    T = swizzledtuple("T", "a aa aaa ab abc abcd")
    t = T(1, 2, 3, 4, 5, 6)
    assert t.aaaaaa == (3, 3)
    assert t.abcdabcaaaaa == (6, 5, 3, 2)


def test_nested_swizzle_sep_resolution():
    T = swizzledtuple("T", "x1 x2 y1 y2", sep="_")
    t = T(1, 2, 3, 4)
    val = t.x1_y1
    assert val == (1, 3)
    assert val.x1 == 1
    assert val.y1 == 3


def test_swizzle_with_rearranged_overlap():
    T = swizzledtuple("T", "a aa aaa", arrange_names="aaa aa a aaa")
    t = T(1, 2, 3)
    assert t == (3, 2, 1, 3)
    assert t.aaaaa == (3, 2)


def test_invalid_swizzle_attribute():
    T = swizzledtuple("T", "x y z")
    t = T(1, 2, 3)
    with pytest.raises(AttributeError):
        _ = t.q
    with pytest.raises(AttributeError):
        _ = t.xqz


def test_common_wordlike_prefixes():
    T = swizzledtuple("T", "a ab abc abcd")
    t = T(1, 2, 3, 4)
    assert t.abcdabc == (4, 3)
    assert t.abcab == (3, 2)


def test_repr_with_longest_match():
    T = swizzledtuple("T", "r g b rgb", arrange_names="rgb r g b")
    t = T(10, 20, 30, 999)
    assert t.rgb == 999
    swz = t.rgbrgb
    assert swz == (999, 999)
    assert swz.rgb == 999


def test_getitem():
    T = swizzledtuple("T", "x y z")
    t = T(1, 2, 3)
    assert t[0] == 1
    assert t[1] == 2
    assert t[2] == 3
    assert t[0:2] == (1, 2)
    assert t[:2] == (1, 2)
    assert t[1:] == (2, 3)
    assert t[:] == (1, 2, 3)
    assert t[-1] == 3
    assert t[-2:] == (2, 3)
    assert t[:-1] == (1, 2)
    assert t[3:] == ()
