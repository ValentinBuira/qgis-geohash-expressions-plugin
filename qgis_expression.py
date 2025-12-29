from qgis.core import *
from qgis.gui import *
from qgis.core import Qgis

from .geohash import encode, decode, decode_extent, neighbours, neighbours_dict

@qgsfunction(args=-1, group='Geohash')
def geohash(values, feature, parent):
    """
    Calculate the <a href="http://en.wikipedia.org/wiki/Geohash">GeoHash</a> from a geometry, the coordinates used to calculate the geohash are the coordinates of the centroid of the geometry.
    
    <p>
    A GeoHash encodes a geographic Point into a text form that is sortable and searchable based on prefixing. A shorter GeoHash is a less precise representation of a point. It can be thought of as a box that contains the point. 
    </p>

    <h4>Syntax</h4>
    <p><b>geohash</b>( <i>geometry[, precision=12]</i> )</p>

    <h4>Arguments</h4>
    <p><i>geometry</i> &rarr; a geometry</p>
    <p><i>precision</i> &rarr; optional precision as characters count. Default value is 12 if not specified. 


<dl>
<dt>Precision increase as following:</dt>
<dd>#precision  km</dd>
<dd>4   ± 20 km</dd>
<dd>5   ± 2.4 km</dd>
<dd>6   ± 0.61 km</dd>
<dd>7   ± 0.076 km</dd>
<dd>8   ± 0.019 km</dd>

</dl>

    </p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash</b>(make_point(-126, 48)) &rarr; 'c0w3hf1s70w3'</li>
      <li><b>geohash</b>(make_point(-126, 48), 5) &rarr; 'c0w3h'</li>
      <li><b>geohash</b>($geometry) &rarr; 'spezef7b6ztj'</li>
    </ul>
    """
    if len(values) < 1 or len(values) > 2:
        parent.setEvalErrorString("Error: invalid number of arguments")
        return
        
    precision = 12
    if len(values) == 2:
        precision = int(values[1])
        
    geometry = values[0]
    point = geometry.centroid().asPoint()
    lon, lat = (point.x(), point.y())
    geohash = encode(lat , lon, precision=precision)
    return geohash

@qgsfunction(args=-1, group='Geohash')
def geohash_yx(values, feature, parent):
    """
    Calculate the <a href="http://en.wikipedia.org/wiki/Geohash">GeoHash</a> from y, x (latitude, longitude) coordinates. 
    
    <p>
    A GeoHash encodes a geographic Point into a text form that is sortable and searchable based on prefixing. A shorter GeoHash is a less precise representation of a point. It can be thought as a box that contains the point. 
    </p>

    <h4>Syntax</h4>
    <p><b>geohash_yx</b>( <i>y, x[, precision=12]</i> )</p>

    <h4>Arguments</h4>
    <p><i>y</i> &rarr; the y or latitude coordinate.</p>
    <p><i>x</i> &rarr; the x or longitude coordinate.</p>
    <p><i>precision</i> &rarr; optional precision as characters count. Default value is 12 if not specified. 


<dl>
<dt>Precision increase as following:</dt>
<dd>#precision  km</dd>
<dd>4   ± 20 km</dd>
<dd>5   ± 2.4 km</dd>
<dd>6   ± 0.61 km</dd>
<dd>7   ± 0.076 km</dd>
<dd>8   ± 0.019 km</dd>

</dl>

    </p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_yx</b>(-126, 48)  &rarr; 'c0w3hf1s70w3'</li>
      <li><b>geohash_yx</b>(-126, 48, 5)  &rarr; 'c0w3h'</li>
      <li><b>geohash_yx</b>('-126', '48')  &rarr; 'c0w3hf1s70w3'</li>
    </ul>
    """
    if len(values) < 2 or len(values) > 3:
        parent.setEvalErrorString("Error: invalid number of arguments")
        return
        
    precision = 12
    if len(values) == 3:
        precision = int(values[2])

    lat = float(values[1])
    lon = float(values[0])
    geohash = encode(lat , lon, precision=precision)
    return geohash

