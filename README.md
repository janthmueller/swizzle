# Swizzle

[![PyPI Latest Release](https://img.shields.io/pypi/v/swizzle.svg)](https://pypi.org/project/swizzle/)
[![Pepy Total Downloads](https://img.shields.io/pepy/dt/swizzle)](https://pepy.tech/project/swizzle)
[![GitHub License](https://img.shields.io/github/license/janthmueller/swizzle)](https://github.com/janthmueller/swizzle/blob/main/LICENSE)

## Introduction

**Swizzle** is a Python package that enhances attribute access, allowing for flexible retrieval of multiple attributes based on specified arrangements of their names.

Managing object attributes efficiently can sometimes become cumbersome, especially when you need to access multiple attributes in various combinations. Swizzle simplifies this process by extending Python's attribute access mechanisms, enabling you to access attributes in any order or combination without explicitly referencing the instance every time or defining new methods for each combination.

## Features

* **Dynamic Attribute Access**: Retrieve multiple attributes in any specified arrangement.
* **Reduced Boilerplate**: One call is enough to access multiple attributes.
* **Integration with Existing Classes**: Works seamlessly with regular classes, `dataclass`, and even `Enum` types.
* **Swizzled Setters (New!)**: Optionally enable attribute assignment with swizzling syntax (e.g., `vec.xyz = 1,2,3`).

## Installation

### From PyPI

Install Swizzle via pip:

```bash
pip install swizzle
```

### From GitHub

Install the latest version directly from GitHub:

```bash
pip install git+https://github.com/janthmueller/swizzle.git
```

## Getting Started

### Basic Usage with the `@swizzle` Decorator

Apply the `@swizzle` decorator to your class:

```python
import swizzle

@swizzle
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

v = Vector(1, 2, 3)

# Access attributes in different orders
print(v.yzx)  # Output: Vector(y=2, z=3, x=1)
```

### Using Swizzle with `dataclass`

Swizzle integrates smoothly with Python's `dataclass`:

```python
import swizzle
from dataclasses import dataclass

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

Enable attribute swizzling directly on the class by setting `meta=True`:

```python
import swizzle
from enum import IntEnum

@swizzle(meta=True)
class Axis(IntEnum):
    X = 1
    Y = 2
    Z = 3

print(Axis.YXZ)  # Output: Axis(Y=<Axis.Y: 2>, X=<Axis.X: 1>, Z=<Axis.Z: 3>)
```

### Swizzled Setters (New!)

Starting with the latest version, Swizzle supports setting multiple attributes at once using swizzled assignment syntax:

```python
import swizzle

@swizzle(setter=True)
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

v = Vector(1, 2, 3)

# Set multiple attributes in swizzled order
v.zyx = 9, 8, 7

# Access the attributes with swizzle syntax
print(v.zyx)  # Output: Vector(z=9, y=8, x=7)
```

## Advanced Usage

### Swizzled Named Tuples with `swizzledtuple`

Create swizzled named tuples inspired by `namedtuple`:

```python
from swizzle import swizzledtuple

Vector = swizzledtuple('Vector', 'x y z') # Equivalent to swizzle.t('Vector', 'x y z')

v = Vector(1, 2, 3)

print(v.yzx)        # Output: Vector(y=2, z=3, x=1)
print(v.yzx.xxzyzz) # Output: Vector(x=1, x=1, z=3, y=2, z=3, z=3)
```

### Custom Separators for Clearer Access

You can customize the separator used between attribute names in swizzle expressions to make them more readable—especially when combining many fields. Use the `sep` argument in the `@swizzle` decorator:

```python
import swizzle

@swizzle(sep='_')
class Vector:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

v = Vector(1, 2, 3, 4)

print(v.x_y_z_w)  # Output: Vector(x=1, y=2, z=3, w=4)
```

This helps visually separate attribute names, making swizzled expressions more readable and less error-prone in complex cases.

## Understanding Swizzling

Swizzling allows:

* **Rearrangement**: Access attributes in any order (e.g., `v.yzx`).
* **Duplication**: Access the same attribute multiple times (e.g., `v.xxy`).
* **Dynamic Composition**: Create new instances with desired attribute arrangements.
* **Swizzled Setters**: Assign multiple attributes simultaneously in any order (e.g., `v.xyz = 1,2,3`).

## Benefits

* **Efficient Attribute Management**: Simplify complex attribute combinations.
* **Dynamic Access Patterns**: No need for predefined attribute combinations.
* **Cleaner Codebase**: Reduce redundancy and improve maintainability.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](https://github.com/janthmueller/swizzle/blob/main/LICENSE) file for details.

## Contributions

Contributions are welcome! Feel free to submit a Pull Request or open an Issue on GitHub.

