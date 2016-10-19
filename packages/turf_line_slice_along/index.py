from packages import bearing, destination, distance
from geojson import LineString


# Takes a {@link LineString|line}, a specified distance along the line
#   to a start {@link Point},
# and a specified  distance along the line to a stop point
# and returns a subsection of the line in-between those points.
#
# This can be useful for extracting only the part of a route
#   between two distances.
#
# @name line_slice_along
# @category misc
# @param {Feature<LineString>} line input line
# @param {Number} startDist distance along the line to starting point
# @param {Number} stopDist distance along the line to ending point
# @param {String} [units=kilometers] can be degrees, radians, miles,
#   or kilometers
# @return {Feature<LineString>} sliced line
# @example
# var line = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "LineString",
#     "coordinates": [
#       [ 7.66845703125, 45.058001435398296 ],
#       [ 9.20654296875, 45.460130637921004 ],
#       [ 11.348876953125, 44.48866833139467 ],
#       [ 12.1728515625, 45.43700828867389 ],
#       [ 12.535400390625, 43.98491011404692 ],
#       [ 12.425537109375, 41.86956082699455 ],
#       [ 14.2437744140625, 40.83874913796459 ],
#       [ 14.765625, 40.681679458715635 ]
#     ]
#   }
# };
# var start = 12.5;
#
# var stop = 25;
#
# var units = 'miles';
#
# var sliced = turf.line_slice_along(start, stop, line, units);
#
# //=line
#
# //=sliced
def line_slice_along(line, start_dist, stop_dist, units):
    slice = []
    if line["type"] == 'Feature':
        coords = line.geometry.coordinates
    elif line["type"] == 'LineString':
        coords = line.coordinates
    else:
        raise ValueError('input must be a LineString Feature or Geometry')

    travelled = 0
    for i in range(len(coords)):
        if start_dist >= travelled and i == coords.length - 1:
            break
        elif travelled > start_dist and len(slice) == 0:
            overshot = start_dist - travelled
            if not overshot:
                return slice.append(coords[i])
            direction = bearing(coords[i], coords[i - 1]) - 180
            interpolated = destination(coords[i], overshot, direction, units)
            slice.append(interpolated.geometry.coordinates)

        if travelled >= stop_dist:
            overshot = stop_dist - travelled
            if not overshot:
                return slice.append(coords[i])
            direction = bearing(coords[i], coords[i - 1]) - 180
            interpolated = destination(coords[i], overshot, direction, units)
            slice.append(interpolated.geometry.coordinates)
            return LineString(tuple(slice))

        if travelled >= start_dist:
            slice.append(coords[i])

        travelled += distance(coords[i], coords[i + 1], units)

    return LineString(coords[coords.length - 1])
