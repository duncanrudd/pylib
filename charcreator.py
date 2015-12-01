import pymel.core as pmc
import skeletonutils

GREEN = 14
BLUE = 6
YELLOW = 17

SETTINGS_DEFAULT = {'joint_size':1.0,
                    'right_colour': BLUE,
                    'left_colour':GREEN,
                    'centre_colour':YELLOW,
                    'prefix':'char_'}

def convert_hierarchies_main(settings=SETTINGS_DEFAULT):
    '''
    Convert hierarchies(pmc.selection())
    Prints and provides user feedback so only call from UI
    '''
    nodes = pmc.selected(type='transform')
    pmc.select(clear=1)
    if not nodes:
        pmc.warning('No Transforms Selected')
        return
    new_roots = convert_hierarchies(nodes, settings)
    print 'Created: ', ','.join([r.name() for r in new_roots])

def convert_hierarchies(rootnodes, settings=SETTINGS_DEFAULT):
    '''
    Converts hierarchy for each root node in 'rootnodes'
    So passing in '[parent, child]' would convert the 'parent' hierarchy assuming 'child lives under it.
    '''
    roots = skeletonutils.uniqueroots(rootnodes)
    result = [convert_hierarchy(r, settings) for r in roots]
    return result

def convert_hierarchy(node, settings=SETTINGS_DEFAULT):
    '''
    Converts the hierarchy under the included 'rootnode' into joints in the same namespace as 'rootnode'
    Deletes 'rootnode' and its hierarchy
    Connections to nodes are not preserved on the newly created joints.
    '''
    result = skeletonutils.convert_to_skeleton(node,
                                               jnt_size = settings['joint_size'],
                                               prefix = settings['prefix'],
                                               rcol = settings['right_colour'],
                                               lcol = settings['left_colour'],
                                               ccol = settings['centre_colour'])
    pmc.delete(node)
    return result