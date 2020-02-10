# -*- coding: utf-8 -*-

ns={'gbxml':'http://www.gbxml.org/schema'}


def get_inner_space_id(element):
    "Returns the inner Space id"
    
    st='./gbxml:AdjacentSpaceId/@spaceIdRef'
    result = element.xpath(st,namespaces=ns)
    if len(result)==0:
        return None
    else:
        return result[0]
    

def get_outer_space_id(element):
    "Returns the outer Space id"
    
    st='./gbxml:AdjacentSpaceId/@spaceIdRef'
    result = element.xpath(st,namespaces=ns)
    if len(result)==2:
        return result[1]    
    else:
        return None 
    
    
def get_azimuth(element):
    "Returns the azimuth value"
    
    st='./gbxml:RectangularGeometry/gbxml:Azimuth/text()'
    result = element.xpath(st,namespaces=ns)
    if len(result)>0:
        return float(result[0])
    else:
        return None
    
    
def get_tilt(element):
    "Returns the tilt value"
    
    st='./gbxml:RectangularGeometry/gbxml:Tilt/text()'
    result = element.xpath(st,namespaces=ns)
    if len(result)>0:
        return float(result[0])
    else:
        return None
    
    
def get_coordinates(element):
    "Returns the coordinates"
    
    result=[]
    st='./gbxml:PlanarGeometry/gbxml:PolyLoop/gbxml:CartesianPoint'
    cartesian_point_elements=element.xpath(st,namespaces=ns)
    for cartesian_point_element in cartesian_point_elements:
        st='./gbxml:Coordinate/text()'
        result2=cartesian_point_element.xpath(st,namespaces=ns)
        result2=[float(x) for x in result2]
        result.append(tuple(result2))
    return result


def get_area(element):
    "Returns the area of the surface"
    
    coordinates=get_coordinates(element)
    if len(coordinates)>0:
        return _AreaOf3DPolygon(coordinates)
    else:
        return None
    

def _AreaOf3DPolygon(c):
    """
    Returns the area of a 3D polygon
    
    Arguments:
        c (list): the coordinates, as a list of tuples i.e.
            [(6.0, 0.0, 6.0), (0.0, 0.0, 6.0), (0.0, 0.0, 3.0), (6.0, 0.0, 3.0)]
    
    """
    #Convert 3D coordinates to 2D coordinates
    loc0=[c[0][0],c[0][1],c[0][2]]
    locx=[loc0[0]-c[1][0],loc0[1]-c[1][1],loc0[2]-c[1][2]]
    normal = _CrossProductOperator(locx[0], locx[1], locx[2], c[2][0] - loc0[0], c[2][1] - loc0[1], c[2][2] - loc0[2])
    locy = _CrossProductOperator(normal[0], normal[1], normal[2], locx[0], locx[1], locx[2])
    locx = _Normalise(locx[0], locx[1], locx[2])
    locy = _Normalise(locy[0], locy[1], locy[2])
    X1=[]
    Y1=[]
    for d in c:
        X1.append(_Dot(d[0] - loc0[0], d[1] - loc0[1], d[2] - loc0[2], locx[0], locx[1], locx[2]))
        Y1.append(_Dot(d[0] - loc0[0], d[1] - loc0[1], d[2] - loc0[2], locy[0], locy[1], locy[2]))
    X2=X1
    Y2=Y1
    X2.append(X1[0])
    Y2.append(Y1[0])
    a=0
    for i in range(len(X2)-1):
        a = a + X2[i] * Y2[i + 1] - X2[i + 1] * Y2[i]
    return abs(a/2)

def _CrossProductOperator(ax, ay, az, bx, by, bz):
    return [ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx]

def _Normalise(X, Y, Z):
    Length = (((X**2 + Y**2)**0.5)**2 + Z**2)**0.5
    return [X / Length, Y / Length, Z / Length]

def _Dot(ax, ay, az, bx, by, bz):
    return ax * bx + ay * by + az * bz       


def get_opening_ids(element):
    "Returns a list of Opening ids"
    
    st='./gbxml:Opening/@id'
    return element.xpath(st,namespaces=ns)
    
    


















