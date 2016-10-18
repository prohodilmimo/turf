from packages import inside
import json

# Takes a set of {@link Point|points} and a set of {@link Polygon|polygons}
#   and performs a spatial join.
#
# @name tag
# @param {FeatureCollection<Point>} points input points
# @param {FeatureCollection<Polygon>} polygons input polygons
# @param {string} field property in `polygons` to add to joined {<Point>}
#    features
# @param {string} outField property in `points` in which to store
#   joined property from `polygons`
# @return {FeatureCollection<Point>} points with `containingPolyId`
#   property containing values from `polyId`
# @example
# var pt1 = point([-77, 44]);
# var pt2 = point([-77, 38]);
# var poly1 = polygon([[
#   [-81, 41],
#   [-81, 47],
#   [-72, 47],
#   [-72, 41],
#   [-81, 41]
# ]], {pop: 3000});
# var poly2 = polygon([[
#   [-81, 35],
#   [-81, 41],
#   [-72, 41],
#   [-72, 35],
#   [-81, 35]
# ]], {pop: 1000});
#
# var points = featureCollection([pt1, pt2]);
# var polygons = featureCollection([poly1, poly2]);
#
# var tagged = turf.tag(points, polygons,
#                       'pop', 'population');
#
# //=tagged
#
def tag(points, polygons, field, out_field):
    # prevent mutations
    points = json.loads(json.dumps(points))
    polygons = json.loads(json.dumps(polygons))
    for pt in points["features"]:
        if not pt.properties:
            pt.properties = {}

        for poly in polygons["features"]:
            if pt.properties[out_field] is None:
                is_inside = inside(pt, poly)
                if is_inside:
                    pt.properties[out_field] = poly.properties[field]
    return points
