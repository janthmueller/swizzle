# Copyright (c) 2024 Jan T. Müller <mail@jantmueller.com>

import builtins
import sys as _sys
import types
import unicodedata
import warnings
from collections.abc import Iterable
from enum import Enum, EnumMeta
from functools import wraps
from importlib.metadata import version as get_version
from keyword import iskeyword as _iskeyword
from operator import itemgetter as _itemgetter

from .trie import Trie

try:
    from _collections import _tuplegetter
except ImportError:
    _tuplegetter = lambda index, doc: property(_itemgetter(index), doc=doc)


try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _version

    __version__ = _version("swizzle")
except PackageNotFoundError:
    try:
        from setuptools_scm import get_version

        __version__ = get_version(root=".", relative_to=__file__)
    except Exception:
        __version__ = "0.0.0-dev"

_type = builtins.type
MISSING = object()


class AttrSource(str, Enum):
    SLOTS = "slots"
    CLASSDIR = "classdir"


def swizzledtuple(
    typename,
    field_names,
    arrange_names=None,
    *,
    rename=False,
    defaults=None,
    module=None,
    sep=None,
):
    """
    Create a custom named tuple class with swizzled attributes, allowing for rearranged field names
    and customized attribute access.

    This function generates a new subclass of `tuple` with named fields, similar to Python's
    `collections.namedtuple`. However, it extends the functionality by allowing field names to be
    rearranged, and attributes to be accessed with a customizable sep. The function also
    provides additional safeguards for field naming and attribute access.

    Args:
        typename (str): The name of the new named tuple type.
        field_names (sequence of str or str): A sequence of field names for the tuple. If given as
            a single string, it will be split into separate field names.
        rename (bool, optional): If True, invalid field names are automatically replaced with
            positional names. Defaults to False.
        defaults (sequence, optional): Default values for the fields. Defaults to None.
        module (str, optional): The module name in which the named tuple is defined. Defaults to
            the caller's module.
        arrange_names (sequence of str, optional): A sequence of field names indicating the order
            in which fields should be arranged in the resulting named tuple. This allows for fields
            to be rearranged and, unlike standard `namedtuple`, can include duplicates. Defaults
            to the order given in `field_names`.
        sep (str, optional): A separator string used to control how attribute names are constructed.
            If provided, fields will be joined using this separator to create compound attribute names.
            Defaults to None.

            Special case: If all field names have the same length `n` after optional renaming,
            and `sep` is still None, then `sep` is automatically set to `"+n"` (e.g. "+2").
            This indicates that names should be split every `n` characters for improved performance.

    Returns:
        type: A new subclass of `tuple` with named fields and customized attribute access.

    Notes:
        - The function is based on `collections.namedtuple` but with additional features such as
          field rearrangement and swizzled attribute access.
        - The `arrange_names` argument allows rearranging the field names, and it can include
          duplicates, which is not possible in a standard `namedtuple`.
        - The generated named tuple class includes methods like `_make`, `_replace`, `__repr__`,
          `_asdict`, and `__getnewargs__`, partially customized to handle the rearranged field order.
        - The `sep` argument enables a custom structure for attribute access, allowing for
          combined attribute names based on the provided sep. If no sep is provided,
          standard attribute access is used.

    Example:
        >>> Vector = swizzledtuple('Vector', 'x y z', arrange_names='y z x x')
        >>> # Test the swizzle
        >>> v = Vector(1, 2, 3)
        >>> print(v)  # Output: Vector(y=2, z=3, x=1, x=1)
        >>> print(v.yzx)  # Output: Vector(y=2, z=3, x=1)
        >>> print(v.yzx.xxzyzz)  # Output: Vector(x=1, x=1, z=3, y=2, z=3, z=3)
    """

    if isinstance(field_names, str):
        field_names = field_names.replace(",", " ").split()
    field_names = list(map(str, field_names))
    if arrange_names is not None:
        if isinstance(arrange_names, str):
            arrange_names = arrange_names.replace(",", " ").split()
        arrange_names = list(map(str, arrange_names))
        assert set(arrange_names) == set(
            field_names
        ), "Arrangement must contain all field names"
    else:
        arrange_names = field_names.copy()

    typename = _sys.intern(str(typename))

    _dir = dir(tuple) + [
        "__match_args__",
        "__module__",
        "__slots__",
        "_asdict",
        "_field_defaults",
        "_fields",
        "_make",
        "_replace",
    ]
    if rename:
        seen = set()
        name_newname = {}
        for index, name in enumerate(field_names):
            if (
                not name.isidentifier()
                or _iskeyword(name)
                or name in _dir
                or name in seen
            ):
                field_names[index] = f"_{index}"
            name_newname[name] = field_names[index]
            seen.add(name)
        for index, name in enumerate(arrange_names):
            arrange_names[index] = name_newname[name]

    for name in [typename] + field_names:
        if type(name) is not str:
            raise TypeError("Type names and field names must be strings")
        if not name.isidentifier():
            raise ValueError(
                "Type names and field names must be valid " f"identifiers: {name!r}"
            )
        if _iskeyword(name):
            raise ValueError(
                "Type names and field names cannot be a " f"keyword: {name!r}"
            )
    seen = set()
    for name in field_names:
        if name in _dir:
            raise ValueError(
                "Field names cannot be an attribute name which would shadow the namedtuple methods or attributes"
                f"{name!r}"
            )
        if name in seen:
            raise ValueError(f"Encountered duplicate field name: {name!r}")
        seen.add(name)

    arrange_indices = [field_names.index(name) for name in arrange_names]

    def tuple_new(cls, iterable):
        new = []
        _iterable = list(iterable)
        for index in arrange_indices:
            new.append(_iterable[index])
        return tuple.__new__(cls, new)

    field_defaults = {}
    if defaults is not None:
        defaults = tuple(defaults)
        if len(defaults) > len(field_names):
            raise TypeError("Got more default values than field names")
        field_defaults = dict(
            reversed(list(zip(reversed(field_names), reversed(defaults))))
        )

    field_names = tuple(map(_sys.intern, field_names))
    arrange_names = tuple(map(_sys.intern, arrange_names))
    num_fields = len(field_names)
    num_arrange_fields = len(arrange_names)
    arg_list = ", ".join(field_names)
    if num_fields == 1:
        arg_list += ","
    repr_fmt = "(" + ", ".join(f"{name}=%r" for name in arrange_names) + ")"
    _dict, _tuple, _len, _zip = dict, tuple, len, zip

    namespace = {
        "_tuple_new": tuple_new,
        "__builtins__": {},
        "__name__": f"swizzledtuple_{typename}",
    }
    code = f"lambda _cls, {arg_list}: _tuple_new(_cls, ({arg_list}))"
    __new__ = eval(code, namespace)
    __new__.__name__ = "__new__"
    __new__.__doc__ = f"Create new instance of {typename}({arg_list})"
    if defaults is not None:
        __new__.__defaults__ = defaults

    @classmethod
    def _make(cls, iterable):
        result = tuple_new(cls, iterable)
        if _len(result) != num_arrange_fields:
            raise ValueError(
                f"Expected {num_arrange_fields} arguments, got {len(result)}"
            )
        return result

    _make.__func__.__doc__ = (
        f"Make a new {typename} object from a sequence " "or iterable"
    )

    def _replace(self, /, **kwds):
        def generator():
            for name in field_names:
                if name in kwds:
                    yield kwds.pop(name)
                else:
                    yield getattr(self, name)

        result = self._make(iter(generator()))
        if kwds:
            raise ValueError(f"Got unexpected field names: {list(kwds)!r}")
        return result

    _replace.__doc__ = (
        f"Return a new {typename} object replacing specified " "fields with new values"
    )

    def __repr__(self):
        "Return a nicely formatted representation string"
        return self.__class__.__name__ + repr_fmt % self

    def _asdict(self):
        "Return a new dict which maps field names to their values."
        return _dict(_zip(arrange_names, self))

    def __getnewargs__(self):
        "Return self as a plain tuple.  Used by copy and pickle."
        return _tuple(self)

    @swizzle_attributes_retriever(sep=sep, type=swizzledtuple, only_attrs=field_names)
    def __getattribute__(self, attr_name):
        return super(_tuple, self).__getattribute__(attr_name)

    def __getitem__(self, index):
        if not isinstance(index, slice):
            return _tuple.__getitem__(self, index)

        selected_indices = arrange_indices[index]
        selected_values = _tuple.__getitem__(self, index)

        seen = set()
        filtered = [
            (i, v, field_names[i])
            for i, v in zip(selected_indices, selected_values)
            if not (i in seen or seen.add(i))
        ]

        if filtered:
            _, filtered_values, filtered_names = zip(*filtered)
        else:
            filtered_values, filtered_names = (), ()

        return swizzledtuple(
            typename,
            filtered_names,
            rename=rename,
            defaults=filtered_values,
            module=module,
            arrange_names=arrange_names[index],
            sep=sep,
        )()

    for method in (
        __new__,
        _make.__func__,
        _replace,
        __repr__,
        _asdict,
        __getnewargs__,
        __getattribute__,
        __getitem__,
    ):
        method.__qualname__ = f"{typename}.{method.__name__}"

    class_namespace = {
        "__doc__": f"{typename}({arg_list})",
        "__slots__": (),
        "_fields": field_names,
        "_field_defaults": field_defaults,
        "__new__": __new__,
        "_make": _make,
        "_replace": _replace,
        "__repr__": __repr__,
        "_asdict": _asdict,
        "__getnewargs__": __getnewargs__,
        "__getattribute__": __getattribute__,
        "__getitem__": __getitem__,
    }
    seen = set()
    for index, name in enumerate(arrange_names):
        if name in seen:
            continue
        doc = _sys.intern(f"Alias for field number {index}")
        class_namespace[name] = _tuplegetter(index, doc)
        seen.add(name)

    result = type(typename, (tuple,), class_namespace)

    if module is None:
        try:
            module = _sys._getframemodulename(1) or "__main__"
        except AttributeError:
            try:
                module = _sys._getframe(1).f_globals.get("__name__", "__main__")
            except (AttributeError, ValueError):
                pass
    if module is not None:
        result.__module__ = module

    return result


