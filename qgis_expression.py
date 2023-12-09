from qgis.core import *
from qgis.gui import *
from qgis.core import Qgis

from .geohash import encode, decode, decode_extent

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
    A GeoHash encodes a geographic Point into a text form that is sortable and searchable based on prefixing. A shorter GeoHash is a less precise representation of a point. It can be thought of as a box that contains the point. 
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