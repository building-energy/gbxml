# -*- coding: utf-8 -*-

from lxml import etree     

class Gbxsd():
    "A class representing a gbXML xsd file"
    
    def __init__(self,fp):
        """Initialises the object
        
        - Reads in the .xsd file
        - Sets the namespace variable
        
        """
        self._ElementTree=self._read(fp)
        self.ns={'a':'http://www.w3.org/2001/XMLSchema'}
    
    
# HIDDEN METHODS
    
    def _attribute(self,element_name,attribute_name):
        """Returns an attribute lxml node
        
        Arguments:
            -element_name (str): the name of the element node
            -attribute_name (str): the name of the attribute node
        
        """
        e=self._element(element_name)
        st='.//a:attribute[@name="%s"]' % (attribute_name)
        return e.xpath(st,namespaces=self.ns)[0]
    
    
    def _element(self,name):
        """Returns an element node 
        
        Arguments:
            -name (str): the name of the element node
        
        """
        st='/a:schema/a:element[@name="%s"]' % (name)
        return self._ElementTree.getroot().xpath(st,namespaces=self.ns)[0]
    
    
    def _element_attributes(self,name):
        """Returns the attribute nodes of an element
        
        """
        e=self._element(name)
        st='.//a:attribute'
        return e.xpath(st,namespaces=self.ns)
    
    
    def _element_children(self,name):
        """Returns the child element nodes of an element
        
        
        """
        e=self._element(name)
        st='.//a:element'
        return e.xpath(st,namespaces=self.ns)
    
    
    def _node_children_dict(self,xpath):
        """A recursive function which shows the structure of the xsd file.
        
        This is used for information only, to see what is going on within 
            the xsd file when designing this class
        
        """
        s=set()
        st=xpath+'/a:*'
        l=self._ElementTree.getroot().xpath(st,namespaces=self.ns)
        l=[x.tag.split('}')[1] for x in l]
        s.update(l)
        d={}
        for x in s:
            st=xpath+'/a:%s' % (x)
            #attributes
            s1=set()
            l=self._ElementTree.getroot().xpath(st,namespaces=self.ns)
            for l1 in l:
                s1.update(list(l1.attrib.keys()))
            d1=self._node_children_dict(st)
            d[x + ' ' + (str(s1) if s1 else '{None}')]=d1 if d1 else None
        return d
    
    
    def _read(self,fp):
        """Reads a gbXML schema file and returns an etree object
        
        Arguments:
            fp (str): the filepath 
        
        """
        return etree.parse(fp)
    
    
    def _simpleType(self,name):
        """Returns a simpleType element
        
        The simpleType element is a child of the schema element
        
        Arguments:
            -name (str): the name of the simpleType element
        
        """
        st='/a:schema/a:simpleType[@name="%s"]' % (name)
        l=self._ElementTree.getroot().xpath(st,namespaces=self.ns)
        if len(l)>0:
            return l[0]
        else:
            raise KeyError("There is no simpleType with the name '%s'" % name)
    
    
    def _simpleType_exists(self,name):
        """Returns True if the simpleType exists, otherwise False
        
        """
        try:
            self._simpleType(name)
            return True
        except KeyError:
            return False
        
        
# ELEMENT METHODS
        
    def element_names(self):
        """Returns a list of all element names
        
        """
        st='/a:schema/a:element/@name'
        return self._ElementTree.getroot().xpath(st,namespaces=self.ns)
    
    
    def element_text_data_type(self,name):
        pass
        
    
    def element_attributes_exist(self,name):
        """Returns True if the element can contain attributes, otherwise false        
        
        """
        l=self._element_attributes(name)
        return len(l)>0
    
    
    def element_attributes_properties(self,name):
        """Returns a list with the properties of the attributes
        
        return is a list of dictionaries i.e. 
            [{'name': 'id', 'type': 'xsd:ID'}, {'name': 'engine'},...]
        
        """
        l=self._element_attributes(name)
        l1=[dict(x.attrib) for x in l]
        return l1
    
    
    def element_children_exist(self,name):
        """Returns True if the element can contain child elements, otherwise false        
        
        """
        l=self._element_children(name)
        return len(l)>0
        
    
    def element_children_specification(self,name):
        """Returns a list with the child attributes
        
                
        """
        e=self._element(name)
        st='.//a:all'
        l=e.xpath(st,namespaces=self.ns)
        st='.//a:choice'
        l+=e.xpath(st,namespaces=self.ns)
        l1=[{'tag':x.tag.split('}')[1],**dict(x.attrib)} for x in l]
        return l1
    
    
    def element_children_properties(self,name):
        """Returns a list with the child attributes
        
        return is a list of dictionaries i.e. 
            [{'ref': 'aecXML', 'minOccurs': '0'}, {'ref': 'Campus'},...]
        
        """
        l=self._element_children(name)
        l1=[dict(x.attrib) for x in l]
        return l1
    
    
    
    
    
    
    
