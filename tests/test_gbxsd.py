# -*- coding: utf-8 -*-

import unittest

import config
from bspy import Gbxsd
from datetime import datetime
from lxml import etree
import json

class Test_gbxsd(unittest.TestCase):
        
    def test_gbxsd___init__(self):
        g=Gbxsd(config.xsd)
        check=isinstance(g,Gbxsd)
        self.assertEqual(True,check)
        
# HIDDEN METHODS
        
    def test__node_children_dict(self):
        g=Gbxsd(config.xsd)
        d=g._node_children_dict('')
        with open('node_children_dict.json','w') as f:
            json.dump(d,f,indent=4,sort_keys=True)
            
            
    def test__simpleType(self):
        g=Gbxsd(config.xsd)
        s=g._simpleType('absorptanceUnitEnum')
        check=isinstance(s,etree._Element)
        self.assertEqual(True,check)
        with self.assertRaises(KeyError):
            s=g._simpleType('namedoesnotexist')
            
            
    def test__simpleType_exists(self):
        g=Gbxsd(config.xsd)
        b=g._simpleType_exists('absorptanceUnitEnum')
        self.assertEqual(b,True)
        b=g._simpleType_exists('namedoesnotexist')
        self.assertEqual(b,False)
        
        
# ELEMENT METHODS
    
    def test_element_names(self):
        g=Gbxsd(config.xsd)
        l=g.element_names()
        check=['gbXML', 'aecXML', 'Absorptance', 'AdjacentSpaceId', 'Age', 'AirChangesPerHour']
        self.assertEqual(l[:6],check)
    
    
    def test_element_attributes_exist(self):
        g=Gbxsd(config.xsd)
        b=g.element_attributes_exist('gbXML')
        check=True
        self.assertEqual(b,check)
        b=g.element_attributes_exist('AirChangesPerHour')
        check=False
        self.assertEqual(b,check)
    
    
    def test_element_attributes_properties(self):
        g=Gbxsd(config.xsd)
        l=g.element_attributes_properties('gbXML')
        check=[{'name': 'id', 'type': 'xsd:ID'}, {'name': 'engine'}]
        self.assertEqual(l[:2],check)
    
    
    def test_element_children_exist(self):
        g=Gbxsd(config.xsd)
        b=g.element_children_exist('gbXML')
        check=True
        self.assertEqual(b,check)
        b=g.element_children_exist('Age')
        check=False
        self.assertEqual(b,check)
        
        
    def test_element_children_specification(self):
        g=Gbxsd(config.xsd)
        l=g.element_children_specification('gbXML')
        check=[{'tag': 'choice', 'minOccurs': '0', 'maxOccurs': 'unbounded'}]
        self.assertEqual(l,check)
                
    
    def test_element_children_properties(self):
        g=Gbxsd(config.xsd)
        l=g.element_children_properties('gbXML')
        check=[{'ref': 'aecXML', 'minOccurs': '0'}, {'ref': 'Campus'}]
        self.assertEqual(l[:2],check)
        
    
    
        
# ATTRIBUTE METHODS
        
    def test_attribute_restriction_values(self):
        g=Gbxsd(config.xsd)
        l=g.attribute_restriction_values('Absorptance','type')
        check=['IntIR', 'IntSolar', 'IntVisible', 'IntTotal', 'ExtIR', 'ExtSolar', 'ExtVisible', 'ExtTotal']
        self.assertEqual(l,check)
        l=g.attribute_restriction_values('AdjacentSpaceId','spaceIdRef')
        check=[]
        self.assertEqual(l,check)
        
        
    def test_attribute_restrictions_exist(self):
        g=Gbxsd(config.xsd)
        b=g.attribute_restrictions_exist('Absorptance','type')
        self.assertEqual(b,True)
        b=g.attribute_restrictions_exist('AdjacentSpaceId','spaceIdRef')
        self.assertEqual(b,False)
        
        
    
    
    
