def getList(tuple):
    values = []
    for x in tuple:
        for y in x:
            values.append(y)
    return values


def getDict(tup,di):
    for a,b in tup:
        di.setdefault(a,[]).append(b)
    return di
