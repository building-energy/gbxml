# -*- coding: utf-8 -*-

from lxml import etree
from .gbxsd import Gbxsd
#from pkg_resources import resource_filename
import pkgutil
from io import BytesIO

class Gbxml():
    "An object that represents a gbXML dataset"
    
    def __init__(self,
                 xml_fp=None,
                 xsd_fp=None):
        """Initialises a new Gbxml instance
        
        Arguments:
            xml_fp (str): filepath to a gbXML file. This is read in as an 
                lxml._ElementTree object. If not supplied then a 
                new lxml._ElementTree object with only a root element is created.
                
            xsd_fp (str): filepath to a gbXML schema file. If not supplied 
                then a default gbXMl schema file is used.
                
        """
        if xml_fp: 
            self._ElementTree=self._read(xml_fp)
        else:
            st = pkgutil.get_data(__package__, 'blank.xml')
            self._ElementTree=self._read(BytesIO(st))
            
        self.ns={'gbxml':'http://www.gbxml.org/schema'}
        
        if xsd_fp:
            self.gbxsd=Gbxsd(xsd_fp)
        else:
            st = pkgutil.get_data(__package__, 'GreenBuildingXML_Ver6.01.xsd')
            self.gbxsd=Gbxsd(BytesIO(st))
        
    
    def _read(self,fp):
        """Reads a xml file and returns an etree object
        
        Arguments:
            fp (str): the filepath or a file-like object
        """
        return etree.parse(fp)

    
# OUTPUT
    
    
    def xmlstring(self,element=None):
        """Returns a string of an xml element
        
        Arguments:
            - element (lxml.etree._Element): default is root node
        
        """
        if element is None: element=self.root()
        return etree.tostring(element,pretty_print=True).decode()
    
    
    def xpath(self,element,st_xpath):
        """Returns the result of an xpath operation on the gbXML file
        
        Arguments
            - st_xpath (str): the xpath string
            - element (lxml.etree._Element): the element for the xpath operation. The 
                default is the root element
        
        """
        return element.xpath(st_xpath,namespaces=self.ns)
    
    
    def write(self,fp):
        """Writes the gbXML file to disc
        
        Arguments:
            fp (str): the filepath
        """
        st=etree.tostring(self.root(),xml_declaration=True)
        with open(fp,'wb') as f:
            f.write(st)
       
# VALIDATION
            
    def validate(self):
        """Validates the gbXMl file using the schema
        
        Returns True if the gbXML file is valid, otherwise False
        
        """
        xmlschema = etree.XMLSchema(self.gbxsd._ElementTree)
        result=xmlschema.validate(self._ElementTree)
        return result
        
# EDITING
        
    def add_element(self,parent_element,label,text=None,**kwargs):
        """Adds an element to the gbXML
        
        Returns the newly created element
        
        Arguments:
            - parent_element (lxml._Element or str): the parent element that the
                new element is added to. This can be either a lxml._Element object
                or a string with the element id.
            - label (str): the label or tag of the new element
            - text (str): the text of the new element
            - **kwargs (keywords): the attributes of the new element
                
        """
        if isinstance(parent_element,str):
            parent_element=self.element(parent_element)
        e=etree.SubElement(parent_element,'{%s}%s' % (self.ns['gbxml'],label))
        if text: e.text=text
        if kwargs:
            for k,v in kwargs.items():
                e.set(k,v)
        return e
    
    def set_attribute(self,element,key,value):
        """Sets the attribute of an element
        
        Returns the modified element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
            - key (str): the name of the attribute
            - value (str): the value of the attribute
        
        """
        if isinstance(element,str):
            element=self.element(element)
        element.set(key,value)
        return element
    
    
    def set_element_id(self,element,new_id):
        """Sets a new id attribute for an element and updates all links
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
            - new_id (str): 
        
        Return value:
            - new_id (str)
        
        """
        #check if new_id already exists
        l=self.elements()
        ids=[x.get('id') for x in l if x.get('id')]
        if new_id in ids:
            raise ValueError('new_id %s already exists' % new_id)
        
        #get element
        if isinstance(element,str):
            element=self.element(element)
            
        #get old id
        old_id=element.get('id')
        
        #set new id
        element.set('id',new_id)
        
        #find all elements with attribute labelRefId=old_id
        label=self.label(element)
        prefix=label[0].lower()+label[1:]
        st='.//gbxml:*[@%sIdRef="%s"]' % (prefix,old_id)
        l=self.xpath(self.root(),st)
        
        #update with id
        for e in l:
            e.set('%sIdRef' % prefix,new_id)
        #return new id 
        return new_id
    
    
    def set_text(self,element,text):
        """Sets the text of an element
        
        Returns the modified element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
            - text (str): the text
        
        """
        if isinstance(element,str):
            element=self.element(element)
        element.text=text
        return element
    
    
    def remove_element(self,element):
        """Removes an element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
        
        """
        if isinstance(element,str):
            element=self.element(element)
        
        #remove links to element
        id=element.get('id')
        label=self.label(element)
        prefix=label[0].lower()+label[1:]
        st='.//gbxml:*[@%sIdRef="%s"]' % (prefix,id)
        l=self.xpath(self.root(),st)
        for x in l:
            self.remove_attribute(x,'%sIdRef' % prefix)
    
        #remove element
        parent=element.getparent()
        parent.remove(element)
    
    
    def remove_attribute(self,element,key):
        """Removes an element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
            - key (str): The name of the attribute to delete
        
        """
        if isinstance(element,str):
            element=self.element(element)
        element.attrib.pop(key)
        
        
    def remove_text(self,element):
        pass
    
    
    
