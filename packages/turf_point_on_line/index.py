from packages import bearing, destination, distance
from geojson import Point

# Takes a {@link Point} and a {@link LineString} and calculates
#   the closest Point on the LineString.
#
# @name inner_function
# @param {Feature<LineString>} line line to snap to
# @param {Feature<Point>} pt point to snap from
# @param {String} [units=miles] can be degrees, radians, miles, or kilometers
# @return {Feature<Point>} closest point on the `line` to `point`
# @example
# var line = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "LineString",
#     "coordinates": [
#       [-77.031669, 38.878605],
#       [-77.029609, 38.881946],
#       [-77.020339, 38.884084],
#       [-77.025661, 38.885821],
#       [-77.021884, 38.889563],
#       [-77.019824, 38.892368]
#     ]
#   }
# };
# var pt = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-77.037076, 38.884017]
#   }
# };
#
# var snapped = turf.inner_function(line, pt, 'miles');
# snapped.properties['marker-color'] = '#00f'
#
# var result = {
#   "type": "FeatureCollection",
#   "features": [line, pt, snapped]
# };
#
# //=result

def point_on_line (line, pt, units='miles'):
    if line["type"] == 'Feature':
        coords = line["geometry"]["coordinates"]
    elif line["type"] == 'LineString':
        coords = line["coordinates"]
    else:
        raise ValueError('input must be a LineString Feature or Geometry')

    return inner_function(pt, coords, units)


def inner_function(pt, coords, units):
    closest_pt = Point((float("inf"), float("inf")), {
        "dist": float("inf")
    })
    for i in range(len(coords)):
        start = Point(coords[i])
        stop = Point(coords[i + 1])
        # start
        start.properties.dist = distance(pt, start, units)
        # stop
        stop.properties.dist = distance(pt, stop, units)
        # perpendicular
        height_distance = max(start.properties.dist, stop.properties.dist)
        direction = bearing(start, stop)
        perpendicular_pt1 = destination(pt, height_distance, direction + 90, units)
        perpendicular_pt2 = destination(pt, height_distance, direction - 90, units)
        intersect = line_intersects(
            perpendicular_pt1.geometry.coordinates[0],
            perpendicular_pt1.geometry.coordinates[1],
            perpendicular_pt2.geometry.coordinates[0],
            perpendicular_pt2.geometry.coordinates[1],
            start.geometry.coordinates[0],
            start.geometry.coordinates[1],
            stop.geometry.coordinates[0],
            stop.geometry.coordinates[1]
        )

        if intersect:
            intersect_pt = Point(intersect)
            intersect_pt.properties.dist = distance(pt, intersect_pt, units)

        if start.properties.dist < closest_pt.properties.dist:
            closest_pt = start
            closest_pt.properties.index = i
        if stop.properties.dist < closest_pt.properties.dist:
            closest_pt = stop
            closest_pt.properties.index = i
        if intersect_pt and intersect_pt.properties.dist < closest_pt.properties.dist:
            closest_pt = intersect_pt
            closest_pt.properties.index = i

    return closest_pt

# modified from http://jsfiddle.net/justin_c_rounds/Gd2S2/light/
def line_intersects(line1_start_x, line1_start_y, line1_end_x, line1_end_y,
                    line2_start_x, line2_start_y, line2_end_x, line2_end_y):
    # if the lines intersect, the result contains the x and y
    #   of the intersection (treating the lines as infinite) and booleans
    #   for whether line segment 1 or line segment 2 contain the point
    result = {"x": None, "y": None, "onLine1": False, "onLine2": False}
    denominator = ((line2_end_y - line2_start_y) *
                   (line1_end_x - line1_start_x)) - \
                  ((line2_end_x - line2_start_x) *
                   (line1_end_y - line1_start_y))
    if denominator == 0:
        if result.x is not None and result.y is not None:
            return result
        else:
            return False
    a = line1_start_y - line2_start_y
    b = line1_start_x - line2_start_x
    numerator1 = ((line2_end_x - line2_start_x) * a) - \
                 ((line2_end_y - line2_start_y) * b)
    numerator2 = ((line1_end_x - line1_start_x) * a) - \
                 ((line1_end_y - line1_start_y) * b)
    a = numerator1 / denominator
    b = numerator2 / denominator

    # if we cast these lines infinitely in both directions,
    #   they intersect here:
    result.x = line1_start_x + (a * (line1_end_x - line1_start_x))
    result.y = line1_start_y + (a * (line1_end_y - line1_start_y))

    # if line1 is a segment and line2 is infinite, they intersect if:
    if 0 < a < 1:
        result.onLine1 = True

    # if line2 is a segment and line1 is infinite, they intersect if:
    if 0 < b < 1:
        result.onLine2 = True

    # if line1 and line2 are segments,
    #   they intersect if both of the above are true
    if result.onLine1 and result.onLine2:
        return [result.x, result.y]
    else:
        return False
