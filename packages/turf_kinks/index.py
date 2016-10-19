# Takes a {@link Polygon|polygon} and returns {@link Point|points} at all self-intersections.
#
# @name kinks
# @param {Feature<Polygon>|Polygon} polygon input polygon
# @returns {FeatureCollection<Point>} self-intersections
# @example
# var poly = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Polygon",
#     "coordinates": [[
#       [-12.034835, 8.901183],
#       [-12.060413, 8.899826],
#       [-12.03638, 8.873199],
#       [-12.059383, 8.871418],
#       [-12.034835, 8.901183]
#     ]]
#   }
# };
#
# var kinks = turf.kinks(poly);
#
# var resultFeatures = kinks.intersections.features.concat(poly);
# var result = {
#   "type": "FeatureCollection",
#   "features": resultFeatures
# };
#
# //=result

from geojson import Point, FeatureCollection

def kinks(poly_in):
    results = FeatureCollection([])
    if poly_in["type"] == 'Feature':
        poly = poly_in["geometry"]
    else:
        poly = poly_in

    for ring1 in poly["coordinates"]:
        for ring2 in poly["coordinates"]:
            for i in range(len(ring1) - 1):
                for k in range(len(ring2) - 1):
                    # don't check adjacent sides of a given ring,
                    #  since of course they intersect in a vertex.
                    if ring1 == ring2 and \
                       (abs(i - k) == 1 or abs(i - k) == len(ring1) - 2):
                        continue

                    intersection = line_intersects(
                        ring1[i][0], ring1[i][1],
                        ring1[i + 1][0], ring1[i + 1][1],
                        ring2[k][0], ring2[k][1], ring2[k + 1][0],
                        ring2[k + 1][1])
                    if intersection:
                        results["features"].append(Point((intersection[0],
                                                          intersection[1])))
    return results


# modified from http://jsfiddle.net/justin_c_rounds/Gd2S2/light/
def line_intersects(line1_start_x, line1_start_y, line1_end_x, line1_end_y,
                    line2_start_x, line2_start_y, line2_end_x, line2_end_y):
    # if the lines intersect, the result contains the x and y
    # of the intersection (treating the lines as infinite) and booleans for
    # whether line segment 1 or line segment 2 contain the point
    result = {"x": None, "y": None, "onLine1": False, "onLine2": False}
    denominator = ((line2_end_y - line2_start_y) *
                   (line1_end_x - line1_start_x)) - \
                  ((line2_end_x - line2_start_x) *
                   (line1_end_y - line1_start_y))
    if denominator == 0:
        if result["x"] is not None and result["y"] is not None:
            return result
        else:
            return False
    a = line1_start_y - line2_start_y
    b = line1_start_x - line2_start_x
    numerator1 = ((line2_end_x - line2_start_x) * a) -\
                 ((line2_end_y - line2_start_y) * b)
    numerator2 = ((line1_end_x - line1_start_x) * a) -\
                 ((line1_end_y - line1_start_y) * b)
    a = numerator1 / denominator
    b = numerator2 / denominator

    # if we cast these lines infinitely in both directions,
    #   they intersect here:
    result["x"] = line1_start_x + (a * (line1_end_x - line1_start_x))
    result["y"] = line1_start_y + (a * (line1_end_y - line1_start_y))

    # if line1 is a segment and line2 is infinite, they intersect if:
    if 0 <= a <= 1:
        result["onLine1"] = True
    # if line2 is a segment and line1 is infinite, they intersect if:
    if 0 <= b <= 1:
        result["onLine2"] = True
    # if line1 and line2 are segments, they intersect if
    #   both of the above are true
    if result["onLine1"] and result["onLine2"]:
        return [result["x"], result["y"]]
    else:
        return False
