from geojson import FeatureCollection, Point, Polygon
from packages import distance

# Takes a bounding box and a cell depth and returns a set of square
#   {@link Polygon|polygons} in a grid.
#
# @name squareGrid
# @param {Array<number>} bbox extent in [minX, minY, maxX, maxY] order
# @param {number} cellSize width of each cell
# @param {string} [units=kilometers] used in calculating cellSize,
#   can be degrees, radians, miles, or kilometers
# @return {FeatureCollection<Polygon>} grid a grid of polygons
# @example
# var bbox = [-96,31,-84,40];
# var cellSize = 10;
# var units = 'miles';
#
# var squareGrid = turf.squareGrid(bbox, cellSize, units);
#
# //=squareGrid
def square_grid(bbox, cell_size, units):
    fc = FeatureCollection([])
    x_fraction = cell_size / distance(Point((bbox[0], bbox[1])),
                                      Point((bbox[2], bbox[1])), units)
    cell_width = x_fraction * (bbox[2] - bbox[0])
    y_fraction = cell_size / distance(Point((bbox[0], bbox[1])),
                                      Point((bbox[0], bbox[3])), units)
    cell_height = y_fraction * (bbox[3] - bbox[1])

    current_x = bbox[0]
    while current_x <= bbox[2]:
        current_y = bbox[1]
        while current_y <= bbox[3]:
            cell_poly = Polygon(([
                [current_x, current_y],
                [current_x, current_y + cell_height],
                [current_x + cell_width, current_y + cell_height],
                [current_x + cell_width, current_y],
                [current_x, current_y]
            ],))
            fc["features"].append(cell_poly)

            current_y += cell_height

        current_x += cell_width

    return fc
