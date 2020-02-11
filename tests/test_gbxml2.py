# -*- coding: utf-8 -*-

import unittest
from gbxml import Gbxml


class Test_gbxml2(unittest.TestCase):

# general query methods
    
    def test_get_ids(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_ids()
        #print(result)
        answer=['campus-1', 'detached_house', 'GROUP_1', 'DINING_ROOM', 
                'KITCHEN', 'LIVING_ROOM', 'HALL', 'BATHROOM', 'WC', 
                'BEDROOM2', 'BEDROOM1', 'BEDROOM3', 'LANDING', 'ROOF', 
                'surface-1', 'surface-2', 'surface-3', 'surface-4', 
                'surface-5', 'surface-6', 'surface-6-opening-1', 'surface-7', 
                'surface-8', 'surface-9', 'surface-10', 'surface-11', 
                'surface-12', 'surface-13', 'surface-13-opening-1', 
                'surface-14', 'surface-14-opening-1', 'surface-15', 
                'surface-16', 'surface-17', 'surface-18', 'surface-19', 
                'surface-20', 'surface-21', 'surface-22', 'surface-23', 
                'surface-23-opening-1', 'surface-24', 'surface-25', 
                'surface-26', 'surface-27', 'surface-28', 
                'surface-28-opening-1', 'surface-29', 'surface-30', 
                'surface-31', 'surface-31-opening-1', 'surface-32', 
                'surface-33', 'surface-34', 'surface-35', 
                'surface-35-opening-1', 'surface-36', 'surface-37', 
                'surface-38', 'surface-39', 'surface-39-opening-1', 
                'surface-40', 'surface-41', 'surface-42', 'surface-43', 
                'surface-44', 'surface-45', 'surface-46', 'surface-47', 
                'surface-47-opening-1', 'surface-48', 'surface-49', 
                'surface-50', 'surface-51', 'surface-52', 'surface-53', 
                'surface-53-opening-1', 'surface-54', 'surface-55', 
                'surface-56', 'surface-57', 'surface-58', 'surface-59', 
                'surface-59-opening-1', 'surface-60', 'surface-61', 
                'surface-62', 'surface-63', 'surface-64', 'surface-65', 
                'surface-66', 'surface-67', 'CEIL', 'PART', 'STD_DOOR', 
                'STD_FLO1', 'STD_ROOF', 'WALL', 'layer-CEIL', 'layer-PART', 
                'layer-STD_DOOR', 'layer-STD_FLO1', 'layer-STD_ROOF', 
                'layer-WALL', 'BRI-0.105', 'BRO1-0.105', 'Cavity-AIR-0.05', 
                'Cavity-AIR-0.065', 'Cavity-AIR-0.2', 'GPB-0.01', 
                'SCP-0.005', 'STDCBM21-0.037', 'STD_CC1-0.1', 'STD_CC2-0.1', 
                'STD_FBA-0.02', 'STD_MEM-0.0001', 'STD_PH1-0.0982', 
                'STD_PHF-0.1544', 'STD_US5-0.0125', 'STD_US5-0.016', 
                'TMF-0.02', 'STD_EXTW', 'STD_EXTW-layer-1', 'STD_EXTW-layer-2', 
                'STD_EXTW-layer-3', 'IESVE', 'cvskf', 'Zone-DINING_ROOM', 
                'Zone-KITCHEN', 'Zone-LIVING_ROOM', 'Zone-HALL', 
                'Zone-BATHROOM', 'Zone-WC', 'Zone-BEDROOM2', 
                'Zone-BEDROOM1', 'Zone-BEDROOM3', 'Zone-LANDING', 
                'schedule-alwaysOn', 'yearSchedule-alwaysOn', 
                'weekSchedule-alwaysOn', 'daySchedule-alwaysOn', 
                'schedule-heating', 'yearSchedule-heating1', 
                'yearSchedule-heating2', 'yearSchedule-heating3', 
                'weekSchedule-heatingOn', 'weekSchedule-heatingOff', 
                'daySchedule-heatingOn', 'daySchedule-heatingOff']
        self.assertEqual(result,answer)
        
        result=g.get_ids(tag='Building')
        #print(result)
        answer=['detached_house']
        self.assertEqual(result,answer)
        
        
    def test_get_xmlstring(self):
    
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_xmlstring()
        #print(result)
        
        result=g.get_xmlstring(id='DINING_ROOM')
        #print(result)
        
        
    def test_get_attributes(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_attributes(id='DINING_ROOM')
        #print(result)
        answer={'id': 'DINING_ROOM', 
                'conditionType': 'HeatedAndCooled', 
                'buildingStoreyIdRef': 'GROUP_1', 
                'peopleScheduleIdRef': 'schedule-alwaysOn', 
                'lightScheduleIdRef': 'schedule-alwaysOn', 
                'equipmentScheduleIdRef': 'schedule-alwaysOn', 
                'zoneIdRef': 'Zone-DINING_ROOM'}
        self.assertEqual(result,answer)
        
        
    def test_get_child_tags(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_child_tags(id='DINING_ROOM')
        #print(result)
        answer=['Name', 'Area', 'Volume', 'AirChangesPerHour', 'PeopleNumber', 
                'PeopleHeatGain', 'LightPowerPerArea', 'EquipPowerPerArea']
        self.assertEqual(result,answer)
        
        
    def test_get_child_tag_text(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_child_tag_text(id='DINING_ROOM',child_tag='Area')
        #print(result)
        answer=['13.136900']
        self.assertEqual(result,answer)
        
        
    def test_get_child_tag_attributes(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_child_tag_attributes(id='DINING_ROOM',child_tag='PeopleHeatGain')
        #print(result)
        answer=[{'unit': 'WattPerPerson', 'heatGainType': 'Total'}]
        self.assertEqual(result,answer)
        
        
    def test_get_children_list(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_children_list(id='DINING_ROOM')
        #print(result)
        answer=[{'tag': 'Name', 'text': 'DINING_ROOM', 'attributes': {}}, 
                {'tag': 'Area', 'text': '13.136900', 'attributes': {}}, 
                {'tag': 'Volume', 'text': '32.842250', 'attributes': {}}, 
                {'tag': 'AirChangesPerHour', 'text': '0.5', 'attributes': {}}, 
                {'tag': 'PeopleNumber', 'text': '0.2', 'attributes': {'unit': 'NumberOfPeople'}}, 
                {'tag': 'PeopleHeatGain', 'text': '90', 'attributes': {'unit': 'WattPerPerson', 'heatGainType': 'Total'}}, 
                {'tag': 'LightPowerPerArea', 'text': '0.5', 'attributes': {'unit': 'WattPerSquareMeter'}}, 
                {'tag': 'EquipPowerPerArea', 'text': '3', 'attributes': {'unit': 'WattPerSquareMeter'}}]
        self.assertEqual(result,answer)
        
        
        
        
# campus tag querys
        
    def test_get_campus_location_tags(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_campus_location_tags(id='campus-1')
        #print(result)
        answer=['CADModelAzimuth']
        self.assertEqual(result,answer)
        
        
    def test_get_campus_location_tag_text(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_campus_location_tag_text(id='campus-1',
                                              child_tag='CADModelAzimuth')
        #print(result)
        answer=['-0.000000']
        self.assertEqual(result,answer)
        
        
# building query methods
        
    def test_get_building_space_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_building_space_ids(id="detached_house")
        #print(result)
        answer=['DINING_ROOM', 'KITCHEN', 'LIVING_ROOM', 'HALL', 
                'BATHROOM', 'WC', 'BEDROOM2', 'BEDROOM1', 'BEDROOM3', 
                'LANDING', 'ROOF']
        self.assertEqual(result,answer)
        
        
    def test_get_building_surface_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_building_surface_ids(id="detached_house")
        #print(result)
        answer=['surface-8', 'surface-20', 'surface-14', 'surface-38', 
                'surface-47', 'surface-37', 'surface-46', 'surface-44', 
                'surface-60', 'surface-63', 'surface-24', 'surface-4', 
                'surface-19', 'surface-21', 'surface-32', 'surface-58', 
                'surface-31', 'surface-48', 'surface-16', 'surface-51', 
                'surface-53', 'surface-30', 'surface-12', 'surface-2', 
                'surface-39', 'surface-54', 'surface-57', 'surface-7', 
                'surface-52', 'surface-50', 'surface-55', 'surface-65', 
                'surface-61', 'surface-40', 'surface-43', 'surface-35', 
                'surface-9', 'surface-15', 'surface-13', 'surface-41', 
                'surface-33', 'surface-66', 'surface-25', 'surface-42', 
                'surface-59', 'surface-23', 'surface-29', 'surface-56', 
                'surface-1', 'surface-10', 'surface-26', 'surface-64', 
                'surface-67', 'surface-45', 'surface-5', 'surface-22', 
                'surface-17', 'surface-34', 'surface-6', 'surface-11', 
                'surface-49', 'surface-28', 'surface-62', 'surface-36', 
                'surface-27', 'surface-18', 'surface-3']
        self.assertEqual(result,answer)
        
        
# space query methods
        
    def test_get_space_surface_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_space_surface_ids(id="DINING_ROOM")
        #print(result)
        answer=['surface-1', 'surface-8', 'surface-4', 'surface-5', 'surface-6', 'surface-2', 'surface-7', 'surface-3']
        self.assertEqual(result,answer)
    
        
# construction query methods
    
    def test_get_construction_layer_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_construction_layer_ids(id="WALL")
        #print(result)
        answer=['layer-WALL']
        self.assertEqual(result,answer)
        
        
    def test_get_construction_material_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_construction_material_ids(id="WALL")
        #print(result)
        answer=['BRO1-0.105', 'Cavity-AIR-0.065', 'BRI-0.105', 'STD_US5-0.016']
        self.assertEqual(result,answer)
        
        
        
# layer query methods
        
    def test_get_layer_material_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_layer_material_ids(id='layer-WALL')
        #print(result)
        answer=['BRO1-0.105', 'Cavity-AIR-0.065', 'BRI-0.105', 'STD_US5-0.016']
        self.assertEqual(result,answer)
        
    
    
# surface query methods
        
    def test_get_surface_inner_space_id(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_inner_space_id(id='surface-6')
        #print(result)
        answer='DINING_ROOM'
        self.assertEqual(result,answer)
        
        
    def test_get_surface_outer_space_id(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_outer_space_id(id='surface-5')
        #print(result)
        answer='KITCHEN'
        self.assertEqual(result,answer)
        
        result=g.get_surface_outer_space_id(id='surface-6')
        #print(result)
        answer=None
        self.assertEqual(result,answer)
        
        
    def test_get_surface_azimuth(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_azimuth(id='surface-6')
        #print(result)
        answer=0
        self.assertEqual(result,answer)
        
        
    def test_get_surface_tilt(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_tilt(id='surface-6')
        #print(result)
        answer=90
        self.assertEqual(result,answer)
        
        
    def test_get_surface_coordinates(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_coordinates(id='surface-6')
        #print(result)
        answer=[(1.1125, 8.979, 2.735), 
                (4.902, 8.979, 2.735), 
                (4.902, 8.979, 0.0), 
                (1.1125, 8.979, 0.0)]
        self.assertEqual(result,answer)
        
        
    def test_get_surface_area(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_area(id='surface-6')
        #print(result)
        answer=10.3642825
        self.assertEqual(result,answer)
        
        
    def test_get_surface_opening_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_surface_opening_ids(id='surface-6')
        #print(result)
        answer=['surface-6-opening-1']
        self.assertEqual(result,answer)
    
    
# opening query methods
    
    def test_get_opening_surface_id(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_opening_surface_id(id='surface-6-opening-1')
        #print(result)
        answer='surface-6'
        self.assertEqual(result,answer)
        
        
    def test_get_opening_coordinates(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_opening_coordinates(id='surface-6-opening-1')
        #print(result)
        answer=[(2.122, 8.979, 2.15), (3.922, 8.979, 2.15), (3.922, 8.979, 0.05), (2.122, 8.979, 0.05)]
        self.assertEqual(result,answer)
        
        
    def test_get_opening_area(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_opening_area(id='surface-6-opening-1')
        #print(result)
        answer=3.7800000000000007
        self.assertEqual(result,answer)
    
    
# zone query methods
        
    def test_get_zone_space_ids(self):
        
        g=Gbxml('detached_house.gbxml')
    
        result=g.get_zone_space_ids(id='Zone-DINING_ROOM')
        #print(result)
        answer=['DINING_ROOM']
        self.assertEqual(result,answer)
    
    
if __name__=='__main__':
    
    o=unittest.main(Test_gbxml2())    
    
    
    
    
    
    
    
    
    
    
    