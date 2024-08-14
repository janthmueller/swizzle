# Copyright (c) 2024 Jan T. Müller <mail@jantmueller.com>

from functools import wraps
import types
import sys as _sys

from keyword import iskeyword as _iskeyword
from operator import itemgetter as _itemgetter
try:
    from _collections import _tuplegetter
except ImportError:
    _tuplegetter = lambda index, doc: property(_itemgetter(index), doc=doc)


__version__ = "2.0.0"

MISSING = object()

def swizzlednamedtuple(typename, field_names, *, rename=False, defaults=None, module=None, arrange_names = None, seperator = None):
    # Validate the field names. Skip duplicate and underscore checks.
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))
    if arrange_names is not None:
        if isinstance(arrange_names, str):
            arrange_names = arrange_names.replace(',', ' ').split()
        arrange_names = list(map(str, arrange_names))
        assert set(arrange_names) == set(field_names), 'Arrangement must contain all field names'
    else:
        arrange_names = field_names.copy()


    typename = _sys.intern(str(typename))

    _dir = dir(tuple) + ['__match_args__', '__module__', '__slots__', '_asdict', '_field_defaults', '_fields', '_make', '_replace',]
    if rename:
        seen = set()
        name_newname = {}
        for index, name in enumerate(field_names):
            if (not name.isidentifier()
                or _iskeyword(name)
                or name in _dir
                or name in seen):
                field_names[index] = f'_{index}'
            name_newname[name] = field_names[index]
            seen.add(name)
        for index, name in enumerate(arrange_names):
            arrange_names[index] = name_newname[name]

    for name in [typename] + field_names:
        if type(name) is not str:
            raise TypeError('Type names and field names must be strings')
        if not name.isidentifier():
            raise ValueError('Type names and field names must be valid '
                             f'identifiers: {name!r}')
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a '
                             f'keyword: {name!r}')
    seen = set()
    for name in field_names:
        if name in _dir and not rename:
            raise ValueError('Field names cannot be an attribute name which would shadow the namedtuple methods or attributes'
                             f'{name!r}')
        if name in seen:
            raise ValueError(f'Encountered duplicate field name: {name!r}')
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
            raise TypeError('Got more default values than field names')
        field_defaults = dict(reversed(list(zip(reversed(field_names),
                                                reversed(defaults)))))

    field_names = tuple(map(_sys.intern, field_names))
    arrange_names = tuple(map(_sys.intern, arrange_names))
    num_fields = len(field_names)
    num_arrange_fields = len(arrange_names)
    arg_list = ', '.join(field_names)
    if num_fields == 1:
        arg_list += ','
    repr_fmt = '(' + ', '.join(f'{name}=%r' for name in arrange_names) + ')'
    _dict, _tuple, _len, _map, _zip = dict, tuple, len, map, zip

    namespace = {
        '_tuple_new': tuple_new,
        '__builtins__': {},
        '__name__': f'namedtuple_{typename}',
    }
    code = f'lambda _cls, {arg_list}: _tuple_new(_cls, ({arg_list}))'
    __new__ = eval(code, namespace)
    __new__.__name__ = '__new__'
    __new__.__doc__ = f'Create new instance of {typename}({arg_list})'
    if defaults is not None:
        __new__.__defaults__ = defaults

    @classmethod
    def _make(cls, iterable):
        result = tuple_new(cls, iterable)
        if _len(result) != num_arrange_fields:
            raise TypeError(f'Expected {num_arrange_fields} arguments, got {len(result)}')
        return result

    _make.__func__.__doc__ = (f'Make a new {typename} object from a sequence '
                              'or iterable')

    def _replace(self, /, **kwds):
        def generator():
            for name in field_names:
                if name in kwds:
                    yield kwds.pop(name)
                else:
                    yield getattr(self, name)

        result = self._make(iter(generator()))
        if kwds:
            raise ValueError(f'Got unexpected field names: {list(kwds)!r}')
        return result

    _replace.__doc__ = (f'Return a new {typename} object replacing specified '
                        'fields with new values')

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + repr_fmt % self

    def _asdict(self):
        'Return a new dict which maps field names to their values.'
        return _dict(_zip(arrange_names, self))

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return _tuple(self)

    @swizzle_attributes_retriever(separator=seperator, type = swizzlednamedtuple)
    def __getattribute__(self, attr_name):
        return super(_tuple, self).__getattribute__(attr_name)



    for method in (
        __new__,
        _make.__func__,
        _replace,
        __repr__,
        _asdict,
        __getnewargs__,
        __getattribute__,
    ):
        method.__qualname__ = f'{typename}.{method.__name__}'

    class_namespace = {
        '__doc__': f'{typename}({arg_list})',
        '__slots__': (),
        '_fields': field_names,
        '_field_defaults': field_defaults,
        '__new__': __new__,
        '_make': _make,
        '_replace': _replace,
        '__repr__': __repr__,
        '_asdict': _asdict,
        '__getnewargs__': __getnewargs__,
        '__getattribute__': __getattribute__
    }
    seen = set()
    for index, name in enumerate(arrange_names):
        if name in seen:
            continue
        doc = _sys.intern(f'Alias for field number {index}')
        class_namespace[name] = _tuplegetter(index, doc)
        seen.add(name)

    result = type(typename, (tuple,), class_namespace)

    if module is None:
        try:
            module = _sys._getframemodulename(1) or '__main__'
        except AttributeError:
            try:
                module = _sys._getframe(1).f_globals.get('__name__', '__main__')
            except (AttributeError, ValueError):
                pass
    if module is not None:
        result.__module__ = module

    return result