# Helper function to split a string based on a sep
def split_string(string, sep):
    if sep[0] == "+":
        n = int(sep)
        return [string[i : i + n] for i in range(0, len(string), n)]
    else:
        return string.split(sep)


# Helper function to collect attribute retrieval functions from a class or meta-class
def get_getattr_methods(cls):
    funcs = []
    if hasattr(cls, "__getattribute__"):
        funcs.append(cls.__getattribute__)
    if hasattr(cls, "__getattr__"):
        funcs.append(cls.__getattr__)
    if not funcs:
        raise AttributeError("No __getattr__ or __getattribute__ found")
    return funcs


def get_setattr_method(cls):
    if hasattr(cls, "__setattr__"):
        return cls.__setattr__
    else:
        raise AttributeError("No __setattr__ found")


def is_valid_sep(s):
    # if not s:
    #     return False
    if s[0] == "+" and s[1:].isdigit():
        return True
    for ch in s:
        if ch == "_":
            continue
        cat = unicodedata.category(ch)
        if not (cat.startswith("L") or cat == "Nd"):
            return False
    return True


def swizzle_attributes_retriever(
    getattr_funcs=None,
    sep=None,
    type=swizzledtuple,
    only_attrs=None,
    setter=None,
):
    assert (
        only_attrs is None or only_attrs
    ), "only_attrs must be either None or a non-empty iterable containing strings"

    if isinstance(only_attrs, str):
        assert only_attrs not in [AttrSource.SLOTS, AttrSource.CLASSDIR]

    trie = None

    if sep == "":
        sep = "+1"  # for backwards compatibility, remove on next version

    if sep is None and only_attrs:
        only_attrs_length = set(len(fname) for fname in only_attrs)
        if len(only_attrs_length) == 1:
            sep = f"+{next(iter(only_attrs_length))}"
        else:
            trie = Trie(only_attrs)

    if sep is not None and not is_valid_sep(sep):
        raise ValueError(
            f"Invalid value for sep: {sep!r}. Must be either:"
            " (1) a non-empty string containing only letters, digits, or underscores, "
            "or (2) a pattern of the form '+N' where N is a positive integer."
        )

    if sep is not None and only_attrs:
        if any(sep in attr for attr in only_attrs):
            warnings.warn(
                "The attribute separator is part of any of the only_attrs. "
                "This may lead to unexpected behavior, since the attribute separator"
                " will be used to split the attribute name. Consider using a different "
                "separator or only_attrs to avoid this issue.",
            )

    def _swizzle_attributes_retriever(getattr_funcs):
        if not isinstance(getattr_funcs, list):
            getattr_funcs = [getattr_funcs]

        def get_attribute(obj, attr_name):
            for func in getattr_funcs:
                try:
                    return func(obj, attr_name)
                except AttributeError:
                    continue
            return MISSING

        def retrieve_attributes(obj, attr_name):
            # Attempt to find an exact attribute match
            attribute = get_attribute(obj, attr_name)
            if attribute is not MISSING:
                return [attr_name], [attribute]

            matched_attributes = []
            arranged_names = []
            # If a sep is provided, split the name accordingly
            if sep is not None:
                attr_parts = split_string(attr_name, sep)
                arranged_names = attr_parts
                for part in attr_parts:
                    if only_attrs and part not in only_attrs:
                        raise AttributeError(
                            f"Attribute {part} is not part of an allowed field for swizzling"
                        )
                    attribute = get_attribute(obj, part)
                    if attribute is not MISSING:
                        matched_attributes.append(attribute)
                    else:
                        raise AttributeError(f"No matching attribute found for {part}")
            elif only_attrs:
                arranged_names = trie.split_longest_prefix(attr_name)
                if arranged_names is None:
                    raise AttributeError(f"No matching attribute found for {attr_name}")
                for name in arranged_names:
                    attribute = get_attribute(obj, name)
                    if attribute is not MISSING:
                        matched_attributes.append(attribute)
                    else:
                        raise AttributeError(f"No matching attribute found for {name}")
            else:
                # No sep provided, attempt to match substrings
                i = 0
                while i < len(attr_name):
                    match_found = False
                    for j in range(len(attr_name), i, -1):
                        substring = attr_name[i:j]
                        attribute = get_attribute(obj, substring)
                        if attribute is not MISSING:
                            matched_attributes.append(attribute)
                            arranged_names.append(substring)
                            i = j  # Move index to end of the matched substring
                            match_found = True
                            break
                    if not match_found:
                        raise AttributeError(
                            f"No matching attribute found for substring: {attr_name[i:]}"
                        )
            return arranged_names, matched_attributes

        @wraps(getattr_funcs[-1])
        def get_attributes(obj, attr_name):
            arranged_names, matched_attributes = retrieve_attributes(obj, attr_name)
            if len(matched_attributes) == 1:
                return matched_attributes[0]
            if type == swizzledtuple:
                seen = set()
                field_names, field_values = zip(
                    *[
                        (name, matched_attributes[i])
                        for i, name in enumerate(arranged_names)
                        if name not in seen and not seen.add(name)
                    ]
                )

                name = "swizzledtuple"
                if hasattr(obj, "__name__"):
                    name = obj.__name__
                elif hasattr(obj, "__class__"):
                    if hasattr(obj.__class__, "__name__"):
                        name = obj.__class__.__name__
                result = type(
                    name,
                    field_names,
                    arrange_names=arranged_names,
                    sep=sep,
                )
                result = result(*field_values)
                return result

            return type(matched_attributes)

        def set_attributes(obj, attr_name, value):
            try:
                arranged_names, _ = retrieve_attributes(obj, attr_name)
            except AttributeError:
                return setter(obj, attr_name, value)

            if not isinstance(value, Iterable):
                raise ValueError(
                    f"Expected an iterable value for swizzle attribute assignment, got {_type(value)}"
                )
            if len(arranged_names) != len(value):
                raise ValueError(
                    "too many values to unpack (expected {len(arranged_names)})"
                )
            kv = {}
            for k, v in zip(arranged_names, value):
                _v = kv.get(k, MISSING)
                if _v is MISSING:
                    kv[k] = v
                elif _v is not v:
                    raise ValueError(
                        f"Tries to assign muliple values to attribute {k} in one go but only one is allowed"
                    )
            for k, v in kv.items():
                setter(obj, k, v)

        if setter is not None:
            return get_attributes, wraps(setter)(set_attributes)
        return get_attributes

    if getattr_funcs is not None:
        return _swizzle_attributes_retriever(getattr_funcs)
    else:
        return _swizzle_attributes_retriever


