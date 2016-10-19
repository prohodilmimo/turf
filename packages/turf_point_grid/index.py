from packages import distance
from geojson import FeatureCollection, Point
# Takes a bounding box and a cell depth and returns
#   a set of {@link Point|points} in a grid.
#
# @name pointGrid
# @param {Array<number>} bbox extent in [minX, minY, maxX, maxY] order
# @param {number} cellSize the distance across each cell
# @param {string} [units=kilometers] used in calculating cellSize,
#   can be degrees, radians, miles, or kilometers
# @return {FeatureCollection<Point>} grid of points
# @example
# var extent = [-70.823364, -33.553984, -70.473175, -33.302986];
# var cellSize = 3;
# var units = 'miles';
#
# var grid = turf.pointGrid(extent, cellSize, units);
#
# //=grid
def point_grid(bbox, cellSize, units):
    fc = FeatureCollection([])
    x_fraction = cellSize / distance(Point((bbox[0], bbox[1])),
                                     Point((bbox[2], bbox[1])), units)
    cell_width = x_fraction * (bbox[2] - bbox[0])
    y_fraction = cellSize / distance(Point((bbox[0], bbox[1])),
                                     Point((bbox[0], bbox[3])), units)
    cell_height = y_fraction * (bbox[3] - bbox[1])

    current_x = bbox[0]
    while current_x <= bbox[2]:
        current_y = bbox[1]
        while current_y <= bbox[3]:
            fc["features"].append(Point((current_x, current_y)))

            current_y += cell_height
        current_x += cell_width

    return fc
