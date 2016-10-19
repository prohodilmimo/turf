from packages import bearing, destination, distance

# Takes two {@link Point|points} and returns a point midway between them.
# The midpoint is calculated geodesically, meaning the curvature of the earth
#   is taken into account.
#
# @name midpoint
# @param {Feature<Point>} from first point
# @param {Feature<Point>} to second point
# @return {Feature<Point>} a point midway between `pt1` and `pt2`
# @example
# var pt1 = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [144.834823, -37.771257]
#   }
# };
# var pt2 = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [145.14244, -37.830937]
#   }
# };
#
# var midpointed = turf.midpoint(pt1, pt2);
# midpointed.properties['marker-color'] = '#f00';
#
#
# var result = {
#   "type": "FeatureCollection",
#   "features": [pt1, pt2, midpointed]
# };
#
# //=result
def midpoint (point_from, point_to):
    dist = distance(point_from, point_to, 'miles')
    heading = bearing(point_from, point_to)

    return destination(point_from, dist / 2, heading, 'miles')
