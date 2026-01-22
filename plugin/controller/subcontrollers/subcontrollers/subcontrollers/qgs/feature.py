

################################################################################
###
################################################################################
'''
The problem with QGIS is that they still use QVariant under some circumstances.
A feature attribute which is NULL may return as QVariant(NULL), or as None,
depending on how the value was originally conceived.
QVariant(NULL) == None, evaluates to True
QVariant(NULL) is None, evalautes to False
'''
def getvalue(feature, key):
    try:
        value = feature[key]
        if value != None: return value
    except KeyError: pass

getValue = getvalue

def setvalue(feature, key, value):
    try:
        feature[key] = value
        return True
    except KeyError:
        return False

setValue = setvalue
