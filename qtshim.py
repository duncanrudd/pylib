from PySide import QtCore, QtGui
import shiboken
Signal = QtCore.Signal

def _getcls(name):
    result = getattr(QtGui, name, None)
    if result is None:
        result = getattr(QtCore, name, None)
    return result

def wrapinstance(ptr):
    '''
    converts a pointer ( int or long ) into the concrete PyQt/PySide object it represents
    '''
    ptr = long(ptr)
    qobj = shiboken.wrapInstance(ptr, QtCore.QObject)
    metaobj = qobj.metaObject()
    realcls = None
    while realcls is None:
        realcls = _getcls(metaobj.className())
        metaobj = metaobj.superClass()
    return shiboken.wrapInstance(ptr, realcls)
