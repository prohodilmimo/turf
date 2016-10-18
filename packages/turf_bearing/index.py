from packages.turf_invariant import get_coord
import math
# http://en.wikipedia.org/wiki/Haversine_formula
# http://www.movable-type.co.uk/scripts/latlong.html

# Takes two {@link Point|points} and finds the geographic bearing between them.
#
# @name bearing
# @param {Feature<Point>} start starting Point
# @param {Feature<Point>} end ending Point
# @returns {Number} bearing in decimal degrees
# @example
# var point1 = {
#   "type": "Feature",
#   "properties": {
#     "marker-color": '#f00'
#   },
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-75.343, 39.984]
#   }
# };
# var point2 = {
#   "type": "Feature",
#   "properties": {
#     "marker-color": '#0f0'
#   },
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-75.534, 39.123]
#   }
# };
#
# var points = {
#   "type": "FeatureCollection",
#   "features": [point1, point2]
# };
#
# //=points
#
# var bearing = turf.bearing(point1, point2);
#
# //=bearing
#
def bearing (start, end):
    degrees2radians = math.pi / 180
    radians2degrees = 180 / math.pi
    coordinates1 = get_coord(start)
    coordinates2 = get_coord(end)

    lon1 = degrees2radians * coordinates1[0]
    lon2 = degrees2radians * coordinates2[0]
    lat1 = degrees2radians * coordinates1[1]
    lat2 = degrees2radians * coordinates2[1]
    a = math.sin(lon2 - lon1) * math.cos(lat2)
    b = math.cos(lat1) * math.sin(lat2) - \
        math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    return radians2degrees * math.atan2(a, b)
