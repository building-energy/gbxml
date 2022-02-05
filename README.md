# gbxml
A Python package for reading, writing and editing [gbXML](https://www.gbxml.org/) files

Any problems? [Please raise an Issue on GitHub](https://github.com/building-energy/gbxml/issues)

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

[lxml](https://lxml.de/) is used as the parser to read the gbXML file. 

As the gbXML file is read in, three properties are populated:

```python
g._ElementTree # an lxml _ElementTree instance of the gbXML file
g._ElementTree_gbxsd # an lxml _ElementTree instance of the gbXML schema file
g.ns # the gbXML namespace as a dictionary {'gbxml':'http://www.gbxml.org/schema'}
```

### Query Methods

The gbXML file contents can be queried using the methods below. See the [Querying_a_gbxml_file.ipynb](https://nbviewer.jupyter.org/github/building-energy/gbxml/blob/master/demo/Querying_a_gbxml_file.ipynb) Jupyter Notebook in the 'demo' section for more details on these methods.

If a query is needed which is not possible using the methods below, then this can be done using the [lxml xpath](https://lxml.de/xpathxslt.html) method on the `g._ElementTree` attribute. See the [source code](https://github.com/building-energy/gbxml/blob/master/gbxml/gbxml.py) of the methods below for inspiration on how to do this.

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
g.get_campus_location_tags ( id ) # returns the location child tags of a campus
g.get_campus_location_tag_text ( id , child_tag ) # returns the text of location child elements of a campus
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

### Editing methods

To do



### Writing methods

To do



### Saving a gbXML file





