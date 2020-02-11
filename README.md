# gbxml
A Python package for reading, writing and editing gbXML files

Any problems? [Please raise an Issue on GitHub](https://github.com/building-energy/gbxml/issues)

## To install

```
pip install gbxml
```

## Quick demo

The following code reads a gbXML file and prints the ids of all 'Building' nodes:

```python
from gbxml import Gbxml
g = Gbxml( 'detached_house.gbxml' )
building_ids = g.get_ids( tag = 'Building' ) 
print( building_ids )
```
This outputs:
```python
['Building01']
```

## User guide

### Importing the Gbxml class:

```python
from gbxml import Gbxml
```

### Creating an instance of Gbxml and reading in a gbXML file:

```python
g = Gbxml( 'detached_house.gbxml' )
```

lxml is used as the parser to read the gbXML file. 

As the gbXML file is read in, three properties are populated:

```python
g._ElementTree # an lxml _ElementTree instance of the gbXML file
g._ElementTree_gbxsd # an lxml _ElementTree instance of the gbXML schema file
g.ns # the gbXML namespace as a dictionary {'gbxml':'http://www.gbxml.org/schema'}
```

### Query Methods

General query methods:

```python
g.get_ids ( tag = None ) # returns the id attributes of the elements
g.get_xmlstring ( id = None ) # returns a string of an element
g.get_attributes ( id ) # returns the attributes of an element
g.get_child_tags ( id ) # returns the child tags of an element
g.get_child_tag_text ( id , child_tag ) # returns the text of child elements
g.get_child_tag_attributes ( id , child_tag ) # returns the attributes of child elements
g.get_children_list ( id ) # returns a list of dicts representing each child element
```

Campus query methods:

```python
g.get_campus_location_child_tags ( id ) # returns the location child tags of a campus
g.get_campus_location_child_tag_text ( id , child_tag ) # returns the text of location child elements of a campus
```

Building query methods:

```python
g.get_building_space_ids ( id ) # returns the ids of spaces in a building
g.get_building_surface_ids (id ) # returns the ids of surfaces in a building
```

Space query methods:

```python
g.get_space_surface_ids ( id ) # returns the ids of surfaces adjacent to a space
```

Construction query methods:

```python
g.get_construction_layer_ids ( id ) # returns the layer ids of a construction
g.get_construction_material_ids ( id ) # returns the material ids of a construction
```

Layer query methods:

```python
g.get_layer_material_ids ( id ) # returns the material ids of a layer
```

Surface query methods:

```python
g.get_surface_inner_space_id ( id ) # returns the inner space id of a surface
g.get_surface_outer_space_id ( id ) # returns the outer space id of a surface
g.get_surface_azimuth ( id ) # returns the azimuth angle of a surface
g.get_surface_tilt ( id ) # returns the tilt angle of a surface
g.get_surface_coordinates ( id ) # returns the coordinates of the vertices of a surface
g.get_surface_area ( id ) # returns the area of a surface
g.get_surface_opening_ids ( id ) # returns the ids of the openings in a surface
```

Opening query methods:

```python
g.get_opening_surface_id ( id ) # returns the id of a parent surface of an opening
g.get_opening_coordinates ( id ) # returns the coordinates of the vertices of an opening
g.get_opening_area ( id ) # returns the area of an opening
```

Zone query methods:

```python
g.get_zone_space_ids ( id ) # return the space ids of a zone
```















get_ids ( label=None )





xmlstring

xpath

write

validate

add_element

set_attribute

set_element_id

set_text

remove_element

remove_attribute

remove_text

elements

root

element

label

attributes

text

child_element

descendent_elements

construction_layers

construction_materials

layer_materials

opening_coordinates

surface_azimuth

surface_coordinates

surface_inner_space

surface_outer_space

surface_construction

surface_layers

surface_materials

windowType_materials

add_zone

remove_zone

---

xpath

get_child

get_child_text

get_children

get_descendents

get_element

construction_layers

construction_materials

get_layer

layer_materials

get_material

get_surface_coordinates

get_surface_inner_space

get_surface_outer_space





or background and information on gbXML files, see https://www.gbxml.org/index.html

## Status

First version complete, still further development to be done.

## Quick start

This package contains classes for gbXML files.

Typical use includes:

- reading and querying a gbXML file
- modifying a gbXML file and saving the changes

A quick example of use is:

```python
>>> from bspy import Gbxml
>>> g=Gbxml('input_file.xml','schema_file.xml')
>>> print(g.node_ids(label='Building'))
['Building01']
```



# The Gbxml class

## Introduction

The Gbxml Class is a class object for working with gbXML data. It represents
a gbXML file and the gbXML schema file, and can be used for creating, quering 
and editing gbXML files.

### Instance Creation

> \_\_init\_\_(xml_fp=None,xsd_fp=None)
>
> - Initialises a new Gbxml instance

| Argument | Type   | Description                                                  | Default                                                      |
| -------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| xml_fp   | string | Filepath to a gbXML file. This is read in as an lxml._ElementTree object. | A default gbXML file with a root element only is used. The file is named 'blank.xml' and is in the gbxml subpackage directory. |
| xsd_fp   | string | Filepath to a gbXML schema file.                             | A default gbXML schema file is used. This file is in the gbxml subpackage directory. |

| Return value                             |
| ---------------------------------------- |
| A bspy.gbxml.gbxml.Gbxml instance object |

This example shows the instance creation from an existing gbXML file:

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> print(g)
<bspy.gbxml.gbxml.Gbxml object at 0x0000018DF4B05EF0>
```

This shows how to create a new or default Gbxml instance:

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> print(g)
<bspy.gbxml.gbxml.Gbxml object at 0x0000018DF4B67860>
```

### Instance Properties

A `Gbxml` instance has the following properties:

| Name         | Type                    | Description                                                  |
| ------------ | ----------------------- | ------------------------------------------------------------ |
| _ElementTree | lxml.etree._ElementTree | The imported or default gbXML file                           |
| ns           | string                  | A dictionary with the gbXML namespace mapping: {'gbxml':'http://www.gbxml.org/schema'} |
| gbxsd        | bspy.gbxml.gbxsd.Gbxsd  | A Gbxsd instance of the gbXML schema file, or None           |

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> print(g._ElementTree)
<lxml.etree._ElementTree object at 0x0000018DF4B019C8>
>>> print(g.ns)
{'a': 'http://www.gbxml.org/schema'}
>>> print(g.gbxsd)
<bspy.gbxml.gbxsd.Gbxsd object at 0x0000018DF4B3D668>
```

## Output

### xmlstring

> xmlstring(e=None)
>
> - Returns a string of a gbXML element and its children

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| e | lxml.etree._Element | A gbXML element | The root element

| Return value |
| ------------ |
| string       |

The example below prints the first 200 characters of the string created from 
the 'detached_house.xml' file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> print(g.xmlstring()[0:200])    
<gbXML xmlns="http://www.gbxml.org/schema" temperatureUnit="C" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true" version="0.37">
  <Campus id="campus-1">        
```

### xpath

> xpath(element,st_xpath)
>
> - Returns the result of an xpath operation on the gbXML file

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| element | lxml.etree._Element | A gbXML element | N/A
| st_xpath | string | The xpath string | N/A

| Return value                            |
| --------------------------------------- |
| List, the result of the xpath operation |

This example finds all elements in the gbXML file with the label 'gbXML'.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> st='/gbxml:gbXML'
>>> l=g.xpath(g.root(),st)
>>> print(l)
[<Element {http://www.gbxml.org/schema}gbXML at 0x1af31cdd588>]
```

### write

> write(fp)
>
> - Writes the gbXML file to disk

| Argument | Type   | Description              | Default |
| -------- | ------ | ------------------------ | ------- |
| fp       | string | The filepath to write to | -       |

| Return value |
| ------------ |
| None         |

This example opens the 'detached_house.xml' file and then saves the file using
the name 'test_gbxml_write.xml'.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> g.write('test_gbxml_write.xml')
```

## Validation

### validate

> validate()
>
> - Validates the gbXMl file using the schema

| Return value                                     |
| ------------------------------------------------ |
| True if the gbXML file is valid, otherwise False |

This example checks that the 'detached_house.xml' file is valid according to 
the 'GreenBuildingXML_Ver6.01.xsd' schema.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> print(g.validate())
True
```

## Editing

### add_element

> add_element(parent_element,label)
>
> - Adds an element to the gbXML

| Argument       | Type                          | Description                                                  | Default |
| -------------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| parent_element | lxml.etree._Element or string | The parent element that the new element is added to. This can be either a lxml._Element object or a string with the element id. | N/A     |
| label          | string                        | the label or tag of the new element                          | N/A     |

| Return value                               |
| ------------------------------------------ |
| The newly-added lxml.etree._Element object |

This example adds a 'Campus' element to a 'gbXML' element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.add_element(g.root(),'Campus')
>>> print(g.xmlstring())
<gbXML xmlns="http://www.gbxml.org/schema" temperatureUnit="C" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true" version="0.37">
  <Campus/>
</gbXML>
>>> print(e)
<Element {http://www.gbxml.org/schema}Campus at 0x1af31cecc88>
```

### set_attribute

> set_attribute(element,key,value)
>
> - Sets the attribute of an element

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |
| key      | string                        | The name of the attribute                                    | N/A     |
| value    | string                        | The value of the attribute                                   | N/A     |


| Return value                            |
| --------------------------------------- |
| The modified lxml.etree._Element object |

This example changes the 'temperatureUnit' attribute of the 'gbXML' element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.root()
>>> g.set_attribute(e,'temperatureUnit','K')
>>> print(g.xmlstring())
<gbXML xmlns="http://www.gbxml.org/schema" temperatureUnit="K" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true" version="0.37"/>
```

### set_text

> set_text(element,text)
>
> - Sets the text of an element

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |
| text     | string                        | The text                                                     | N/A     |

| Return value                            |
| --------------------------------------- |
| The modified lxml.etree._Element object |

This example adds a 'Campus' element, then a 'Name' element and sets the text
value of the 'Name' element to 'MyCampus'.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.add_element(g.root(),'Campus')
>>> e=g.add_element(e,'Name')
>>> g.set_text(e,'MyCampus')
>>> print(g.xmlstring())
<gbXML xmlns="http://www.gbxml.org/schema" temperatureUnit="C" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true" version="0.37">
  <Campus>
    <Name>MyCampus</Name>
  </Campus>
</gbXML>
```

### remove_element

> remove_element(element)
>
> - Removes an element

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |

| Return value |
| ------------ |
| None         |

This example removes the 'Campus' element from the gbXML file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> g.remove_element('campus-1')
>>> print(g.elements('Campus'))
[]
```

### remove_attribute

> remove_attribute(element,key)
>
> - Removes an attribute

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |
| key      | string                        | The name of the attribute                                    | N/A     |

| Return value |
| ------------ |
| None         |

This example removes the 'temperatureUnit' attribute from the 'gbXML' element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.root()
>>> g.remove_attribute(e,'temperatureUnit')
>>> print(g.attributes(e))
{'lengthUnit': 'Meters', 'areaUnit': 'SquareMeters', 'volumeUnit': 'CubicMeters', 'useSIUnitsForResults': 'true', 'version': '0.37'}
```

## Querying

### elements

> elements(label='*')
>
> - Returns the elements of the gbXML file

| Argument | Type   | Description                     | Default                     |
| -------- | ------ | ------------------------------- | --------------------------- |
| id       | string | The element id.                 | N/A                         |
| label    | string | The element label to filter on. | No label filter is applied. |

| Return value                          |
| ------------------------------------- |
| A list of lxml.etree._Element objects |

This example prints the first 5 elements in the gbXML file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> l=g.elements()
>>> print(l[0:5])
[<Element {http://www.gbxml.org/schema}gbXML at 0x1af31cff3c8>, 
 <Element {http://www.gbxml.org/schema}Campus at 0x1af31cff408>, 
 <Element {http://www.gbxml.org/schema}Name at 0x1af31cff348>, 
 <Element {http://www.gbxml.org/schema}Location at 0x1af31cff388>, 
 <Element {http://www.gbxml.org/schema}ZipcodeOrPostalCode at 0x1af31cff448>]
```

### root

> root()
>
> - Returns the root element of the gbXML file

| Return value                 |
| ---------------------------- |
| A lxml.etree._Element object |

This example finds the root element of the gbXML file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.root()
>>> print(e)
<Element {http://www.gbxml.org/schema}gbXML at 0x1bab25f3508>
```

### element

> element(id,label='*')
>
> - Returns an element from the gbXML file

| Argument | Type   | Description        | Default                     |
| -------- | ------ | ------------------ | --------------------------- |
| id       | string | The element id.    | N/A                         |
| label    | string | The element label. | No label filter is applied. |

| Return value                 |
| ---------------------------- |
| A lxml.etree._Element object |

This example finds the 'Campus' element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> e=g.element(id='campus-1')
>>> print(e)
<Element {http://www.gbxml.org/schema}Campus at 0x1bab15a0948>
```

### label

> label(element)
>
> - Returns the label of an element

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |

| Return value                  |
| ----------------------------- |
| A string of the element label |

This example prints the label of the 'gbXML' element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.root()
>>> print(g.label(e))
gbXML
```


### attributes

> attributes(element)
>
> - Returns the attributes of an element

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |

| Return value                           |
| -------------------------------------- |
| A dictionary of the element attributes |

This example prints the attributes of the 'gbXML' element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> e=g.elements(label='Name')[0]
>>> print(g.text(e))
detached_house
```

### text

> text(element)
>
> - Returns the text of an element

| Argument | Type                          | Description                                                  | Default |
| -------- | ----------------------------- | ------------------------------------------------------------ | ------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |

| Return value |
| ------------ |
| String       |

This example prints the text of the first 'Name' element in the gbXML file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> e=g.root()
>>> print(g.attributes(e))
{'temperatureUnit': 'C', 'lengthUnit': 'Meters', 'areaUnit': 'SquareMeters', 'volumeUnit': 'CubicMeters', 'useSIUnitsForResults': 'true', 'version': '0.37'}
```


### child_elements

> child_elements(element,label='*')
>
> - Returns the child elements of an element

| Argument | Type                          | Description                                                  | Default                     |
| -------- | ----------------------------- | ------------------------------------------------------------ | --------------------------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A                         |
| label    | string                        | The element label.                                           | No label filter is applied. |

| Return value                          |
| ------------------------------------- |
| A list of lxml.etree._Element objects |

This example finds all 'Campus' child elements of the 'gbXML' root element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> e=g.root()
>>> print(g.child_elements(e,label='Campus'))
[<Element {http://www.gbxml.org/schema}Campus at 0x1c26908f6c8>]
```

### descendent_elements

> descendent_elements(element,label='*')
>
> - Returns the descendent elements of an element

| Argument | Type                          | Description                                                  | Default                     |
| -------- | ----------------------------- | ------------------------------------------------------------ | --------------------------- |
| element  | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A                         |
| label    | string                        | The element label.                                           | No label filter is applied. |

| Return value                          |
| ------------------------------------- |
| A list of lxml.etree._Element objects |

This example finds all 'Building' descendent elements of the 'gbXML' root element.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> e=g.root()
>>> print(g.descendent_elements(e,label='Building'))
[<Element {http://www.gbxml.org/schema}Building at 0x1c26a0a04c8>]
```

## Zone Functions

### add_zone

> add_zone(zone_id,space_ids)
>
> - Adds a zone element and the IdRef links to it 

| Argument  | Type           | Description                                  | Default |
| --------- | -------------- | -------------------------------------------- | ------- |
| zone_id   | string         | The id of the new zone.                      | N/A     |
| space_ids | list or string | The ids of the spaces that link to the zone. | N/A     |

| Return value                                    |
| ----------------------------------------------- |
| A lxml.etree._Element of the newly created zone |

This example adds a Zone element to a gbXML file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml()
>>> campus=g.add_element(g.root(),'Campus')
>>> building=g.add_element(campus,'Building')
>>> space=g.add_element(building,'Space')
>>> space.set('id','space-1')
>>> g.add_zone('zone-1','space-1')
>>> print(g.xmlstring())
<gbXML xmlns="http://www.gbxml.org/schema" temperatureUnit="C" lengthUnit="Meters" areaUnit="SquareMeters" volumeUnit="CubicMeters" useSIUnitsForResults="true" version="0.37">
  <Campus>
    <Building>
      <Space id="space-1" zoneIdRef="zone-1"/>
    </Building>
  </Campus>
  <Zone id="zone-1"/>
</gbXML>
```


### remove_zone

> remove_zone(zone_element)
>
> - Removes a Zone element and all references to it 

| Argument     | Type                          | Description                                                  | Default |
| ------------ | ----------------------------- | ------------------------------------------------------------ | ------- |
| zone_element | lxml.etree._Element or string | This is a lxml.etree._Element object or a string with the element id. | N/A     |

| Return value |
| ------------ |
| None         |

This example removes Zone element 'ZONE_1' from the gbXML file.

```python
>>> from bspy import Gbxml
>>> g=Gbxml(xml_fp='detached_house.xml',
            xsd_fp='GreenBuildingXML_Ver6.01.xsd')
>>> g.remove_zone('ZONE_1')
>>> print(g.elements('Zone'))
[]
>>> print(g.attributes(g.elements('Space')[0]))
{'id': 'DN000000', 'conditionType': 'HeatedAndCooled', 'buildingStoreyIdRef': 'GROUP_1'}
```



# The Gbxsd class

## Instance Creation

```python
>>> from bspy import Gbxsd
>>> g=Gbxsd('GreenBuildingXML_Ver6.01.xsd')
>>> print(g)
<bspy.gbxml.gbxsd.Gbxsd object at 0x0000021AE02ABEB8>
```

## Properties

### _ElementTree & ns

```python
>>> from bspy import Gbxsd
>>> g=Gbxsd('GreenBuildingXML_Ver6.01.xsd')
>>> print(g._ElementTree)
<lxml.etree._ElementTree object at 0x0000021AE0281188>
>>> print(g.ns)
{'a': 'http://www.w3.org/2001/XMLSchema'}
```

## Element Methods

These are methods for the `<xsd:schema>/<xsd:element>` nodes.

### element_names

> element_names()
>
> - returns a list of all element names

| Return value    |
| --------------- |
| List of strings |

This examples prints the first 6 names in the schema file:

```python
>>> from bspy import Gbxsd
>>> g=Gbxsd('GreenBuildingXML_Ver6.01.xsd')
>>> l=g.element_names()
>>> print(l[:6])
['gbXML', 'aecXML', 'Absorptance', 'AdjacentSpaceId', 'Age', 'AirChangesPerHour']
```

### element_attributes_exist

### element_attributes_properties

### element_children_exist

> element_children_exist(name)
>
> - returns True if the element can contain child elements, otherwise False

| Argument | Type   | Description             |
| -------- | ------ | ----------------------- |
| name     | string | the name of the element |

| Return value         |
| -------------------- |
| boolean (True/False) |

This example checks to see if the elements 'gbXML' and 'Age' can contain child elements:

```python
>>> g=Gbxsd('GreenBuildingXML_Ver6.01.xsd')
>>> print(g.element_children_exist('gbXML'))
True
>>> print(g.element_children_exist('Age'))
False
```

### element_children_specification

### element_children_properties

> element_children_properties(name)
>
> - returns a list with the child properties

| Argument | Type   | Description             |
| -------- | ------ | ----------------------- |
| name     | string | the name of the element |

| Return value                                                 |
| ------------------------------------------------------------ |
| a list of dictionaries, where each dictionary holds the attributes of the child `<xsd:element>` node |

This example returns the child element properties of the first two chile elements of the 'gbXML' element:

```python
>>> g=Gbxsd('GreenBuildingXML_Ver6.01.xsd')
>>> print(g.element_children_properties('gbXML')[:2])
[{'ref': 'aecXML', 'minOccurs': '0'}, {'ref': 'Campus'}]
```

## Attribute Methods

### attribute_restrictions_exist

### attribute_restriction_values