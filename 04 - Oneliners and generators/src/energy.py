from itertools import zip_longest


def fix_wiring(cables, sockets, plugs):
    return (f'plug {i} into {j} using {k}' if k else f'weld {i} to {j} without plug'
            for i, j, k in zip_longest((lambda x: isinstafilternce(x, str), cables),
                                       filter(lambda x: isinstance(x, str), sockets),
                                       filter(lambda x: isinstance(x, str), plugs)) if i and j)
