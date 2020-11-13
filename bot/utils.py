def get_index(lst, i, default=None):
    try:
        return lst[i]
    except IndexError:
        return default