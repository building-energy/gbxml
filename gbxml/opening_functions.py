# -*- coding: utf-8 -*-

from . import surface_functions

ns={'gbxml':'http://www.gbxml.org/schema'}


def get_surface_id(element):
    "Returns the parent surface id of an opening"
    
    surface_element=element.getparent()
    return surface_element.get('id')
    

def get_coordinates(element):
    "Returns the coordinates of an opening"
    return surface_functions.get_coordinates(element)


def get_area(element):
    "Returns the area of an opening"
    return surface_functions.get_area(element)

