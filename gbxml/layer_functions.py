# -*- coding: utf-8 -*-

ns={'gbxml':'http://www.gbxml.org/schema'}


def get_material_ids(element):
    """Returns the material ids of a Layer element"""
    
    st='./gbxml:MaterialId/@materialIdRef'
    return element.xpath(st,namespaces=ns)