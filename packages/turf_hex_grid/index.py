from packages import distance
from geojson import Point, Polygon, FeatureCollection
import math

# Precompute cosines and sines of angles used in hexagon creation
#   for performance gain
cosines = []
sines = []
for ii in range(6):
    angle = 2 * math.pi / 6 * ii
    cosines.append(math.cos(angle))
    sines.append(math.sin(angle))

# Takes a bounding box and a cell size in degrees and returns a {@link FeatureCollection} of flat-topped
# hexagons ({@link Polygon} features) aligned in an "odd-q" vertical grid as
# described in [Hexagonal Grids](http://www.redblobgames.com/grids/hexagons/).
#
# @name hexGrid
# @param {Array<number>} bbox extent in [minX, minY, maxX, maxY] order
# @param {number} cellSize dimension of cell in specified units
# @param {string} [units=kilometers] used in calculating cellSize, can be degrees, radians, miles, or kilometers
# @param {boolean} triangles whether to return as triangles instead of hexagons
# @return {FeatureCollection<Polygon>} a hexagonal grid
# @example
# var bbox = [-96,31,-84,40];
# var cellSize = 50;
# var units = 'miles';
#
# var hexgrid = turf.hexGrid(bbox, cellSize, units);
#
# //=hexgrid
def hex_grid(bbox, cell_size, units, triangles):
    x_fraction = cell_size / (distance(Point((bbox[0], bbox[1])),
                                       Point((bbox[2], bbox[1])), units))
    cell_width = x_fraction * (bbox[2] - bbox[0])
    y_fraction = cell_size / (distance(Point((bbox[0], bbox[1])),
                                       Point((bbox[0], bbox[3])), units))
    cell_height = y_fraction * (bbox[3] - bbox[1])
    radius = cell_width / 2

    hex_width = radius * 2
    hex_height = math.sqrt(3) / 2 * cell_height

    box_width = bbox[2] - bbox[0]
    box_height = bbox[3] - bbox[1]

    x_interval = 3 / 4 * hex_width
    y_interval = hex_height

    x_span = box_width / (hex_width - radius / 2)
    x_count = math.ceil(x_span)
    if round(x_span) == x_count:
        x_count += 1

    x_adjust = ((x_count * x_interval - radius / 2) - box_width) / 2 - radius / 2

    y_count = math.ceil(box_height / hex_height)

    y_adjust = (box_height - y_count * hex_height) / 2

    has_offset_y = y_count * hex_height - box_height > hex_height / 2
    if has_offset_y:
        y_adjust -= hex_height / 4

    fc = FeatureCollection([])
    for x in range(x_count):
        for y in range(y_count):

            is_odd = x % 2 == 1
            if y == 0 and is_odd:
                continue

            if y == 0 and has_offset_y:
                continue

            center_x = x * x_interval + bbox[0] - x_adjust
            center_y = y * y_interval + bbox[1] + y_adjust

            if is_odd:
                center_y -= hex_height / 2
            if triangles:
                fc["features"] += [
                    hex_triangles([center_x, center_y],
                                  cell_width / 2, cell_height / 2)
                ]
            else:
                fc["features"] += [
                    hexagon([center_x, center_y],
                            cell_width / 2, cell_height / 2)
                ]

    return fc

# //Center should be [x, y]
def hexagon(center, rx, ry):
    vertices = []
    for i in range(6):
        x = center[0] + rx * cosines[i]
        y = center[1] + ry * sines[i]
        vertices.append([x, y])

    # //first and last vertex must be the same
    vertices.append(vertices[0])
    return Polygon((vertices,))


# //Center should be [x, y]
def hex_triangles(center, rx, ry):
    triangles = []
    for i in range(6):
        vertices = []
        vertices.append(center)
        vertices.append([
            center[0] + rx * cosines[i],
            center[1] + ry * sines[i]
        ])
        vertices.append([
            center[0] + rx * cosines[(i + 1) % 6],
            center[1] + ry * sines[(i + 1) % 6]
        ])
        vertices.append(center)
        triangles.append(Polygon((vertices,)))
    return triangles
