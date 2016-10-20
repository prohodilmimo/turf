from packages.turf_meta import coord_each
from geojson import Feature, Point

# Takes one or more features and calculates the centroid using
# the mean of all vertices.
# This lessens the effect of small islands and artifacts when calculating
# the centroid of a set of polygons.
#
# @name centroid
# @param {(Feature|FeatureCollection)} features input features
# @return {Feature<Point>} the centroid of the input features
# @example
# var poly = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Polygon",
#     "coordinates": [[
#       [105.818939,21.004714],
#       [105.818939,21.061754],
#       [105.890007,21.061754],
#       [105.890007,21.004714],
#       [105.818939,21.004714]
#     ]]
#   }
# };
#
# var centroidPt = turf.centroid(poly);
#
# var result = {
#   "type": "FeatureCollection",
#   "features": [poly, centroidPt]
# };
#
# //=result
def centroid(features):
    local_vars = {
        "x_sum": 0,
        "y_sum": 0,
        "length": 0
    }

    def callback(coord):
        local_vars["x_sum"] += coord[0]
        local_vars["y_sum"] += coord[1]
        local_vars["length"] += 1

    coord_each(features, callback, True)
    return Feature(Point((local_vars["x_sum"] / local_vars["length"],
                          local_vars["y_sum"] / local_vars["length"])))
