# -*- coding: utf-8 -*-

import unittest
import config
from gbxml import Gbxml, Gbxsd
from lxml import etree
from io import StringIO

class Test_gbxml(unittest.TestCase):

# OBJECT CREATION
    
    def test_gbxml___init__(self):
        g=Gbxml(config.xml,config.xsd)
        b=isinstance(g,Gbxml)
        self.assertEqual(b,True)
        b=isinstance(g.gbxsd,Gbxsd)
        self.assertEqual(b,True)
        g=Gbxml(xsd_fp=config.xsd)
        b=isinstance(g,Gbxml)
        self.assertEqual(b,True)
        g=Gbxml()
        b=isinstance(g,Gbxml)
        self.assertEqual(b,True)


#OUTPUT
     
    def test_gbxml_xmlstring(self):
        g=Gbxml(config.xml,config.xsd)
        st=g.xmlstring()
        check="""<ns0:gbXML xmlns:ns0="http://www.gbxml.org/schema" temperatureUnit="C" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true" version="0.37">"""
        self.assertEqual(st[:len(check)],check)
                
        
    def test_gbxml_xpath(self):
        g=Gbxml(config.xml,config.xsd)
        st='/gbxml:gbXML'
        l=g.xpath(g.root(),st)
        n=len(l)
        check=1
        self.assertEqual(n,check)
        
        
#    def test_gbxml_write(self):
#        g=Gbxml(config.xml,config.xsd)
#        g.write('test_gbxml_write.xml')

# VALIDATION
    
    def test_gbxml_validate(self):
        g=Gbxml(config.xml,config.xsd)
        b=g.validate()
        check=False #actually the new gbxml file doesn't validate...
        self.assertEqual(b,check)
        g._ElementTree=etree.parse(StringIO('<a><c></c></a>'))
        b=g.validate()
        check=False
        self.assertEqual(b,check)
        
        
# EDITING
        
    def test_gbxml_add_element(self):
        g=Gbxml()
        g.add_element(g.root(),'Campus')
        n=len(g.elements())
        check=2
        self.assertEqual(n,check)
        
        
    def test_gbxml_set_attribute(self):
        g=Gbxml()
        e=g.root()
        e=g.set_attribute(e,'temperatureUnit','K')
        st=e.get('temperatureUnit')
        check='K'
        self.assertEqual(st,check)
        
        
    def test_gbxml_set_text(self):
        g=Gbxml()
        e=g.add_element(g.root(),'Campus')
        e=g.add_element(e,'Name')
        e=g.set_text(e,'MyCampus')
        st=e.text
        check='MyCampus'
        self.assertEqual(st,check)
    
    
    def test_gbxml_remove_element(self):
        g=Gbxml(config.xml,config.xsd)
        g.remove_element('campus-1')
        l=g.elements('Campus')
        check=[]
        self.assertEqual(l,check)
        
    
    def test_gbxml_remove_attribute(self):
        g=Gbxml()
        e=g.root()
        g.remove_attribute(e,'temperatureUnit')
        d=g.attributes(e)
        check={'lengthUnit': 'Meters', 'areaUnit': 'SquareMeters', 'volumeUnit': 'CubicMeters', 'useSIUnitsForResults': 'true', 'version': '0.37'}
        self.assertEqual(d,check)
    
    
         
