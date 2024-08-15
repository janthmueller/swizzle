# Swizzle
[![PyPI version](https://badge.fury.io/py/swizzle.svg?kill_cache=1)](https://badge.fury.io/py/swizzle)
[![Downloads](https://pepy.tech/badge/swizzle?kill_cache=1)](https://pepy.tech/project/swizzle)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/janthmueller/swizzle/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/janthmueller/swizzle.svg?kill_cache=1)](https://github.com/janthmueller/swizzle/stargazers)

**Swizzle** for Python enhances attribute lookup methods to facilitate dynamic and flexible retrieval of multiple attributes based on specified arrangements of their names.
> **Update v2:**
> Introducing `swizzledtuple` , a new function that allows you to create swizzled named tuples. This feature is inspired by the `namedtuple` function from the [collections module](https://docs.python.org/3/library/collections.html#collections.namedtuple) and provides a concise way to define swizzled tuples.
> ```python
> from swizzle import swizzledtuple
>
> Vector = swizzledtuple('Vector', 'x y z', arrange_names = "y z x x")
>
> # Test the swizzle
> v = Vector(1, 2, 3)
> print(v)  # Output: Vector(y=2, z=3, x=1, x=1)
> print(v.yzx)  # Output: Vector(y = 2, z = 3, x = 1)
> print(v.yzx.xxzyzz)  # Output: Vector(x=1, x=1, z=3, y=2, z=3, z=3)
>```

### Swizzle Decorator:

```python
import swizzle

@swizzle
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Test the swizzle
print(Vector(1, 2, 3).yzx)  # Output: Vector(y = 2, z = 3, x = 1)
```


## Installation
### From PyPI
```bash
pip install swizzle
```
### From GitHub
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
class Vector:
    x: int
    y: int
    z: int

# Test the swizzle
print(Vector(1, 2, 3).yzx)  # Output: Vector(y = 2, z = 3, x = 1)
```

### Using `swizzle` with `IntEnum`

```python
import swizzle
from enum import IntEnum

@swizzle(meta=True)
class Vector(IntEnum):
    X = 1
    Y = 2
    Z = 3

# Test the swizzle
print(Vector.YXZ)  # Output: Vector(Y=<Vector.Y: 2>, X=<Vector.X: 1>, Z=<Vector.Z: 3>)
```
Setting the `meta` argument to `True` in the swizzle decorator extends the `getattr` behavior of the metaclass, enabling attribute swizzling directly on the class itself.


### Sequential matching
Attributes are matched from left to right, starting with the longest substring match. This behavior can be controlled by the `seperator` argument in the swizzle decorator.
```python
import swizzle

@swizzle(meta=True)
class Vector:
    x = 1
    y = 2
    z = 3
    xy = 4
    yz = 5
    xz = 6
    xyz = 7

# Test the swizzle
print(Vector.xz)  # Output: 6
print(Vector.yz)  # Output: 5
print(Vector.xyyz)  # Output: Vector(xy=4, yz=5)
print(Vector.xyzx)  # Output: Vector(xyz=7, x=1)
```


