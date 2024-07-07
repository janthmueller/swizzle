# Swizzle Decorator

The **Swizzle Decorator** for Python enhances attribute lookup methods (`__getattr__` or `__getattribute__`) to facilitate dynamic and flexible retrieval of multiple attributes based on specified arrangements of their names. This concept is reminiscent of swizzling in computer graphics, where it allows efficient access to components of vectors or coordinates in various orders:

```python
import swizzle

@swizzle
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

print(Vector(1, 2, 3).yzx)  # Output: (2, 3, 1)
```

## Installation
```bash
pip install git+https://github.com/janthmueller/swizzle.git
```

## Further Examples

### Using `swizzle` with `dataclass`

```python
import swizzle
from dataclasses import dataclass

@swizzle
@dataclass
class XYZ:
    x: int
    y: int
    z: int

# Test the swizzle
xyz = XYZ(1, 2, 3)
print(xyz.yzx)  # Output: (2, 3, 1)
```

### Using `swizzle` with `IntEnum`

```python
import swizzle
from enum import IntEnum

@swizzle(meta=True)
class XYZ(IntEnum):
    X = 1
    Y = 2
    Z = 3

# Test the swizzle
print(XYZ.yxz)  # Output: (2, 3, 1)
```
Setting the `meta` argument to `True` in the swizzle decorator extends the `getattr` behavior of the metaclass, enabling attribute swizzling directly on the class itself.

### Using `swizzle` with `NamedTuple`

```python
import swizzle
from typing import NamedTuple

@swizzle
class XYZ(NamedTuple):
    x: int
    y: int
    z: int

# Test the swizzle
xyz = XYZ(1, 2, 3)
print(xyz.yzx)  # Output: (2, 3, 1)
```


### Sequential matching 
Attributes are matched from left to right, starting with the longest substring match. 
```python
import swizzle

@swizzle(meta=True)
class Test:
    x = 1
    y = 2
    z = 3
    xy = 4
    yz = 5
    xz = 6
    xyz = 7

# Test the swizzle
print(Test.xz)  # Output: (6,)
print(Test.yz)  # Output: (5,)
print(Test.xyyz)  # Output: (4, 5)
print(Test.xyzx)  # Output: (7, 1)
```

