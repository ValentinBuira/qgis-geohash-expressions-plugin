# Qgis geohash expressions plugin

This plugin adds four expression functions to work with geohash in the field calculator 

## How to use

The expressions functions of plugin are all located in the field calculator window under the "Geohash" folder 


![Screenshot of where are the expressions function add in the field calcultor](<How to use plugin.png>)


#### geohash
Calculate the <a href="http://en.wikipedia.org/wiki/Geohash">GeoHash</a> from a geometry, the coordinates used to calculate the geohash are the coordinates of the centroid of the geometry.
#### geohash_yx
Calculate the GeoHash from y, x (latitude, longitude) coordinates. 
#### geom_from_geohash
Return a geometry from a GeoHash string. The geometry will be a polygon representing the GeoHash bounds. 
#### point_from_geohash

Return a point geometry from a GeoHash string. The point represents the center point of the GeoHash. 

## Thanks 

This plugin is based off Leonard Norrgård's geohash implementation in python so special thanks to him.