# QUERYING
       
    def elements(self,label='*'):
        """Returns the elements of the gbXML file
        
        Arguments:
            - label (str): the label of the elements
        
        """
        st='//gbxml:%s' % label
        return self.xpath(self.root(),st)
    
    
    def root(self):
        "Returns the root element"
        return self._ElementTree.getroot()
    
    
    def element(self,id,label='*'):
        """Returns an element from the gbXML file
        
        Arguments:
            - id (str): the id of the element
            - label (str): the label of the element
        
        """
        st='//gbxml:%s[@id="%s"]' % (label,id)
        try:
            return self.xpath(self.root(),st)[0]
        except IndexError:
            raise KeyError('there is no element with an id of %s' % id)
            
    
    def label(self,element):
        """Returns the label of an element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
        """
        if isinstance(element,str):
            element=self.element(element)
        return  element.tag.split('}')[1]
            
    
    def attributes(self,element):
        """Returns the attributes of an element
        
        Return value is a dictionary
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
        """
        if isinstance(element,str):
            element=self.element(element)
        return  dict(element.attrib)

    
    def text(self,element):
        """Returns the text of an element, or None
        
        Return value is a string
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
        """
        if isinstance(element,str):
            element=self.element(element)
        return element.text
        
    
    def text_value(self,element):
        """Returns the text value of an element, i.e the text converted 
            according to its schema data type
        
        Return value is an object with data type dependent on the schema
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
        """
        
        #JUST RETURNS STRINGS AT PRESENT - TO DO
        
        if isinstance(element,str):
            element=self.element(element)
        text=element.text
        return text
            
    
    def child_elements(self,element,label='*'):
        """Returns the child elements of an element
        
        Return value is a list of elements
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
            - label (str): the label of the element
        """
        if isinstance(element,str):
            element=self.element(element)
        st='./gbxml:%s' % label
        return self.xpath(element,st)
        
        
    def descendent_elements(self,element,label='*'):
        """Returns the descendent elements of an element
        
        Return value is a list of elements
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
            - label (str): the label of the element
        """
        if isinstance(element,str):
            element=self.element(element)
        st='.//gbxml:%s' % label
        return self.xpath(element,st)
    
  
# FUNCTIONS - CONSTRUCTION
        

    def construction_materials(self,construction_element):
        """Returns the material elements of a construction in order
        
        Arguments:
            - construction_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - material_elements (list)
        
        """
        l=[]
        if isinstance(construction_element,str):
            construction_element=self.element(construction_element,label='Construction')
        layerIds=self.child_elements(construction_element,label='LayerId')
        for layerId in layerIds:
            layer_id=layerId.get('layerIdRef')
            layer=self.element(layer_id,label='Layer')
            materialIds=self.child_elements(layer,label='MaterialId')
            for materialId in materialIds:
                material_id=materialId.get('materialIdRef')
                material=self.element(material_id,label='Material')
                l.append(material)
        return l
    
# OPENING FUNCTIONS
        
    def opening_coordinates(self,opening_element):
        """Returns a list of coordinate tuples
        
        Arguments:
            - opening_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - coordinates (list): a list where each item is a tuple of (x,y,z) coordinates.
                i.e. [(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),...]
                or None
                
        """
        if isinstance(opening_element,str):
            opening_element=self.element(opening_element,label='Opening')
        l=[]
        st='./gbxml:PlanarGeometry/gbxml:PolyLoop/gbxml:CartesianPoint'
        cartesian_points=self.xpath(opening_element,st)
        for cartesian_point in cartesian_points:
            st='./gbxml:Coordinate'
            coordinates=self.xpath(cartesian_point,st)
            t=(float(self.text_value(coordinates[0])),
               float(self.text_value(coordinates[1])),
               float(self.text_value(coordinates[2])))
            l.append(t)
        return l
    
