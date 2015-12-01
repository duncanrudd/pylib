from qtshim import wrapinstance, QtGui, QtCore
import maya.OpenMayaUI as OpenMayaUI

def get_maya_window():
    '''
    returns the QMainWindow for the main maya window
    '''
    winptr = OpenMayaUI.MQtUtil.mainWindow()
    if winptr is None:
        raise RuntimeError('No Maya window found')
    window = wrapinstance(winptr)
    assert isinstance(window, QtGui.QMainWindow)
    return window