# -*- coding: utf-8 -*-

from . import layer_functions

ns={'gbxml':'http://www.gbxml.org/schema'}


def get_layer_ids(element):
    """Returns the layer ids of a Construction element
    """
    
    st='./gbxml:LayerId/@layerIdRef'
    return element.xpath(st,namespaces=ns)


def get_material_ids(element):
    "Returns the material ids of a Construction element"
    
    layer_ids=get_layer_ids(element)
    
    material_ids=[]
    for layer_id in layer_ids:
        st='./gbxml:Layer[@id="%s"]' % layer_id
        layer_element=element.getparent().xpath(st,namespaces=ns)[0]
        material_ids+=layer_functions.get_material_ids(layer_element)
    
    return material_ids