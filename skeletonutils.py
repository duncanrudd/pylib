import pymel.core as pmc

GREEN = 14
BLUE = 6
YELLOW = 17

def _convert_to_joint(node, parent, prefix, jnt_size, lcol, rcol, ccol):
    '''
    Creates a joint from the given node, parents it to 'parent' and named with 'prefix' + node.name()
    Copies attributes from 'node' onto the newly created joint - for example translate, rotate
    '''
    j = pmc.joint(name=prefix + node.name())
    safe_setparent(j, parent)
    j.translate.set(node.translate.get())
    j.rotate.set(node.rotate.get())
    j.setRadius(jnt_size)
    def calc_wirecolor():
        x = j.translateX.get()
        if x < -0.001:
            return rcol
        elif x > 0.001:
            return lcol
        else:
            return ccol
    j.overrideColor.set(calc_wirecolor())
    j.overrideEnabled.set(1)
    return j

def convert_to_skeleton(rootnode, prefix='skel', jnt_size=1.0, lcol=BLUE, rcol=GREEN, ccol=YELLOW, _parent=None):
    '''
    Converts a hierarchy of nodes into joints that have the same transform. Joint names are prefixed with 'prefix'.
    :param rootnode: The root PyNode, everything under it will be oonverted.
    :param prefix: String to prefix newly created nodes with
    :param _parent:
    :return: Newly created rootnode
    '''
    # Set the parent to rootnode.parent() if _parent = None
    if _parent == None:
        _parent = rootnode.getParent()
    j = _convert_to_joint(rootnode, _parent, prefix, jnt_size, lcol, rcol, ccol)
    # Convert all the children recursively using the newly created joint as the parent
    for c in [child for child in rootnode.getChildren() if 'Transform' in repr(child)]:
        convert_to_skeleton(c, prefix, jnt_size, lcol, rcol, ccol, j)
    return j

def safe_setparent(node, parent):
    '''
    node.setParent(parent) if 'parent' is not the same as node's current parent
    '''
    if node.getParent() != parent:
        node.setParent(parent)

def ancestors(node):
    '''
    Return a list of ancestors, starting with the direct parent and ending the top level (root) parent.
    '''
    result = []
    parent = node.getParent()
    while parent is not None:
        result.append(parent)
        parent = parent.getParent()
    return result

def uniqueroots(nodes):
    '''
    Return a list of the nodes in 'nodes' that are not children of any node in 'nodes'
    '''
    result = []
    def handle_node(n):
        '''
        If any of the ancestors of 'n' are in result, just return.
        Otherwise, append to result
        '''
        for ancestor in ancestors(n):
            if ancestor in nodes:
                return
        result.append(n)
    for node in nodes:
        handle_node(node)
    return result