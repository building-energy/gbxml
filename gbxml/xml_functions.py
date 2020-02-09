# -*- coding: utf-8 -*-

from lxml import etree

def get_xmlstring(element):
    """Returns a string of the contents of an xml element
    """
    return etree.tostring(element,pretty_print=True).decode()


def get_attributes(element):
    "Returns the attributes of an element as a dictionary"
    return dict(element.attrib)


def get_child_tags(element):
    "Returns the child tags of an element"
    return [child.tag.split('}')[1] for child in element]
    
    
def get_child_tag_text(element,child_tag):
    "Returns the text of a children with a specified tag"
    return [child.text for child in element
            if child.tag.split('}')[1]==child_tag]