# ATTRIBUTE METHODS
    
    
    def attribute_restriction_values(self,element_name,attribute_name):
        """Returns the possible values of a restricted attribute
        
        Return value is a list of strings.
        
        If no restriction values are present then an empty list is returned.
        
        """
        def _simpleType_values(simpleType_element):
            "Returns the restriction values for a simpleType element"
            st='./a:restriction/a:enumeration/@value'
            return simpleType_element.xpath(st,namespaces=self.ns)
        
        a=self._attribute(element_name,attribute_name)
        st='./a:simpleType'
        l=a.xpath(st,namespaces=self.ns)
        if len(l)>0:
            s=l[0]
            return _simpleType_values(s)
        typ=a.get('type')
        try:
            s=self._simpleType(typ)
            return _simpleType_values(s)
        except KeyError:
            return []
    
    
    def attribute_restrictions_exist(self,element_name,attribute_name):
        """Returns True if the attribute has restrictions, otherwise False
        
        """
        a=self._attribute(element_name,attribute_name)
        st='.//a:restriction'
        l=a.xpath(st,namespaces=self.ns)
        if len(l)>0: return True
        typ=a.get('type')
        if typ:
            b=self._simpleType_exists(typ)
            if b: return True
        return False
    
    
    
    
    
    
    
   
    
    
    
    
    
    
#    def element_type(self,element_name):
#        """Returns the 'type' or 'base' attribute of an element
#        """
#        e=self._element(element_name)
#        typ=e.get('type',None)
#        if typ: return typ
#        st='./a:simpleType/a:restriction/@base'
#        typ=e.xpath(st,namespaces=self.ns)
#        if typ: return typ[0]
#        st='./a:complexType/a:simpleContent/a:extension/@base'
#        typ=e.xpath(st,namespaces=self.ns)
#        if typ: return typ[0]
#        return None
        
    

        
    
    
    
    
    
    
    
    
    
    
    
    
#
#
#def read(fp):
#    """Reads a gbxml schema file and returns an etree object
#    
#    Arguments:
#        fp (str): the filepath of the gbxml schema file
#    
#    """
#    return etree.parse(fp)
#

