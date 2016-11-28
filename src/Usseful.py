import exceptions

def list_search(val, lst):
    try:
        index_found = lst.index(val)
    except exceptions.Exception:
        index_found = -1

    return index_found

def take_out_class(data, class_index):
    ls = []
    for elem in data:
        aux = elem[0:class_index]
        aux.extend(elem[class_index + 1:len(elem)])
        ls.append(aux)

    return ls

def index_in_range(index, lst):
    if index >= len(lst):
        print 'Index out of bounds'
        return False
    return True