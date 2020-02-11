# -*- coding: utf-8 -*-

from . import xml_functions, surface_functions

ns={'gbxml':'http://www.gbxml.org/schema'}


def get_surface_ids(element):
    "Returns ids of surfaces adjacent to a Space"
    
    space_id=element.get('id')
    
    campus_element=element.getparent().getparent()
    
    surface_ids=xml_functions.get_ids(campus_element,'Surface')
    
    result=set()
    for surface_id in surface_ids:
        
        st='./gbxml:Surface[@id="%s"]' % surface_id
        surface_element=campus_element.xpath(st,namespaces=ns)[0]
        
        if surface_functions.get_inner_space_id(surface_element)==space_id:
            result.add(surface_id)
            
        if surface_functions.get_outer_space_id(surface_element)==space_id:
            result.add(surface_id)
    
    return list(result)
    