import hierarchyconvertergui as hierconvgui
import mayautils
import maya.OpenMaya as OpenMaya
import pymel.core as pmc
import charcreator

_window = None

def show():
    global _window
    if _window is None:
        cont = hierconvgui.HierarchyConverterController()

        def emit_selchanged(_):
            cont.selectionChanged.emit(pmc.selected(type='transform'))
        OpenMaya.MEventMessage.addEventCallback('SelectionChanged', emit_selchanged)
        parent = mayautils.get_maya_window()
        _window = hierconvgui.create_window(cont, parent)

        def onconvert(prefix):
            settings = dict(charcreator.SETTINGS_DEFAULT, prefix=unicode(prefix))
            charcreator.convert_hierarchies_main(settings)

        _window.convertClicked.connect(onconvert)
    _window.show()