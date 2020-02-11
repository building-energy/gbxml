# -*- coding: utf-8 -*-

from . import space_functions

ns={'gbxml':'http://www.gbxml.org/schema'}



def get_space_ids(element):
    "Returns the space ids of a building"
    
    st='./gbxml:Space/@id' 
    return element.xpath(st,namespaces=ns)


def get_surface_ids(element):
    "Returns the surface ids of a building"
    
    space_ids=get_space_ids(element)
    
    result=set()
    for space_id in space_ids:
        
        st='./gbxml:Space[@id="%s"]' % space_id 
        space_element=element.xpath(st,namespaces=ns)[0]
        
        surface_ids=space_functions.get_surface_ids(space_element)
        
        result.update(surface_ids)
    
    return list(result)
    
    
        

        
    