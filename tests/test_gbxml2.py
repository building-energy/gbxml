# -*- coding: utf-8 -*-

import unittest
import config
from gbxml import Gbxml
from lxml import etree
from io import StringIO

class Test_gbxml2(unittest.TestCase):

    def test1(self):
        
        g=Gbxml('detached_house.gbxml')
        
        result=g.get_ids()
        
        print(result)
        
        result=g.get_ids(label='Building')
        
        print(result)
        
        result=g.get_xmlstring()
        #print(result)
        
        result=g.get_xmlstring(id='DINING_ROOM')
        print(result)
    
        result=g.get_construction_layers(id="WALL")
        print(result)
    
if __name__=='__main__':
    
    o=unittest.main(Test_gbxml2())    