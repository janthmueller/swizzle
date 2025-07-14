import unicodedata


def split_attr_name(s, split, sep=""):
    if split == "by_sep":
        return s.split(sep)

    step = split + len(sep)
    if step == 0 or (len(s) + len(sep)) % step:
        raise AttributeError(
            f"length of {s} is incompatible with split={split} and sep={sep}"
        )

    parts = [s[i : i + split] for i in range(0, len(s), step)]
    if sep.join(parts) != s:
        raise AttributeError("separator positions or values don’t match")

    return parts


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
    for ch in s:
        if ch == "_":
            continue
        cat = unicodedata.category(ch)
        if not (cat.startswith("L") or cat == "Nd"):
            return False
    return True
