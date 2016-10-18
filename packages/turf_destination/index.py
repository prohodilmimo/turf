# http://en.wikipedia.org/wiki/Haversine_formula
# http://www.movable-type.co.uk/scripts/latlong.html
from packages.turf_invariant import get_coord
from packages.turf_helpers import distance_to_radians
from geojson import Point
import math

# Takes a {@link Point} and calculates the location of a 
#   destination point given a distance in degrees, radians, miles, or kilometers;
#   and bearing in degrees. 
#   This uses the [Haversine formula](http://en.wikipedia.org/wiki/Haversine_formula)
#   to account for global curvature.
# 
# @name destination
# @param {Feature<Point>} from starting point
# @param {number} distance distance from the starting point
# @param {number} bearing ranging from -180 to 180
# @param {String} [units=kilometers] miles, kilometers, degrees, or radians
# @returns {Feature<Point>} destination point
# @example
# var point = {
#   "type": "Feature",
#   "properties": {
#     "marker-color": "#0f0"
#   },
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-75.343, 39.984]
#   }
# };
# var distance = 50;
# var bearing = 90;
# var units = 'miles';
# 
# var destination = turf.destination(point, distance, bearing, units);
# destination.properties['marker-color'] = '#f00';
# 
# var result = {
#   "type": "FeatureCollection",
#   "features": [point, destination]
# };
# 
# //=result
# 
def destination (point_from, distance, bearing, units):
    degrees2radians = math.pi / 180
    radians2degrees = 180 / math.pi
    coordinates1 = get_coord(point_from)
    longitude1 = degrees2radians * coordinates1[0]
    latitude1 = degrees2radians * coordinates1[1]
    bearing_rad = degrees2radians * bearing

    radians = distance_to_radians(distance, units)

    latitude2 = math.asin(
        math.sin(latitude1) * math.cos(radians) +
        math.cos(latitude1) * math.sin(radians) * math.cos(bearing_rad)
    )
    longitude2 = longitude1 + math.atan2(
        math.sin(bearing_rad) * math.sin(radians) * math.cos(latitude1),
        math.cos(radians) - math.sin(latitude1) * math.sin(latitude2)
    )

    return Point((radians2degrees * longitude2, radians2degrees * latitude2))
