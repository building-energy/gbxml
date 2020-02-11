# -*- coding: utf-8 -*-

from lxml import etree

ns={'gbxml':'http://www.gbxml.org/schema'}


def get_ids(element,tag):
    "Returns the ids for the specified tag"
    st='//gbxml:%s/@id' % tag
    return element.xpath(st,namespaces=ns)

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
    

def get_child_tag_attributes(element,child_tag):
    "Returns the text of a children with a specified tag"
    return [dict(child.attrib) for child in element
            if child.tag.split('}')[1]==child_tag]
    
    
def get_children_list(element):
    "Returns a list of dicts representing each child element"
    return [{'tag':child.tag.split('}')[1],
             'text':child.text,
             'attributes':dict(child.attrib)}
            for child in element]
            