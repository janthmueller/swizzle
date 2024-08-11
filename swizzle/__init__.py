from functools import wraps
import sys
import types

__version__ = "0.1.4"
MISSING = object()


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
def swizzle_attributes_retriever(attribute_funcs, separator=None):
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

        # If a separator is provided, split the name accordingly
        if separator is not None:
            attr_parts = split_string(attr_name, separator)
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
                        i = j  # Move index to end of the matched substring
                        match_found = True
                        break
                if not match_found:
                    raise AttributeError(f"No matching attribute found for substring: {attr_name[i:]}")

        return tuple(matched_attributes)

    return retrieve_swizzled_attributes

# Decorator function to enable swizzling for a class
def swizzle(cls=None, use_meta=False, separator=None):
    def class_decorator(cls):
        # Collect attribute retrieval functions from the class
        attribute_funcs = collect_attribute_functions(cls)

        # Apply the swizzling to the class's attribute retrieval
        setattr(cls, attribute_funcs[-1].__name__, swizzle_attributes_retriever(attribute_funcs, separator))

        # Handle meta-class swizzling if requested
        if use_meta:
            meta_cls = type(cls)
            if meta_cls == type:
                class SwizzledMetaType(meta_cls):
                    pass
                meta_cls = SwizzledMetaType
                cls = meta_cls(cls.__name__, cls.__bases__, dict(cls.__dict__))
                meta_cls = SwizzledMetaType
                cls = meta_cls(cls.__name__, cls.__bases__, dict(cls.__dict__))

            meta_funcs = collect_attribute_functions(meta_cls)
            setattr(meta_cls, meta_funcs[-1].__name__, swizzle_attributes_retriever(meta_funcs, separator))

        return cls

    if cls is None:
        return class_decorator
    else:
        return class_decorator(cls)


class Swizzle(types.ModuleType):
    def __init__(self):
        types.ModuleType.__init__(self, __name__)
        self.__dict__.update(sys.modules[__name__].__dict__)

    def __call__(self, cls=None, meta=False, sep = None):
        return swizzle(cls, meta, sep)

sys.modules[__name__] = Swizzle()
