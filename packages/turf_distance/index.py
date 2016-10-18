from packages.turf_invariant import get_coord
from packages.turf_helpers import radians_to_distance
import math
# //http://en.wikipedia.org/wiki/Haversine_formula
# //http://www.movable-type.co.uk/scripts/latlong.html

# Calculates the distance between two {@link Point|points} in degrees, radians,
# miles, or kilometers. This uses the
# [Haversine formula](http://en.wikipedia.org/wiki/Haversine_formula)
# to account for global curvature.
# 
# @name distance
# @param {Feature<Point>} from origin point
# @param {Feature<Point>} to destination point
# @param {String} [units=kilometers] can be degrees, radians, miles, or kilometers
# @return {Number} distance between the two points
# @example
# var from = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-75.343, 39.984]
#   }
# };
# var to = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-75.534, 39.123]
#   }
# };
# var units = "miles";
# 
# var points = {
#   "type": "FeatureCollection",
#   "features": [from, to]
# };
# 
# //=points
# 
# var distance = turf.distance(from, to, units);
# 
# //=distance
# 
def distance (point_from, point_to, units):
    degrees2radians = math.pi / 180
    coordinates1 = get_coord(point_from)
    coordinates2 = get_coord(point_to)
    d_lat = degrees2radians * (coordinates2[1] - coordinates1[1])
    d_lon = degrees2radians * (coordinates2[0] - coordinates1[0])
    lat1 = degrees2radians * coordinates1[1]
    lat2 = degrees2radians * coordinates2[1]

    a = math.pow(math.sin(d_lat / 2), 2) + \
        math.pow(math.sin(d_lon / 2), 2) * math.cos(lat1) * math.cos(lat2)

    return radians_to_distance(
        2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)),
        units
    )