@qgsfunction(args='auto', group='Geohash')
def geom_from_geohash(geohash, feature, parent) :
    """
    Return a geometry from a GeoHash string. The geometry will be a polygon representing the GeoHash bounds.
    <h4>Syntax</h4>
    <p><b>geom_from_geohash</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geom_from_geohash</b>('9qqj7nmxncgyy4d0dbxqz0') &rarr; 'Polygon ((-115.172816 36.114646,-115.172816 36.114646,-115.172816 36.114646,-115.172816 36.114646,-115.172816 36.114646))'</li>
    </ul>
    """
    lat_min, lat_max, lon_min, lon_max  = decode_extent(geohash)
    rect = QgsRectangle(lon_min, lat_min, lon_max, lat_max)
    polygon = QgsGeometry.fromRect(rect)
    return polygon

@qgsfunction(args='auto', group='Geohash')
def point_from_geohash(geohash, feature, parent):
    """
    Return a point geometry from a GeoHash string. The point represents the center point of the GeoHash.
    <h4>Syntax</h4>
    <p><b>point_from_geohash</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>point_from_geohash</b>('9qqj7nmxncgyy4d0dbxqz0') &rarr; 'Point (-115.172816 36.114646)'</li>
    </ul>
    """
    lat, lon = decode(geohash)
    lat, lon = float(lat), float(lon)
    point = QgsGeometry.fromPointXY(QgsPointXY(lat, lon))
    return point

@qgsfunction(args='auto', group='Geohash')
def geohash_neighbours(geohash, feature, parent):
    """
    Return an array of all the neighbors from a GeoHash string. The returned geohashes array is in order ['N', 'NE', 'E', 'SE','S', 'SW', 'W', 'NW']

    <h4>Syntax</h4>
    <p><b>geohash_neighbours</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_neighbours</b>('w21z74nz') &rarr; [ 'w21z74qb', 'w21z74r0', 'w21z74nx', 'w21z74pp', 'w21z74nw', 'w21z74ny', 'w21z74pn', 'w21z74q8' ]</li>
    </ul>

    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours(geohash)

@qgsfunction(args='auto', group='Geohash')
def geohash_neighbours_map(geohash, feature, parent):
    """
    Return a map of all the neighbors from a GeoHash string. The key in the map are the following cardinal point: 'N', 'NE', 'E', 'SE','S', 'SW', 'W', 'NW' .

    <h4>Syntax</h4>
    <p><b>geohash_neighbours_map</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_neighbours_map</b>('w21z74nz') &rarr; { 'E': 'w21z74nx', 'N': 'w21z74qb', 'NE': 'w21z74r0', 'NW': 'w21z74q8', 'S': 'w21z74nw', 'SE': 'w21z74pp', 'SW': 'w21z74ny', 'W': 'w21z74pn' }</li>
      <li><b>geohash_neighbours_map</b>('w21z74nz')[<b>'N'</b>] &rarr; 'w21z74qb'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours</i> function </p>
    <p><i>geohash_(north|northeast|east|southeast|south|southwest|west|northwest)</i> functions </p>

    """
    return neighbours_dict(geohash)


@qgsfunction(args='auto', group='Geohash')
def geohash_north(geohash, feature, parent):
    """
    Return the northen neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['N']
    <pre>
    +----+---+----+
    | NW | <b>N</b> | NE |
    +----+---+----+
    | W  |   | E  |
    +----+---+----+
    | SW | S | SE |
    +----+---+----+
    </pre>
    <h4>Syntax</h4>
    <p><b>geohash_north</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_north</b>('w21z74nz') &rarr; 'w21z74qb'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['N']

