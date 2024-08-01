from functools import wraps
import sys
import types

__version__ = "0.1.4"

def _split(s, sep):
    if sep == '':
        return list(s)
    else:
        return s.split(sep)
    
def _swizzle(func, sep = None):
    def _getattr(obj, name, default=object()):
        try:
            return func(obj, name)
        except AttributeError:
            return default

    @wraps(func)
    def _swizzle_attributes(obj, name):
        """Find attributes of an object that match substrings of a given name."""
        try:
            return func(obj, name)
        except AttributeError:
            pass
        if sep is not None:
            names = _split(name, sep)
            found_attributes = [func(obj, n) for n in names]
        else:
            found_attributes = []
            sentinel = object()
            i = 0
            while i < len(name):
                match_found = False
                for j in range(len(name), i, -1):
                    substr = name[i:j]
                    attr = _getattr(obj, substr, sentinel)
                    if attr is not sentinel:
                        found_attributes.append(attr)
                        i = j  # Move index to end of the matched substring
                        match_found = True
                        break
                if not match_found:
                    raise AttributeError(f"No matching attribute found for substring: {name[i:]}")
        return tuple(found_attributes) 
    return _swizzle_attributes
    
def swizzle(cls=None, meta = False, sep = None):
    def decorator(cls):
        # Decorate the class's __getattr__ or __getattribute__
        cls_fn = cls.__getattr__ if hasattr(cls, '__getattr__') else cls.__getattribute__
        setattr(cls, cls_fn.__name__, _swizzle(cls_fn, sep)) 

        # Handle the meta class
        if meta:
            meta_cls = type(cls)
            if meta_cls == type:
                class SwizzleType(meta_cls): pass
                meta_cls = SwizzleType
                cls = meta_cls(cls.__name__, cls.__bases__, dict(cls.__dict__))
            meta_fn = meta_cls.__getattr__ if hasattr(meta_cls, '__getattr__') else meta_cls.__getattribute__
            setattr(meta_cls, meta_fn.__name__, _swizzle(meta_fn, sep))
        return cls

    if cls is None:
        return decorator
    else:
        return decorator(cls)
        
class Swizzle(types.ModuleType):
    def __init__(self):
        types.ModuleType.__init__(self, __name__)
        self.__dict__.update(sys.modules[__name__].__dict__)
    
    def __call__(self, cls=None, meta=False, sep = None):
        return swizzle(cls, meta, sep)

sys.modules[__name__] = Swizzle()
        