#    
#def _show_schema_children(xsd):
#    "Returns a dictionary of nodes and their children"
#    return _node_children_dict(xsd,'')
#
#
#def annotations(xsd,node):
#    """Returns the annotations for a given node
#    """
#    st='./a:annotation/a:documentation/text()'
#    #print(st)
#    return node.xpath(st,namespaces=ns)
#
#
#def element(xsd,name):
#    """Returns an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    st='/a:schema/a:element[@name="%s"]' % (name)
#    #print(st)
#    return xsd.getroot().xpath(st,namespaces=ns)[0]
#
#
#def element_attribute(xsd,element_name,attribute_name):
#    """Returns an attribute node of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -attribute_name (str): the name of the element node
#    
#    """
#    e=element(xsd,element_name)
#    st='./a:complexType/a:attribute[@name="%s"]' % attribute_name 
#    #print(st)
#    return e.xpath(st,namespaces=ns)[0]
#
#
#def element_attribute_annotations(xsd,element_name,attribute_name):
#    """Returns the annotations of an attribute of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -attribute_name (str): the name of the element node
#    
#    """
#    e=element_attribute(xsd,element_name,attribute_name)
#    #print(st)
#    return annotations(xsd,e)
#
#
#def element_attribute_enumeration_values(xsd,element_name,attribute_name):
#    """Returns the annotations of an attribute of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -attribute_name (str): the name of the element node
#    
#    """
#    e=element_attribute(xsd,element_name,attribute_name)
#    st='./a:simpleType/a:restriction/a:enumeration/@value'
#    #print(st)
#    return e.xpath(st,namespaces=ns)
#
#
#def element_attribute_type(xsd,element_name,attribute_name):
#    """Returns the type of an attribute of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -attribute_name (str): the name of the element node
#    
#    """
#    e=element_attribute(xsd,element_name,attribute_name)
#    #print(st)
#    return e.get('type')
#
#
#def element_attribute_use(xsd,element_name,attribute_name):
#    """Returns the use of an attribute of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -attribute_name (str): the name of the element node
#    
#    """
#    e=element_attribute(xsd,element_name,attribute_name)
#    #print(st)
#    return e.get('use')
#
#
#def element_attributes(xsd,name):
#    """Returns a list of the attributes of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    e=element(xsd,name)
#    st='./a:complexType/a:attribute' 
#    #print(st)
#    return e.xpath(st,namespaces=ns)
#    
#
#def element_attributes_names(xsd,name):
#    """Returns a list of the names of attributes of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    l=element_attributes(xsd,name)
#    #print(st)
#    return [x.get('name') for x in l]
#
#
#def element_child(xsd,element_name,child_name):
#    """Returns an element child of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -child_name (str): the name of the child node
#    
#    """
#    e=element(xsd,element_name)
#    st='./a:complexType/a:choice/a:element[@ref="%s"]' % child_name 
#    #print(st)
#    return e.xpath(st,namespaces=ns)[0]
#
#
#def element_child_properties(xsd,element_name,child_name):
#    """Returns a dict with the properties of an element child of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -element_name (str): the name of the element node
#        -child_name (str): the name of the child node
#    
#    """
#    e=element_child(xsd,element_name,child_name)
#    return e.attrib
#
#
#def element_children(xsd,name):
#    """Returns a list of the element children of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    e=element(xsd,name)
#    st='./a:complexType/a:choice/a:element' 
#    #print(st)
#    return e.xpath(st,namespaces=ns)
#    
#
#def element_children_names(xsd,name):
#    """Returns a list of the names of element children of an element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    l=element_children(xsd,name)
#    #print(st)
#    return [x.get('ref') for x in l]
#
#
#def element_complexType_is_simpleContent(xsd,name):
#    """Returns True if the element complexType has a singleContent node
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    e=element(xsd,name)
#    st='./a:complexType/a:simpleContent' 
#    #print(st)
#    b=len(e.xpath(st,namespaces=ns))>0
#    return b
#
#
#def element_complexType_simpleContent_attributes(xsd,name):
#    """Returns a list of the attributes of an simpleContent element node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    e=element(xsd,name)
#    st='./a:complexType/a:simpleContent/a:extension/a:attribute' 
#    #print(st)
#    return e.xpath(st,namespaces=ns)
#
#
#def element_complexType_simpleContent_base(xsd,name):
#    """Returns the base of the simpleContent of an element
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    e=element(xsd,name)
#    st='./a:complexType/a:simpleContent/a:extension/@base' 
#    #print(st)
#    return e.xpath(st,namespaces=ns)[0]
#
#
#def element_is_complexType(xsd,name):
#    """Returns True if the element has a complexType node
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the element node
#    
#    """
#    e=element(xsd,name)
#    st='./a:complexType' 
#    #print(st)
#    b=len(e.xpath(st,namespaces=ns))>0
#    return b
#
#
#def elements_names(xsd):
#    """Returns a list of the element names
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#    
#    """
#    st='/a:schema/a:element/@name'
#    #print(st)
#    return xsd.getroot().xpath(st,namespaces=ns)
#
#
#def simpleType(xsd,name):
#    """Returns a simpleType node 
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the simpleType node
#    
#    """
#    st='/a:schema/a:simpleType[@name="%s"]' % (name)
#    #print(st)
#    return xsd.getroot().xpath(st,namespaces=ns)[0]
#
#
#def simpleType_annotations(xsd,name):
#    """Returns a list of the simpleType annotations
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the simpleType node
#        
#    """
#    e=simpleType(xsd,name)
#    return annotations(xsd,e)
#
#
#def simpleType_emuneration_annotations(xsd,simpleType_name,enumeration_name):
#    """Returns a list of the annotations for an enumeration in a simpleType node
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -simpleType_name (str): the name of the simpleType node
#        -enumeration_name (str): the name of the enumeration node
#        
#    """
#    e=simpleType_enumeration(xsd,simpleType_name,enumeration_name)
#    return annotations(xsd,e)
#
#
#def simpleType_enumeration(xsd,simpleType_name,enumeration_name):
#    """Returns a simpleType enumeration node
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -simpleType_name (str): the name of the simpleType node
#        -enumeration_name (str): the name of the enumeration node
#        
#    """
#    e=simpleType(xsd,simpleType_name)
#    st='./a:restriction/a:enumeration[@value="%s"]' % (enumeration_name)
#    #print(st)
#    return e.xpath(st,namespaces=ns)[0]
#    
#
#def simpleType_enumerations_values(xsd,name):
#    """Returns a list of the simpleType enumerations values
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        -name (str): the name of the simpleType node
#        
#    """
#    e=simpleType(xsd,name)
#    st='./a:restriction/a:enumeration/@value'
#    #print(st)
#    return e.xpath(st,namespaces=ns)
#
#
#def simpleType_names(xsd):
#    """Returns a list of the simpleType names
#    
#    Arguments:
#        -xsd (lxml.etree._ElementTree): the gbxml schema
#        
#    """
#    st='/a:schema/a:simpleType/@name'
#    #print(st)
#    return xsd.getroot().xpath(st,namespaces=ns)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#def _element_type(self,e):
#    "Returns the type of element e"
#    #type attribute
#    if 'type' in e.attrib:
#        return e.get('type')
#    #simpleType
#    xpath='./a:simpleType/a:restriction/@base'
#    result=e.xpath(xpath,namespaces=self.ns)
#    if result:
#        return result[0]
#    #complexType
#    xpath='./a:complexType/a:simpleContent/a:extension/@base'
#    result=e.xpath(xpath,namespaces=self.ns)
#    if result:
#        return result[0]
#    return None
#
#
#def element_type(xsd,name):
#    "Returns the type of a given element name"
#    e=self.element_dict[name]
#    return self._element_type(e)
#
#
#
#
#
#
#
#def elements(xsd):
#        "Returns a dictionary of the schema elements"
#        xpath='./a:element'
#        ebunch=xsd.getroot().xpath(xpath,namespaces=ns)
#        return {e.get('name'):e for e in ebunch}
#
#  
#def simpleTypes(self):
#    "Returns a dictionary of the simpleTypes which are children of the 'schema' element"
#    xpath='./a:simpleType[@name]'
#    ebunch=self.schema.getroot().xpath(xpath,namespaces=self.ns)
#    return{e.get('name'):e for e in ebunch}
#
#
#def _attributes(self,e):
#    """
#    Returns a dictionary of attributes for a given element
#    
#    """
#    xpath='.//a:attribute'
#    ebunch=e.xpath(xpath,namespaces=self.ns)
#    return {e.get('name'):e for e in ebunch}
#
#
#def attributes(self,name):
#    """
#    Returns a dictionary of attributes for a given element name
#    
#    """
#    e=self.element_dict[name]
#    return self._attributes(e)
#
#
#def _attribute_simpleType(self,e):
#    """
#    Returns the simpleType element of an attribute element e
#    
#    """
#    #looks for a simpleType child
#    xpath='./a:simpleType'
#    result=e.xpath(xpath,namespaces=self.ns)
#    if len(result)>0: 
#        return result[0]
#    #else looks for a type attribute
#    xpath='./@type'
#    t=e.xpath(xpath,namespaces=self.ns)[0]
#    return self.simpleType_dict[t]
#
#
#def _enumurations(self,e):
#    """
#    Returns a dict of enumerations elements for a given simpleType element
#    """
#    xpath='.//a:enumeration'
#    ebunch=e.xpath(xpath,namespaces=self.ns)
#    return {e.get('value'):e for e in ebunch}
#
#
#def enumurations(self,element_name,attribute_name):
#    """
#    Returns a dict of enumerations elements for a given element name and attribute name
#    """
#    e=self.attributes(element_name)[attribute_name] 
#    e1=self._attribute_simpleType(e)
#    return self._enumurations(e1)
#
#
#def child_element_bounds(self,element_tag,child_tag):
#    """
#    Returns the bounds of the child element 'child' in element 'e
#    """
#    e=self.element_dict[element_tag]
#    xpath='./a:complexType/a:choice/a:element[@ref="{0}"]|./a:complexType/a:all/a:element[@ref="{0}"]'.format(child_tag)
#    child=e.xpath(xpath,namespaces=self.ns)[0]
#    minOccurs=child.get('minOccurs')
#    maxOccurs=child.get('maxOccurs')
#    return minOccurs,maxOccurs
#