@qgsfunction(args='auto', group='Geohash')
def geohash_northeast(geohash, feature, parent):
    """
    Return the north east neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['NE']
    <pre>
    +----+---+----+
    | NW | N | <b>NE</b> |
    +----+---+----+
    | W  |   | E  |
    +----+---+----+
    | SW | S | SE |
    +----+---+----+
    </pre>

    <h4>Syntax</h4>
    <p><b>geohash_northeast</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_northeast</b>('w21z74nz') &rarr; 'w21z74r0'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['NE']

@qgsfunction(args='auto', group='Geohash')
def geohash_east(geohash, feature, parent):
    """
    Return the eastern neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['E']
    <pre>
    +----+---+----+
    | NW | N | NE |
    +----+---+----+
    | W  |   | <b>E</b> |
    +----+---+----+
    | SW | S | SE |
    +----+---+----+
    </pre>

    <h4>Syntax</h4>
    <p><b>geohash_east</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_east</b>('w21z74nz') &rarr; 'w21z74nx'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['E']


@qgsfunction(args='auto', group='Geohash')
def geohash_southeast(geohash, feature, parent):
    """
    Return the south east neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['SE']
    <pre>
    +----+---+----+
    | NW | N | NE |
    +----+---+----+
    | W  |   | E  |
    +----+---+----+
    | SW | S | <b>SE</b> |
    +----+---+----+
    </pre>
    
    <h4>Syntax</h4>
    <p><b>geohash_southeast</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_southeast</b>('w21z74nz') &rarr; 'w21z74pp'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['SE']


@qgsfunction(args='auto', group='Geohash')
def geohash_south(geohash, feature, parent):
    """
    Return the southern neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['S']
    <pre>
    +----+---+----+
    | NW | N | NE |
    +----+---+----+
    | W  |   | E  |
    +----+---+----+
    | SW | <b>S</b> | SE |
    +----+---+----+
    </pre>
    <h4>Syntax</h4>
    <p><b>geohash_south</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_south</b>('w21z74nz') &rarr; 'w21z74nw'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['S']


@qgsfunction(args='auto', group='Geohash')
def geohash_southwest(geohash, feature, parent):
    """
    Return the south west neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['SW']
    <pre>
    +----+---+----+
    | NW | N | NE |
    +----+---+----+
    | W  |   | E  |
    +----+---+----+
    | <b>SW</b>| S | SE |
    +----+---+----+
    </pre>

    <h4>Syntax</h4>
    <p><b>geohash_southwest</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_southwest</b>('w21z74nz') &rarr; 'w21z74ny'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['SW']

@qgsfunction(args='auto', group='Geohash')
def geohash_west(geohash, feature, parent):
    """
    Return the western neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['W']
    
    <pre>
    +----+---+----+
    | NW | N | NE |
    +----+---+----+
    | <b>W</b> |   | E  |
    +----+---+----+
    | SW | S | SE |
    +----+---+----+
    </pre>
    
    <h4>Syntax</h4>
    <p><b>geohash_west</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_west</b>('w21z74nz') &rarr; 'w21z74pn'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['W']

@qgsfunction(args='auto', group='Geohash')
def geohash_northwest(geohash, feature, parent):
    """
    Return the north west neighbor of a geohash string.<br>Handy shortcut for geohash_neighbours_map(geohash)['NW']

    <pre>
    +----+---+----+
    | <b>NW</b>| N | NE |
    +----+---+----+
    | W  |   | E  |
    +----+---+----+
    | SW | S | SE |
    +----+---+----+
    </pre>

    <h4>Syntax</h4>
    <p><b>geohash_northwest</b>( <i>geohash</i> )</p>

    <h4>Arguments</h4>
    <p><i>geohash</i> &rarr; the geohash string.</p>

    <h4>Example usage</h4>
    <ul>
      <li><b>geohash_northwest</b>('w21z74nz') &rarr; 'w21z74q8'</li>
    </ul>
    <h4>See also</h4>
    <p><i>geohash_neighbours_map</i> function </p>
    """
    return neighbours_dict(geohash)['NW']


