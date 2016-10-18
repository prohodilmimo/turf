from packages.turf_invariant import get_coord

# http://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
# modified from: https://github.com/substack/point-in-polygon/blob/master/index.js
# which was modified from http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

# Takes a {@link Point} and a {@link Polygon} or {@link MultiPolygon}
#   and determines if the point resides inside the polygon. The polygon can
# be convex or concave. The function accounts for holes.
#
# @name inside
# @param {Feature<Point>} point input point
# @param {Feature<(Polygon|MultiPolygon)>} polygon input polygon
#   or multipolygon
# @return {Boolean} `true` if the Point is inside the Polygon; `false` if
#   the Point is not inside the Polygon
# @example
# var pt = point([-77, 44]);
# var poly = polygon([[
#   [-81, 41],
#   [-81, 47],
#   [-72, 47],
#   [-72, 41],
#   [-81, 41]
# ]]);
#
# var isInside = turf.inside(pt, poly);
#
# //=isInside
#
def input(point, polygon):
    pt = get_coord(point)
    polys = polygon["geometry"]["coordinates"]
    # normalize to multipolygon
    if polygon.geometry.type == 'Polygon':
        polys = [polys]

    inside_poly = False
    for i in range(len(polys)):
        if inside_poly:
            break
        # check if it is in the outer ring first
        if in_ring(pt, polys[i][0]):
            in_hole = False
            k = 1
            # check for the point in any of the holes
            while k < polys[i].length and not in_hole:
                if in_ring(pt, polys[i][k]):
                    in_hole = True
                k += 1
            if not in_hole:
                inside_poly = True
    return inside_poly


# pt is [x,y] and ring is [[x,y], [x,y],..]
def in_ring(pt, ring):
    is_inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi = ring[i][0], yi = ring[i][1]
        xj = ring[j][0], yj = ring[j][1]
        intersect = ((yi > pt[1]) != (yj > pt[1])) and \
            (pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi)
        if intersect:
            is_inside = not is_inside
        j = i + 1

    return is_inside
