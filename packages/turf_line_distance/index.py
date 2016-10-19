from packages import distance
from geojson import Point

# Takes a {@link LineString} or {@link Polygon} and measures its length
#   in the specified units.
#
# @name lineDistance
# @param {Feature<(LineString|Polygon)>|FeatureCollection<(LineString|Polygon)>} line line to measure
# @param {String} [units=kilometers] can be degrees, radians, miles, or kilometers
# @return {Number} length of the input line
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
# var length = turf.lineDistance(line, 'miles');
#
# //=line
#
# //=length
def line_distance(line, units):
    if line["type"] == 'FeatureCollection':
        return reduce(lambda memo, feature: memo + line_distance(feature, units), line["features"], 0)

    geometry = line["geometry"] if line["type"] == 'Feature' else line

    if geometry["type"] == 'LineString':
        return length(geometry["coordinates"], units)

    elif geometry["type"] == 'Polygon' or geometry["type"] == 'MultiLineString':
        d = 0
        for i in range(len(geometry["coordinates"])):
            d += length(geometry["coordinates"][i], units)
        return d

    elif geometry["type"] == 'MultiPolygon':
        d = 0
        for i in range(len(geometry["coordinates"])):
            for j in range(len(geometry["coodinates"][i])):
                d += length(geometry["coordinates"][i][j], units)

        return d

    else:
        raise ValueError(
            'input must be a LineString, MultiLineString, Polygon, '
            'or MultiPolygon Feature or Geometry (or a FeatureCollection '
            'containing only those types)')


def length(coords, units):
    travelled = 0
    prev_coords = Point(coords[0])
    cur_coords = Point(coords[0])

    for i in range(len(coords)):
        cur_coords.geometry.coordinates = coords[i]
        travelled += distance(prev_coords, cur_coords, units)
        temp = prev_coords
        prev_coords = cur_coords
        cur_coords = temp

    return travelled
