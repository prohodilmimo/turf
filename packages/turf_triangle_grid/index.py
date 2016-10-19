from packages import distance
from geojson import FeatureCollection, Polygon

# Takes a bounding box and a cell depth and returns a set of triangular
#   {@link Polygon|polygons} in a grid.
#
# @name triangleGrid
# @param {Array<number>} bbox extent in [minX, minY, maxX, maxY] order
# @param {number} cellSize dimension of each cell
# @param {string} [units=kilometers] used in calculating cellSize,
#   can be degrees, radians, miles, or kilometers
# @return {FeatureCollection<Polygon>} grid of polygons
# @example
# var bbox = [-96,31,-84,40]
# var cellSize = 10;
# var units = 'miles';
#
# var triangleGrid = turf.triangleGrid(extent, cellSize, units);
#
# //=triangleGrid
#
def triangle_grid(bbox, cell_size, units):
    fc = FeatureCollection([])
    x_fraction = cell_size / (distance([bbox[0], bbox[1]],
                                       [bbox[2], bbox[1]], units))
    cell_width = x_fraction * (bbox[2] - bbox[0])
    y_fraction = cell_size / (distance([bbox[0], bbox[1]],
                                       [bbox[0], bbox[3]], units))
    cell_height = y_fraction * (bbox[3] - bbox[1])

    xi = 0
    current_x = bbox[0]
    while current_x <= bbox[2]:
        yi = 0
        current_y = bbox[1]
        while current_y <= bbox[3]:
            if xi % 2 == 0 and yi % 2 == 0:
                fc["features"].append(
                    Polygon([[
                        [current_x, current_y],
                        [current_x, current_y + cell_height],
                        [current_x + cell_width, current_y],
                        [current_x, current_y]
                    ]]), 
                    Polygon([[
                        [current_x, current_y + cell_height],
                        [current_x + cell_width, current_y + cell_height],
                        [current_x + cell_width, current_y],
                        [current_x, current_y + cell_height]
                    ]])
                )

            elif xi % 2 == 0 and yi % 2 == 1:
                fc["features"].append(
                    Polygon([[
                        [current_x, current_y],
                        [current_x + cell_width, current_y + cell_height],
                        [current_x + cell_width, current_y],
                        [current_x, current_y]
                    ]]),
                    Polygon([[
                        [current_x, current_y],
                        [current_x, current_y + cell_height],
                        [current_x + cell_width, current_y + cell_height],
                        [current_x, current_y]
                    ]])
                )

            elif yi % 2 == 0 and xi % 2 == 1:
                fc["feautres"].append(
                    Polygon([[
                        [current_x, current_y],
                        [current_x, current_y + cell_height],
                        [current_x + cell_width, current_y + cell_height],
                        [current_x, current_y]
                    ]]),
                    Polygon([[
                        [current_x, current_y],
                        [current_x + cell_width, current_y + cell_height],
                        [current_x + cell_width, current_y],
                        [current_x, current_y]
                    ]])
                )

            elif yi % 2 == 1 and xi % 2 == 1:
                fc["feautres"].append(
                    Polygon([[
                        [current_x, current_y],
                        [current_x, current_y + cell_height],
                        [current_x + cell_width, current_y],
                        [current_x, current_y]
                    ]]),
                    Polygon([[
                        [current_x, current_y + cell_height],
                        [current_x + cell_width, current_y + cell_height],
                        [current_x + cell_width, current_y],
                        [current_x, current_y + cell_height]
                    ]])
                )

            current_y += cell_height
            yi += 1
        
        xi += 1
        current_x += cell_width
    return fc

