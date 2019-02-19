import collections

# Inspired by https://stackoverflow.com/a/3233356

def deep_update(d: dict, u: dict) -> dict:
    if not isinstance(d, collections.Mapping):
        return d

    for k, v in u.items():
        if v is None:
            continue
        if isinstance(v, collections.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d