# FUNCTIONS - SURFACE
    
    def surface_azimuth(self,surface_element):
        """Returns the azimuth of a surface
        
        Arguments:
            - surface_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - azimuth (float) or None
        
        """
        if isinstance(surface_element,str):
            surface_element=self.element(surface_element,label='Surface')
        l=self.xpath(surface_element,'./gbxml:RectangularGeometry/gbxml:Azimuth')
        if len(l)>0:
            azimuth=l[0]
            return float(self.text_value(azimuth))
    
    
    def surface_coordinates(self,surface_element):
        """Returns a list of coordinate tuples
        
        Arguments:
            - surface_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - coordinates (list): a list where each item is a tuple of (x,y,z) coordinates.
                i.e. [(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),...]
                or None
                
        """
        if isinstance(surface_element,str):
            surface_element=self.element(surface_element,label='Surface')
        l=[]
        st='./gbxml:PlanarGeometry/gbxml:PolyLoop/gbxml:CartesianPoint'
        cartesian_points=self.xpath(surface_element,st)
        for cartesian_point in cartesian_points:
            st='./gbxml:Coordinate'
            coordinates=self.xpath(cartesian_point,st)
            t=(float(self.text_value(coordinates[0])),
               float(self.text_value(coordinates[1])),
               float(self.text_value(coordinates[2])))
            l.append(t)
        return l
    
    
    def surface_inner_space(self,surface_element):
        """Returns the inner Space element of a Surface, or None
        
        Arguments:
            - surface_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - space (lxml._Element) or None
        
        """
        if isinstance(surface_element,str):
            surface_element=self.element(surface_element,label='Surface')
        adjacentSpaceIds=self.child_elements(surface_element,label='AdjacentSpaceId')
        if len(adjacentSpaceIds)>0:
            adjacentSpaceId=adjacentSpaceIds[0]
            spaceIdRef=adjacentSpaceId.get('spaceIdRef')
            return self.element(spaceIdRef)
        
        
    def surface_outer_space(self,surface_element):
        """Returns the outer Space element of a Surface, or None
        
        Arguments:
            - surface_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - space (lxml._Element) or None
        
        """
        if isinstance(surface_element,str):
            surface_element=self.element(surface_element,label='Surface')
        adjacentSpaceIds=self.child_elements(surface_element,label='AdjacentSpaceId')
        if len(adjacentSpaceIds)>1:
            adjacentSpaceId=adjacentSpaceIds[1]
            spaceIdRef=adjacentSpaceId.get('spaceIdRef')
            return self.element(spaceIdRef)
        
        
    def surface_tilt(self,surface_element):
        """Returns the tilt of a surface
        
        Arguments:
            - surface_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - tilt (float) or None
            
        """
        if isinstance(surface_element,str):
            surface_element=self.element(surface_element,label='Surface')
        l=self.xpath(surface_element,'./gbxml:RectangularGeometry/gbxml:Tilt')
        if len(l)>0:
            tilt=l[0]
            return float(self.text_value(tilt))

        
        

## SPACE FUNCTIONS
#        
#    def set_space_id(self,space_element,id):
#        """Sets a new id attribute for a Space element and updates all links
#        
#        
#        """
#        if isinstance(space_element,str):
#            space_element=self.element(space_element)
#        #get old id
#        old_id=space_element.get('id')
#        #set new id
#        space_element.set('id',id)
#        #find all elements with attribute spaceRefId=old_id
#        st='.//gbxml:*[@spaceIdRef="%s"]' % old_id
#        l=self.xpath(self.root(),st)
#        #update with id
#        for e in l:
#            e.set('spaceIdRef',id)
#        #return new id 
#        return id
       
        
# WINDOWTYPE FUNCTIONS
        
    def windowType_materials(self,windowType_element):
        """Returns the Glaze and Gap elements of a windowType in order
        
        Arguments:
            - windowType_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
                
        Return value:
            - glaze_and_gap_elements (list)
        
        """
        l=[]
        if isinstance(windowType_element,str):
            windowType_element=self.element(windowType_element,label='WindowType')
        l=self.child_elements(windowType_element)
        return [x for x in l if self.label(x) in ['Glaze','Gap']]
       
    
# ZONE FUNCTIONS
        
    def add_zone(self,zone_id,space_ids):
        """Adds a zone element and the IdRef links to it.
        
        Arguments:
            - zone_id (str): the id of the new zone
            - space_ids (str or list): the ids of the spaces that link to the zone 
        """
        #adds element
        parent=self.root()
        e=self.add_element(parent,'Zone')
        self.set_attribute(e,'id',zone_id)
        #adds links
        if isinstance(space_ids,str):
            space_ids=[space_ids]
        for space_id in space_ids:
            space=self.element(space_id,'Space')
            self.set_attribute(space,'zoneIdRef',zone_id)
        #returns the new zone element
        return e
    
        
    def remove_zone(self,zone_element):
        """Removes a Zone element and all IdRef links to the zone.
        
        Arguments:
            - zone_element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
        """
        #find id
        if isinstance(zone_element,str):
            id=zone_element
        else:
            id=zone_element.get('id')
        #find all elements with attribute zoneRefId=id
        st='.//gbxml:*[@zoneIdRef="%s"]' % id
        l=self.xpath(self.root(),st)
        #removes all attributes zoneRefId=id
        for x in l:
            self.remove_attribute(x,'zoneIdRef')
        #remove node
        self.remove_element(zone_element)
        
        
        
    
    
    
    
    
    
    
    
    
    
