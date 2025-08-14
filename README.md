# Swizzle

[![PyPI Latest Release](https://img.shields.io/pypi/v/swizzle.svg)](https://pypi.org/project/swizzle/)
[![Pepy Total Downloads](https://img.shields.io/pepy/dt/swizzle)](https://pepy.tech/project/swizzle)
[![GitHub License](https://img.shields.io/github/license/janthmueller/swizzle)](https://github.com/janthmueller/swizzle/blob/main/LICENSE)

## Overview

**Swizzle** is a Python utility for flexible attribute manipulation. You can retrieve and assign multiple attributes of an object in any order or combination using simple attribute syntax.

It works with regular classes, `dataclass`, `Enum`, and other objects. The goal is to make working with objects that have multiple fields more flexible and expressive.

---

## Installation

### From PyPI

```bash
pip install swizzle
```

### From GitHub

```bash
pip install git+https://github.com/janthmueller/swizzle.git
```

---

## Getting Started

### Basic Usage with the `@swizzle` Decorator

```python
import swizzle

@swizzle
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

v = Vector(1, 2, 3)
print(v.yzx)  # Output: Vector(y=2, z=3, x=1)
```

### Swizzled Setters

```python
@swizzle(setter=True)
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

v = Vector(1, 2, 3)
v.zyx = 9, 8, 7
print(v.zyx)  # Output: Vector(z=9, y=8, x=7)
```

### Custom Separators

For objects with multiple fields, combining attribute names without a separator can become hard to read. You can define a separator to make expressions clearer:

```python
import swizzle

@swizzle(sep='_')
class Person:
    def __init__(self, name, age, city, country):
        self.name = name
        self.age = age
        self.city = city
        self.country = country

p = Person("Jane", 30, "Berlin", "Germany")

# Access multiple attributes clearly using underscores
print(p.name_age_city_country)  
# Output: Person(name='Jane', age=30, city='Berlin', country='Germany')
```

Without a separator, `p.nameagecitycountry` is harder to read. Using `sep='_'` keeps your attribute combinations clear and expressive.

### Swizzled Named Tuples

Inspired by `namedtuple`, `swizzledtuple` is the default output type for swizzled attributes.

```python
from swizzle import swizzledtuple

Vector = swizzledtuple('Vector', 'x y z')
v = Vector(1, 2, 3)

print(v.yzx)        # Output: Vector(y=2, z=3, x=1)
print(v.yzx.xxzyzz) # Output: Vector(x=1, x=1, z=3, y=2, z=3, z=3)
```

### Using Swizzle with `dataclass`

```python
from dataclasses import dataclass
import swizzle

@swizzle
@dataclass
class Point:
    x: int
    y: int
    z: int

p = Point(1, 2, 3)
print(p.zxy)  # Output: Point(z=3, x=1, y=2)
```

### Swizzling Enums with `meta=True`

```python
from enum import IntEnum
import swizzle

@swizzle(meta=True)
class Axis(IntEnum):
    X = 1
    Y = 2
    Z = 3

print(Axis.YXZ)  # Output: Axis(Y=<Axis.Y: 2>, X=<Axis.X: 1>, Z=<Axis.Z: 3>)
```

---

## Documentation and Advanced Usage

For more advanced features, custom settings, and examples, see the full documentation: [Swizzle Docs](https://janthmueller.github.io/swizzle/swizzle.html)

---

## Feedback and Use Cases

Swizzle was built to explore flexible attribute manipulation in Python. Feedback and suggestions are welcome. I would love to hear:

* Interesting use cases you discover
* Ideas for improvements or additional features

Feel free to open an issue or PR if you try it out.

---

## License

MIT License. See [LICENSE](https://github.com/janthmueller/swizzle/blob/main/LICENSE)