#    
#    
#    def test_gbxml_child_node_values(self):
#        #print('TESTING gbxml.child_node_values...')
#        g=Gbxml(config.xml,config.xsd)
#        d=g.child_node_values('DN000000','Space')
#        check={'Name': 'DINING_ROOM', 
#               'Area': 13.1369, 
#               'Volume': 32.84225, 
#               'TypeCode': '0'}
#        self.assertEqual(d,check)
#    
#    
#    def test_gbxml_read(self):
#        #print('TESTING gbxml.__init__...')
#        g=Gbxml(config.xml,config.xsd)
#        b=isinstance(g.xml._ElementTree,etree._ElementTree)
#        self.assertEqual(b,True)
#        c=isinstance(g.xsd._ElementTree,etree._ElementTree)
#        self.assertEqual(c,True)
#        #print(g)
#    
#    
#class Test_gbxml_xml(unittest.TestCase):
#    
#    
#    def test_gbxml_xml__id(self):
#        g=Gbxml(config.xml,config.xsd)
#        e=g.xml._element('DN000000','Space')
#        st=g.xml._id(e)
#        check='DN000000'
#        self.assertEqual(st,check)
#    
#    
#    def test_gbxml_xml_child_node_text(self):
#        #print('TESTING gbxml.xml.child_node_text...')
#        g=Gbxml(config.xml,config.xsd)
#        d=g.xml.child_node_text('DN000000','Space')
#        check={'Name': 'DINING_ROOM', 
#               'Area': '13.136900', 
#               'Volume': '32.842250', 
#               'TypeCode': '0'}
#        self.assertEqual(d,check)
#    
#    
#    def test_gbxml_xml_node_attributes(self):
#        #print('TESTING gbxml.xml.node_attributes...')
#        g=Gbxml(config.xml,config.xsd)
#        d=g.xml.node_attributes('DN000000','Space')
#        check={'id': 'DN000000', 'zoneIdRef': 'ZONE_1', 
#               'conditionType': 'HeatedAndCooled', 
#               'buildingStoreyIdRef': 'GROUP_1'}
#        self.assertEqual(d,check)
#    
#    
#    def test_gbxml_xml_node_ids(self):
#        #print('TESTING gbxml.xml.node_ids...')
#        g=Gbxml(config.xml,config.xsd)
#        l=g.xml.node_ids()
#        self.assertEqual(len(l),3953)
#        l=g.xml.node_ids('Building')
#        check=['ff88c119_9818_4829_a88f_460af894b4c5']
#        self.assertEqual(l,check)
#        
#        
#    def test_gbxml_xml_parent_object(self):
#        #print('TESTING gbxml.xml.node_ids...')
#        g=Gbxml(config.xml,config.xsd)
#        d=g.xml.parent_object('DN000000','Space')
#        check={'id': 'ff88c119_9818_4829_a88f_460af894b4c5', 'label': 'Building'}
#        self.assertEqual(d,check)
#        
#        
#    def test_gbxml_xml_surface_adjacent_objects(self):
#        #print('TESTING gbxml.xml.surface_adjacent_objects...')
#        g=Gbxml(config.xml,config.xsd)
#        l=g.xml.surface_adjacent_objects('surface-1')
#        check=[{'id': 'DN000000', 'label': 'Space'}, {'id': 'Ground1', 'label': 'Ground'}]
#        self.assertEqual(l,check)
#        
#        
#    def test_gbxml_xml_surface_building_ids(self):
#        #print('TESTING gbxml.xml.surface_adjacent_objects...')
#        g=Gbxml(config.xml,config.xsd)
#        l=g.xml.surface_building_ids('surface-1')
#        check=['ff88c119_9818_4829_a88f_460af894b4c5']
#        self.assertEqual(l,check)
#    
#
##class Test_gbxml_to_system(unittest.TestCase):
##         
##    def test_gbxml_to_system(self):
##        print('TESTING gbxml.to_system...')
##        g=Gbxml(config.xml,config.xsd)
##        s=System(r'bolt://localhost:7687','','Gbxml')
##        dt=datetime(2001,1,1).isoformat()
##        s.delete_all()
##        g.to_system(system=s,timestamps=[dt])
##        
##        print('COUNTING NODES AND RELATIONSHIPS...')
##        print('Number of nodes:',s.count_nodes())
##        print('Number of relationships:',s.count_relationships())
##        
#        
        
if __name__=='__main__':
    
    o=unittest.main(Test_gbxsd())
#    o=unittest.main(Test_gbxml_to_system())