#    def child_node_text(self,id,label='*'):
#        """Returns a dictionary listing any child nodes which have text
#        
#        Return values is {tag:text}
#                
#        """
#        e=self._element(id,label)
#        d={}
#        for e1 in e:
#            if e1.text:
#                label=e1.tag.split('}')[1]
#                d[label]=e1.text
#        return d
#    
#    
#    def child_node_values(self,id,label='*'):
#        """Returns a dictionary listing any child nodes which have text
#        
#        Node text values are converted from strings into their datatype
#            i.e. the text from an 'Area' node is converted into a float
#        
#        Return values is {label:value}
#                
#        """
#        d=self.xml.child_node_text(id=id,label=label)
#        d1={}
#        for k,v in d.items():
#            xml_type=self.xsd.element_type(k)
#            #print(xml_type)
#            if xml_type=='xsd:string':
#                value=v
#            elif xml_type=='xsd:decimal':
#                value=float(v)
#            else:
#                raise Exception(xml_type)
#            d1[k]=value
#        return d1
#
#           
#    
#    def node_attributes(self,id,label='*'):
#        "Returns the attribute dict of node with id 'id'"
#        e=self._element(id,label)
#        return dict(e.attrib)
#    
#    
#    def node_ids(self,label='*'):
#        """Returns the ids of all nodes
#        
#        Arguments:
#            label (str): the node tag to filter on
#            
#        """
#        #filter by label
#        st='//a:%s' % (label)
#        l=self._ElementTree.getroot().xpath(st,namespaces=self.ns)
#        return [x.get('id') for x in l]
#    
#    
#    def parent_object(self,id,label='*'):
#        """Returns the parent of an element
#        
#        Return value is a dictionary {'id':value,'label':value}
#        
#        """
#        e=self._element(id,label)
#        parent=e.getparent()
#        return {'id':self._id(parent),
#                'label':self._label(parent)}
#        
#    
#    
#    
#    
#    def surface_adjacent_objects(self,id):
#        """Returns the objects adjacent to the surface
#        
#        Return value is a 2 item list of dictionaries [{'id':value,'label':value}]
#        
#        """
#        label='Surface'
#        e=self._element(id,label)
#        st='./a:AdjacentSpaceId/@spaceIdRef'
#        l=e.xpath(st,namespaces=self.ns)
#        l=l+[None]*(2-len(l))
#        surfaceType=e.get('surfaceType')
#        d=\
#            {'InteriorWall':None,
#             'ExteriorWall':{'id':'Climate1','label':'Climate'},
#             'Roof':{'id':'Climate1','label':'Climate'},
#             'InteriorFloor':None,
#             'ExposedFloor':{'id':'Climate1','label':'Climate'},
#             'Shade':{'id':'Climate1','label':'Climate'},
#             'UndergroundWall':{'id':'Ground1','label':'Ground'},
#             'UndergroundSlab':{'id':'Ground1','label':'Ground'},
#             'Ceiling':None,
#             'Air':None,
#             'UndergroundCeiling':{'id':'Ground1','label':'Ground'},
#             'RaisedFloor':{'id':'Climate1','label':'Climate'},
#             'SlabOnGrade':{'id':'Ground1','label':'Ground'},
#             'FreestandingColumn':None,
#             'EmbeddedColumn':None
#             }
#        l1=[]
#        for x in l:
#            if not x is None:
#                l1.append({'id':x,'label':'Space'})
#            else:
#                l1.append(d[surfaceType])
#        return l1
#
#
#    def surface_building_ids(self,id):
#        """Returns a list of building ids that the surface belongs to
#        """
#        l=self.surface_adjacent_objects(id)
#        l=[self.parent_object(x['id'])['id'] for x in l if x['label']=='Space']
#        return l
#        
#    
#    

#    def elements(xml, tag='*'):
#        """Returns a list of lxml elements, filtered by tag
#        
#        Arguments:
#            xml (lxml.etree._ElementTree): the gbXML instance
#            tag (str): the tag name, not including the namespace
#    
#        """
#        st='//a:%s' % (tag)
#        #print(st)
#        return xml.getroot().xpath(st,namespaces=ns)
    

