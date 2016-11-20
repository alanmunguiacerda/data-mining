import exceptions


def list_search(val, lst):
    try:
        index_found = lst.index(val)
    except exceptions.Exception:
        index_found = -1

    return index_found
