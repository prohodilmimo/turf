from packages import bearing, distance as measure_distance, destination
from geojson import Point

# Takes a {@link LineString|line} and returns a {@link Point|point}
#  at a specified distance along the line.
#
# @name along
# @param {Feature<LineString>} line input line
# @param {number} distance distance along the line
# @param {String} [units=miles] can be degrees, radians, miles, or kilometers
# @return {Feature<Point>} Point `distance` `units` along the line
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
#
# var along = turf.along(line, 1, 'miles');
#
# var result = {
#   "type": "FeatureCollection",
#   "features": [line, along]
# };
#
# //=result
#
def along (line, distance, units):
    if line["type"] == 'Feature':
        coords = line["geometry"]["coordinates"]
    elif line["type"] == 'LineString':
        coords = line["coordinates"]
    else:
        raise ValueError("input must be a LineString Feature or Geometry")

    travelled = 0
    for i in range(len(coords)):
        if distance >= travelled and (i == len(coords) - 1):
            break
        elif travelled >= distance:
            overshot = distance - travelled
            if not overshot:
                return Point(coords[i])
            else:
                direction = bearing(coords[i], coords[i - 1]) - 180
                interpolated = destination(coords[i], overshot,
                                           direction, units)
                return interpolated
        else:
            travelled += measure_distance(coords[i], coords[i + 1], units)

    return Point(coords[coords.length - 1])