# QUERYING
        
    def test_gbxml_elements(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.elements()
        n=len(l)
        check=2707
        self.assertEqual(n,check)
        
    
    def test_gbxml_root(self):
        g=Gbxml()
        e=g.root()
        st=g.label(e)
        check='gbXML'
        self.assertEqual(st,check)
        
        
    def test_gbxml_element(self):
        g=Gbxml(config.xml,config.xsd)
        e=g.element(id='campus-1')
        st=g.label(e)
        check='Campus'
        self.assertEqual(st,check)
        
          
    def test_gbxml_label(self):
        g=Gbxml()
        e=g.root()
        st=g.label(e)
        check='gbXML'
        self.assertEqual(st,check)
        
        
    def test_gbxml_attributes(self):
        g=Gbxml()
        e=g.root()
        d=g.attributes(e)
        check={'temperatureUnit': 'C', 'lengthUnit': 'Meters', 'areaUnit': 'SquareMeters', 'volumeUnit': 'CubicMeters', 'useSIUnitsForResults': 'true', 'version': '0.37'}
        self.assertEqual(d,check)
        
        
    def test_gbxml_text(self):
        g=Gbxml(config.xml,config.xsd)
        e=g.elements(label='Name')[0]
        st=g.text(e)
        check='detached_house'
        self.assertEqual(st,check)
        
        
    def test_gbxml_child_elements(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.child_elements(g.root(),label='Campus')
        st=g.label(l[0])
        check='Campus'
        self.assertEqual(st,check)
        
        
    def test_gbxml_descendent_elements(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.descendent_elements(g.root(),label='Building')
        st=g.label(l[0])
        check='Building'
        self.assertEqual(st,check)
    
    
# CONSTRUCTION FUNCTIONS
        
    def test_gbxml_construction_layers(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.construction_layers('CEIL')
        layer_ids=[x.get('id') for x in l]
        check=['layer-CEIL']
        self.assertEqual(layer_ids,check)
        
        
    def test_gbxml_construction_materials(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.construction_materials('CEIL')
        material_ids=[x.get('id') for x in l]
        check=['SCP-0.005', 'TMF-0.02', 'Cavity-AIR-0.2', 'GPB-0.01']
        self.assertEqual(material_ids,check)
        
        

# LAYER FUNCTIONS
        
    def test_gbxml_layer_materials(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.layer_materials('layer-CEIL')
        material_ids=[x.get('id') for x in l]
        check=['SCP-0.005', 'TMF-0.02', 'Cavity-AIR-0.2', 'GPB-0.01']
        self.assertEqual(material_ids,check)
    
        
# OPENING FUNCTIONS
        
    def test_gbxml_opening_coordinates(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.opening_coordinates('surface-6-opening-1')
        check=[(2.122, 8.979, 2.15), (3.922, 8.979, 2.15), (3.922, 8.979, 0.05), (2.122, 8.979, 0.05)]
        self.assertEqual(l,check)

# SURFACE FUNCTIONS
        
    def test_gbxml_surface_azimuth(self):
        g=Gbxml(config.xml,config.xsd)
        st=g.surface_azimuth('surface-1')
        check=0
        self.assertEqual(st,check)
        
    def test_gbxml_surface_coordinates(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.surface_coordinates('surface-1')
        check=[(1.1125, 4.7895, 0.0), (1.1125, 8.979, 0.0), (4.902, 8.979, 0.0), (4.902, 4.7895, 0.0)]
        self.assertEqual(l,check)
        
    def test_gbxml_surface_inner_space(self):
        g=Gbxml(config.xml,config.xsd)
        space=g.surface_inner_space('surface-1')
        st=space.get('id')
        check='DINING_ROOM'
        self.assertEqual(st,check)
        
    def test_gbxml_surface_outer_space(self):
        g=Gbxml(config.xml,config.xsd)
        #None condition
        space=g.surface_outer_space('surface-1')
        check=None
        self.assertEqual(space,check)
        #
        space=g.surface_outer_space('surface-2')
        st=space.get('id')
        check='LANDING'
        self.assertEqual(st,check)
        
    def test_gbxml_surface_tilt(self):
        g=Gbxml(config.xml,config.xsd)
        st=g.surface_tilt('surface-1')
        check=180
        self.assertEqual(st,check)
    
    def test_gbxml_surface_construction(self):
        g=Gbxml(config.xml,config.xsd)
        e=g.surface_construction('surface-1')
        check='STD_FLO1'
        self.assertEqual(e.get('id'),check)
    
    def test_gbxml_surface_layers(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.surface_layers('surface-1')
        layer_ids=[x.get('id') for x in l]
        check=['layer-STD_FLO1']
        self.assertEqual(layer_ids,check)
        
    def test_gbxml_surface_materials(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.surface_materials('surface-1')
        material_ids=[x.get('id') for x in l]
        check=['STD_PH1-0.0982','STD_CC2-0.1','Cavity-AIR-0.05','STD_FBA-0.02']
        self.assertEqual(material_ids,check)
    
    
# FUNCTIONS - WINDOWTYPE
        
    def test_gbxml_windowType_materials(self):
        g=Gbxml(config.xml,config.xsd)
        l=g.windowType_materials('STD_EXTW')
        ids=[x.get('id') for x in l]
        check=['STD_EXTW-layer-1', 'STD_EXTW-layer-2', 'STD_EXTW-layer-3']
        self.assertEqual(ids,check)
        
    
# ZONE FUNCTIONS
    
    def test_gbxml_add_zone(self):
        g=Gbxml()
        campus=g.add_element(g.root(),'Campus')
        building=g.add_element(campus,'Building')
        space=g.add_element(building,'Space')
        space.set('id','space-1')
        g.add_zone('zone-1','space-1')
        l=g.elements('Zone')
        check=1
        self.assertEqual(len(l),check)
        st=space.get('zoneIdRef')
        check='zone-1'
        self.assertEqual(st,check)
        
    
    def test_gbxml_remove_zone(self):
        g=Gbxml(config.xml,config.xsd)
        g.remove_zone('Zone-DINING_ROOM')
        l=g.elements('Zone')
        check=9
        self.assertEqual(len(l),check)
        space=g.element('DINING_ROOM')[0]
        check=None
        self.assertEqual(space.get('zoneIdRef'),check)
        
        
        
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
    
    o=unittest.main(Test_gbxml())    
#    o=unittest.main(Test_gbxml_xml())
#    o=unittest.main(Test_gbxml_to_system())