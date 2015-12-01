import pymel.core as pmc
import sys
import types
import webbrowser

HELP_ROOT_URL = ('http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/PyMel/')

def syspath():
    print 'sys.path:'
    for p in sys.path:
        print '    ' + p

def info(obj):
    '''Prints information about the object'''

    lines = ['Info for %s' % obj.name(),
             'Attributes:']

    # Get the name of all attributes
    for a in obj.listAttr():
        lines.append('    ' + a.name())

    # Get the names of all the object's relatives
    lines.append('Relatives of %s:' % obj.name())
    for r in obj.listRelatives():
        lines.append('    ' + r.name())

    # Method resolution order (I think this results in an inheritance hierarchy for obj's 'type')
    lines.append('MEL type: %s' % obj.type())
    lines.append('MRO:')
    lines.extend(['    ' + t.__name__ for t in type(obj).__mro__])

    result = '\n'.join(lines)
    print result

def _py_to_helpstr(obj):
    if isinstance(obj, basestring):
        return 'search.html?q=%s' % (obj.replace(' ', '+'))
    if not _is_pymel(obj):
        return None
    if isinstance(obj, types.ModuleType):
        return ('generated/%(module)s.html#module-%(module)s' % dict(module=obj.__name__))
    if isinstance(obj, types.MethodType):
        return ('generated/classes/%(module)s/%(module)s.%(typename)s.html'
                '#%(module)s.%(typename)s.%(methname)s' % dict(module=obj.__module__, typename=obj.im_class.__name__, methname=obj.__name__))
    if isinstance(obj, types.FunctionType):
        return ('generated/functions/%(module)s/%(module)s.%(funcname)s.html'
                '#%(module)s.%(funcname)s' % dict(module=obj.__module__, funcname=obj.__name__))
    if not isinstance(obj, type):
        obj = type(obj)
    return ('generated/classes/%(module)s/%(module)s.%(typename)s.html'
            '#%(module)s.%(typename)s' % dict(module=obj.__module__, typename=obj.__name__))

def test_py_to_helpstr():
    def dotest(obj, ideal):
        result = _py_to_helpstr(obj)
        assert result == ideal, '%s != %s' % (result, ideal)
    # basestring test
    dotest('maya rocks', 'search.html?q=maya+rocks')

    # pmc nodetypes test for modules
    dotest(pmc.nodetypes, 'generated/pymel.core.nodetypes.html'
                            '#module-pymel.core.nodetypes')

    dotest(pmc.nodetypes.Joint,
           'generated/classes/pymel.core.nodetypes/'
           'pymel.core.nodetypes.Joint.html'
           '#pymel.core.nodetypes.Joint')

    dotest(pmc.nodetypes.Joint(),
           'generated/classes/pymel.core.nodetypes/'
           'pymel.core.nodetypes.Joint.html'
           '#pymel.core.nodetypes.Joint')

    dotest(pmc.nodetypes.Joint().getTranslation,
           'generated/classes/pymel.core.nodetypes/'
           'pymel.core.nodetypes.Joint.html'
           '#pymel.core.nodetypes.Joint.getTranslation')

    dotest(pmc.joint,
           'generated/functions/pymel.core.animation/'
           'pymel.core.animation.joint.html'
           '#pymel.core.animation.joint')

    # non pymel object tests
    dotest(object(), None)
    dotest(10, None)
    dotest([], None)
    dotest(sys, None)


def _is_pymel(obj):
    try:
        module= obj.__module__
    except AttributeError:
        try:
            module = obj.__name__
        except AttributeError:
            return None
    return module.startswith('pymel')

def pmhelp(obj):
    '''
    gives help for a pymel or python object
    If obj os not a PyMel object, use python's built in 'help' function
    If obj is a string, open a web browser to a search in the pymel help for the string
    Otherwise, open a web browser to the page for the object
    '''
    tail = _py_to_helpstr(obj)
    if tail is None:
        help(obj)
    else:
        webbrowser.open(HELP_ROOT_URL + tail)

def is_exact_type(node, typename):
    '''
    node.type() == typename
    '''
    return node.type() == typename

def is_type(node, typename):
    '''
    Return true if node.type() == typename or any subclass of typename
    '''
    return typename in node.nodetype(inherited=True)

