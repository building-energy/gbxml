# -*- coding: utf-8 -*-


ns={'gbxml':'http://www.gbxml.org/schema'}



def get_space_ids(element):
    "Returns the space ids of a zone"
    
    zone_id=element.get('id')
    
    root_element=element.getparent()
    
    st='./gbxml:Campus/gbxml:Building/gbxml:Space'
    space_elements=root_element.xpath(st,namespaces=ns)
        
    result=[]
    for space_element in space_elements:
        
        if space_element.get('zoneIdRef')==zone_id:
            result.append(space_element.get('id'))
    
    return result