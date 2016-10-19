from packages import point_on_line
from geojson import LineString

# Takes a {@link LineString|line}, a start {@link Point}, and a stop point
# and returns a subsection of the line in-between those points.
# The start & stop points don't need to fall exactly on the line.
#
# This can be useful for extracting only the part of a route between waypoints.
#
# @name lineSlice
# @param {Feature<Point>} startPt starting point
# @param {Feature<Point>} stopPt stopping point
# @param {Feature<LineString>|LineString} line line to slice
# @return {Feature<LineString>} sliced line
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
# var start = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-77.029609, 38.881946]
#   }
# };
# var stop = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-77.021884, 38.889563]
#   }
# };
#
# var sliced = turf.lineSlice(start, stop, line);
#
# //=line
#
# //=sliced

def line_slice(start_pt, stop_pt, line):
    if line["type"] == 'Feature':
        coords = line["geometry"]["coordinates"]
    elif line["type"] == 'LineString':
        coords = line["coordinates"]
    else:
        raise ValueError('input must be a LineString Feature or Geometry')

    start_vertex = point_on_line(line, start_pt)
    stop_vertex = point_on_line(line, stop_pt)

    if start_vertex["properties"]["index"] <= \
       stop_vertex["properties"]["index"]:
        ends = [start_vertex, stop_vertex]
    else:
        ends = [stop_vertex, start_vertex]

    clip_line = LineString((ends[0]["geometry"]["coordinates"],))
    for i in range(ends[0]["properties"]["index"],
                   ends[1]["properties"]["index"] + 1):
        clip_line.geometry.coordinates.push(coords[i])
    clip_line["geometry"]["coordinates"].append(ends[1]["geometry"]["coordinates"])

    return clip_line
