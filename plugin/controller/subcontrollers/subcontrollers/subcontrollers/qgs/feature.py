

def getvalue(feature, key):
    try: return feature[key]
    except KeyError: pass

getValue = getvalue

def setvalue(feature, key, value):
    try:
        feature[key] = value
        return True
    except KeyError:
        return False

setValue = setvalue
