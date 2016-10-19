from packages import inside
from geojson import FeatureCollection

# Takes a set of {@link Point|points} and a set of {@link Polygon|polygons}
#   and returns the points that fall within the polygons.
#
# @name within
# @param {FeatureCollection<Point>} points inside points
# @param {FeatureCollection<Polygon>} polygons inside polygons
# @return {FeatureCollection<Point>} points that land within at least
#   one polygon
# @example
# var searchWithin = {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [[
#           [-46.653,-23.543],
#           [-46.634,-23.5346],
#           [-46.613,-23.543],
#           [-46.614,-23.559],
#           [-46.631,-23.567],
#           [-46.653,-23.560],
#           [-46.653,-23.543]
#         ]]
#       }
#     }
#   ]
# };
# var points = {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-46.6318, -23.5523]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-46.6246, -23.5325]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-46.6062, -23.5513]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-46.663, -23.554]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-46.643, -23.557]
#       }
#     }
#   ]
# };
#
# var ptsWithin = turf.within(points, searchWithin);
#
# //=points
#
# //=searchWithin
#
# //=ptsWithin
#
def within (points, polygons):
    points_within = FeatureCollection([])
    for i in range(len(polygons["features"])):
        for j in range(len(points.features)):
            is_inside = inside(points.features[j], polygons.features[i])
            if is_inside:
                points_within["features"].push(points.features[j])
    return points_within