from packages import destination
from geojson import Polygon

# Takes a {@link Point} and calculates the circle polygon given a radius
#   in degrees, radians, miles, or kilometers; and steps for precision.
#
# @name circle
# @param {Feature<Point>} center center point
# @param {number} radius radius of the circle
# @param {number} [steps=64] number of steps
# @param {string} [units=kilometers] miles, kilometers, degrees, or radians
# @returns {Feature<Polygon>} circle polygon
# @example
# var center = point([-75.343, 39.984]);
# var radius = 5;
# var steps = 10;
# var units = 'kilometers';
#
# var circle = turf.circle(center, radius, steps, units);
#
# //=circle
#
def circle(center, radius, steps, units):
    steps = steps or 64
    coordinates = []

    for i in range(steps):
        point = destination(center, radius, i * 360 / steps, units)
        coordinates.append(point["geometry"]["coordinates"])

    coordinates.append(coordinates[0])

    return Polygon([coordinates])
