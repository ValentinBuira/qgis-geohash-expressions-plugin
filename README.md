# Qgis geohash expressions plugin

This plugin adds expression functions to work with geohash in the field calculator 

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O5O41BY00W)

## How to use

The expressions functions of plugin are all located in the field calculator window under the "Geohash" folder 


![Screenshot of where are the expressions function add in the field calcultor](<how_to_use_plugin.png>)


#### geohash_from_geom | geohash
Calculate the <a href="http://en.wikipedia.org/wiki/Geohash">GeoHash</a> from a geometry, the coordinates used to calculate the geohash are the coordinates of the centroid of the geometry.
#### geohash_yx
Calculate the GeoHash from y, x (latitude, longitude) coordinates. 
#### geom_from_geohash
Return a geometry from a GeoHash string. The geometry will be a polygon representing the GeoHash bounds. 
#### point_from_geohash

Return a point geometry from a GeoHash string. The point represents the center point of the GeoHash. 
#### geohash_neighbors
Return an array of all the neighbors from a GeoHash string
#### geohash_neighbors_map
Return a map of all the neighbors from a GeoHash string
#### geohash_(north|northeast|east|southeast|south|southwest|west|northwest)
Return the specified cardinal point neighbor of a geohash string.

## Thanks 

This plugin is based off Leonard Norrgård's geohash implementation in python so special thanks to him.