# Helper function to split a string based on a separator
def split_string(string, separator):
    if separator == '':
        return list(string)
    else:
        return string.split(separator)

# Helper function to collect attribute retrieval functions from a class or meta-class
def collect_attribute_functions(cls):
    funcs = []
    if hasattr(cls, '__getattribute__'):
        funcs.append(cls.__getattribute__)
    if hasattr(cls, '__getattr__'):
        funcs.append(cls.__getattr__)
    if not funcs:
        raise AttributeError("No __getattr__ or __getattribute__ found on the class or meta-class")
    return funcs

# Function to combine multiple attribute retrieval functions

def swizzle_attributes_retriever(attribute_funcs=None, separator=None, type = tuple):
    def _swizzle_attributes_retriever(attribute_funcs):
        if not isinstance(attribute_funcs, list):
            attribute_funcs = [attribute_funcs]

        def retrieve_attribute(obj, attr_name):
            for func in attribute_funcs:
                try:
                    return func(obj, attr_name)
                except AttributeError:
                    continue
            return MISSING

        @wraps(attribute_funcs[-1])
        def retrieve_swizzled_attributes(obj, attr_name):
            # Attempt to find an exact attribute match
            attribute = retrieve_attribute(obj, attr_name)
            if attribute is not MISSING:
                return attribute

            matched_attributes = []
            arranged_names = []
            # If a separator is provided, split the name accordingly
            if separator is not None:
                attr_parts = split_string(attr_name, separator)
                arranged_names = attr_parts
                for part in attr_parts:
                    attribute = retrieve_attribute(obj, part)
                    if attribute is not MISSING:
                        matched_attributes.append(attribute)
            else:
                # No separator provided, attempt to match substrings
                i = 0
                while i < len(attr_name):
                    match_found = False
                    for j in range(len(attr_name), i, -1):
                        substring = attr_name[i:j]
                        attribute = retrieve_attribute(obj, substring)
                        if attribute is not MISSING:
                            matched_attributes.append(attribute)
                            arranged_names.append(substring)
                            i = j  # Move index to end of the matched substring
                            match_found = True
                            break
                    if not match_found:
                        raise AttributeError(f"No matching attribute found for substring: {attr_name[i:]}")

            if type == swizzlednamedtuple:
                field_names = set(arranged_names)
                field_values = [retrieve_attribute(obj, name) for name in field_names]
                name = "swizzlednamedtuple"
                if hasattr(obj, "__name__"):
                    name = obj.__name__
                elif hasattr(obj, "__class__"):
                    if hasattr(obj.__class__, "__name__"):
                        name = obj.__class__.__name__
                result = type(name, field_names, arrange_names=arranged_names)
                result = result(*field_values)
                return result


            return type(matched_attributes)

        return retrieve_swizzled_attributes

    if attribute_funcs is not None:
        return _swizzle_attributes_retriever(attribute_funcs)
    else:
        return _swizzle_attributes_retriever

# Decorator function to enable swizzling for a class
def swizzle(cls=None, use_meta=False, separator=None, _type = tuple):
    def class_decorator(cls):
        # Collect attribute retrieval functions from the class
        attribute_funcs = collect_attribute_functions(cls)

        # Apply the swizzling to the class's attribute retrieval
        setattr(cls, attribute_funcs[-1].__name__, swizzle_attributes_retriever(attribute_funcs, separator, _type))

        # Handle meta-class swizzling if requested
        if use_meta:
            print(cls)
            meta_cls = type(cls)
            if meta_cls == type:
                class SwizzledMetaType(meta_cls):
                    pass
                meta_cls = SwizzledMetaType
                cls = meta_cls(cls.__name__, cls.__bases__, dict(cls.__dict__))
                meta_cls = SwizzledMetaType
                cls = meta_cls(cls.__name__, cls.__bases__, dict(cls.__dict__))

            meta_funcs = collect_attribute_functions(meta_cls)
            setattr(meta_cls, meta_funcs[-1].__name__, swizzle_attributes_retriever(meta_funcs, separator, _type))

        return cls

    if cls is None:
        return class_decorator
    else:
        return class_decorator(cls)


class Swizzle(types.ModuleType):
    def __init__(self):
        types.ModuleType.__init__(self, __name__)
        self.__dict__.update(_sys.modules[__name__].__dict__)

    def __call__(self, cls=None, meta=False, sep = None, type = swizzlednamedtuple):
        return swizzle(cls, meta, sep, type)

_sys.modules[__name__] = Swizzle()