def swizzle(
    cls=None,
    meta=False,
    sep=None,
    type=tuple,
    only_attrs=None,
    setter=False,
):
    """
    A decorator that adds attribute swizzling capabilities to a class.

    The decorator first attempts to resolve attribute access normally. If, and only if,
    a direct attribute lookup fails, it then tries to interpret the requested
    attribute name as a sequence of existing attribute names to be "swizzled".
    For example, if an object `p` has attributes `x` and `y`, a normal access to
    `p.x` works as expected, but a failed access to `p.yx` would trigger the
    swizzling logic and could return `(p.y, p.x)`.

    The decorator can parse attribute names using one of three strategies, depending
    on the arguments provided:

    **Attribute Retrieval Strategies**

    1.  **Explicit Splitting (`sep`):
        This strategy uses a clear, unambiguous rule to parse the attribute string.
        Using a delimiter (e.g., `sep='_'`) makes swizzled attributes visually distinct
        and easy to read. Using a fixed width (e.g., `sep='+1'`) allows for compact names.
        Both methods are simple and offer the highest runtime performance.

    2.  **Whitelist-Based Matching (`only_attrs`):
        This strategy restricts swizzling to a specific list of attribute names.
        It is useful for creating a well-defined and safe API, as it prevents
        accidental matching of methods or private attributes and resolves ambiguity
        if some attribute names are prefixes of others. For efficiency, the allowed
        names are pre-compiled into a Trie, which makes lookups very fast.

    3.  **Flexible Dynamic Matching (Default):
        This is the default behavior. It dynamically finds all possible attribute
        sequences within the string. This is the most flexible method and is perfect
        for interactive use or for classes with custom `__getattr__` methods or
        attributes that are added and removed at runtime. While it has more
        computational overhead, it provides the greatest adaptability for dynamic objects.

    Args:
        cls (type, optional): The class to be decorated. If `None`, the decorator
            returns a function that can be applied to a class. Defaults to `None`.
        meta (bool, optional): If `True`, swizzling is also applied to the class's
            metaclass, allowing for swizzling on the class attributes themselves.
            Defaults to `False`.
        sep (str, optional): Activates the **Explicit Splitting** strategy.
            If `sep` is in the format `'+N'`, the name is split into N-character chunks.
            Otherwise, it is split by the `sep` string. If `only_attrs` is provided and
            all names have the same length `N`, `sep` is automatically set to `'+N'`
            to ensure the best performance. Defaults to `None`.
        type (type, optional): The type of the returned collection of attributes.
            Defaults to `tuple`. For `swizzledtuple`, the swizzled attributes are
            returned as a `swizzledtuple` instance.
        only_attrs (iterable of str or AttrSource, optional): Activates the
            **Whitelist-Based Matching** strategy when `sep` is not provided.
            Can also be set to `AttrSource.SLOTS` or `AttrSource.CLASSDIR` to dynamically
            use the attributes from the class's `__slots__` or `dir(cls)`, respectively.
            Defaults to `None`.
        setter (bool, optional): If `True`, the decorator also enables swizzling for
            attribute assignment (e.g., `instance.xy = 1, 2`). It is highly recommended
            to define `__slots__` on the class when using this, as it prevents typos
            from accidentally creating new instance attributes. This is especially
            important when using a non-visually-distinct separator.
            Defaults to `False`.

    Returns:
        type or function: If `cls` is provided, returns the decorated class.
            Otherwise, returns a decorator function that can be applied to a class.

    Example:
        @swizzle
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        p = Point(1, 2)
        print(p.yx)  # Output: (2, 1)
    """

    def preserve_metadata(
        target,
        source,
        keys=("__name__", "__qualname__", "__doc__", "__module__", "__annotations__"),
    ):
        for key in keys:
            if hasattr(source, key):
                try:
                    setattr(target, key, getattr(source, key))
                except (TypeError, AttributeError):
                    pass  # some attributes may be read-only

    def class_decorator(cls):
        # Collect attribute retrieval functions from the class
        nonlocal only_attrs
        if isinstance(only_attrs, str):
            if only_attrs == AttrSource.SLOTS:
                only_attrs = cls.__slots__
                if not only_attrs:
                    raise AttributeError(
                        f"cls.__slots__ cannot be empty for only_attrs = {AttrSource.SLOTS}"
                    )
            elif only_attrs == AttrSource.CLASSDIR:
                only_attrs = dir(cls)

        getattr_methods = get_getattr_methods(cls)

        if setter:
            setattr_method = get_setattr_method(cls)
            new_getter, new_setter = swizzle_attributes_retriever(
                getattr_methods,
                sep,
                type,
                only_attrs,
                setter=setattr_method,
            )
            setattr(cls, getattr_methods[-1].__name__, new_getter)
            setattr(cls, setattr_method.__name__, new_setter)
        else:
            new_getter = swizzle_attributes_retriever(
                getattr_methods, sep, type, only_attrs, setter=None
            )
            setattr(cls, getattr_methods[-1].__name__, new_getter)

        # Handle meta-class swizzling if requested
        if meta:
            meta_cls = _type(cls)

            class SwizzledMetaType(meta_cls):
                pass

            if meta_cls == EnumMeta:

                def cfem_dummy(*args, **kwargs):
                    pass

                cfem = SwizzledMetaType._check_for_existing_members_
                SwizzledMetaType._check_for_existing_members_ = cfem_dummy

            class SwizzledClass(cls, metaclass=SwizzledMetaType):
                pass

            if meta_cls == EnumMeta:
                SwizzledMetaType._check_for_existing_members_ = cfem

            # Preserve metadata on swizzled meta and class
            preserve_metadata(SwizzledMetaType, meta_cls)
            preserve_metadata(SwizzledClass, cls)

            meta_cls = SwizzledMetaType
            cls = SwizzledClass

            meta_funcs = get_getattr_methods(meta_cls)
            if setter:
                setattr_method = get_setattr_method(meta_cls)
                new_getter, new_setter = swizzle_attributes_retriever(
                    meta_funcs,
                    sep,
                    type,
                    only_attrs,
                    setter=setattr_method,
                )
                setattr(meta_cls, meta_funcs[-1].__name__, new_getter)
                setattr(meta_cls, setattr_method.__name__, new_setter)
            else:
                new_getter = swizzle_attributes_retriever(
                    meta_funcs, sep, type, only_attrs, setter=None
                )
                setattr(meta_cls, meta_funcs[-1].__name__, new_getter)
        return cls

    if cls is None:
        return class_decorator
    else:
        return class_decorator(cls)


t = swizzledtuple
# c = swizzledclass


class Swizzle(types.ModuleType):
    def __init__(self):
        types.ModuleType.__init__(self, __name__)
        self.__dict__.update(_sys.modules[__name__].__dict__)

    def __call__(
        self,
        cls=None,
        meta=False,
        sep=None,
        type=swizzledtuple,
        only_attrs=None,
        setter=False,
    ):
        return swizzle(cls, meta, sep, type, only_attrs, setter)


_sys.modules[__name__] = Swizzle()
