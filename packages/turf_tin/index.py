# http://en.wikipedia.org/wiki/Delaunay_triangulation
# https://github.com/ironwallaby/delaunay
from geojson import FeatureCollection, Polygon

# Takes a set of {@link Point|points} and the name of a z-value property and
# creates a [Triangulated Irregular Network](http://en.wikipedia.org/wiki/Triangulated_irregular_network),
# or a TIN for short, returned as a collection of Polygons. These are often used
# for developing elevation contour maps or stepped heat visualizations.
#
# This triangulates the points, as well as adds properties called `a`, `b`,
# and `c` representing the value of the given `propertyName` at each of
# the points that represent the corners of the triangle.
#
# @name tin
# @param {FeatureCollection<Point>} points input points
# @param {String=} z name of the property from which to pull z values
# This is optional: if not given, then there will be no extra data added to the derived triangles.
# @return {FeatureCollection<Polygon>} TIN output
#
# @example
# // generate some random point data
# var points = turf.random('points', 30, {
#   bbox: [50, 30, 70, 50]
# });
# //=points
#
# // add a random property to each point between 0 and 9
# for (var i = 0; i < points.features.length; i++) {
#   points.features[i].properties.z = ~~(Math.random() * 9);
# }
#
# var tin = turf.tin(points, 'z')
#
# for (var i = 0; i < tin.features.length; i++) {
#   var properties  = tin.features[i].properties;
#   // roughly turn the properties of each
#   // triangle into a fill color
#   // so we can visualize the result
#   properties.fill = '#' + properties.a +
#     properties.b + properties.c;
# }
# //=tin
#
def tin (points, z):
    # (dict, str) -> FeatureCollection
    def mapping1(p):
        point = {
            "x": p["geometry"]["coordinates"][0],
            "y": p["geometry"]["coordinates"][1]
        }
        if z:
            point["z"] = p["properties"][z]
        return point

    def mapping2(triangle):
        return Polygon(([
            [triangle.a["x"], triangle.a["y"]],
            [triangle.b["x"], triangle.b["y"]],
            [triangle.c["x"], triangle.c["y"]],
            [triangle.a["x"], triangle.a["y"]]
        ],), None, {
            "a": triangle.a["z"],
            "b": triangle.b["z"],
            "c": triangle.c["z"]
        })
    # break down points
    return FeatureCollection(
        map(mapping2, triangulate(map(mapping1, points["features"])))
    )

class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        aa = b["x"] - a["x"]
        bb = b["y"] - a["y"]
        cc = c["x"] - a["x"]
        dd = c["y"] - a["y"]
        ee = aa * (a["x"] + b["x"]) + bb * (a["y"] + b["y"])
        ff = cc * (a["x"] + c["x"]) + dd * (a["y"] + c["y"])
        gg = 2 * (aa * (c["y"] - b["y"]) - bb * (c["x"] - b["x"]))

        # If the points of the triangle are collinear, then just find the
        # extremes and use the midpoint as the center of the circumcircle.
        self.x = (dd * ee - bb * ff) / gg
        self.y = (aa * ff - cc * ee) / gg
        dx = self.x - a["x"]
        dy = self.y - a["y"]
        self.r = dx * dx + dy * dy


def dedup(edges):
    j = len(edges)

    flag = False
    while j:
        j -= 1
        b = edges[j]
        j -= 1
        a = edges[j]
        i = j
        while i:
            i -= 1
            n = edges[i]
            i -= 1
            m = edges[i]
            if (a == m and b == n) or (a == n and b == m):
                edges.splice(j, 2)
                edges.splice(i, 2)
                j -= 2
                flag = True
            if flag:
                break
        if flag:
            continue

def triangulate(vertices):
    # Bail if there aren't enough vertices to form any triangles.
    if len(vertices) < 3:
        return []

    # Ensure the vertex array is in order of descending X coordinate
    # (which is needed to ensure a subquadratic runtime), and then find
    # the bounding box around the points.
    vertices.sort(lambda (v1, v2): v2["x"] - v1["x"])

    i = len(vertices) - 1
    xmin = vertices[i]["x"]
    xmax = vertices[0]["x"]
    ymin = vertices[i]["y"]
    ymax = ymin
    epsilon = 1e-12


    while i:
        i -= 1
        if vertices[i]["y"] < ymin:
            ymin = vertices[i]["y"]
        if vertices[i]["y"] > ymax:
            ymax = vertices[i]["y"]

    # Find a supertriangle, which is a triangle that surrounds all the
    # vertices. This is used like something of a sentinel value to remove
    # cases in the main algorithm, and is removed before we return any results.

    # Once found, put it in the "open" list. (The "open" list is for
    # triangles who may still need to be considered; the "closed" list is
    # for triangles which do not.)
    dx = xmax - xmin
    dy = ymax - ymin
    d_max = dx if (dx > dy) else dy
    x_mid = (xmax + xmin) * 0.5
    y_mid = (ymax + ymin) * 0.5
    open_set = [
        Triangle({"x": x_mid - 20 * d_max,  "y": y_mid - d_max,
                  "__sentinel": True},
                 {"x": x_mid,               "y": y_mid + 20 * d_max,
                  "__sentinel": True},
                 {"x": x_mid + 20 * d_max,  "y": y_mid - d_max,
                  "__sentinel": True})
    ]
    closed_set = []

    # Incrementally add each vertex to the mesh.
    i = len(vertices)
    while i:
        i -= 1
        # For each open triangle, check to see if the current point is
        # inside it's circumcircle. If it is, remove the triangle and add
        # it's edges to an edge list.
        edges = []
        j = len(open_set)
        while j:
            j -= 1
            # If this point is to the right of this triangle's circumcircle,
            # then this triangle should never get checked again. Remove it
            # from the open list, add it to the closed list, and skip.
            dx = vertices[i].x - open_set[j].x
            if dx > 0 and dx * dx > open_set[j].r:
                closed_set.append(open_set[j])
                open_set.pop(j)
                continue

            # If not, skip this triangle.
            dy = vertices[i]["y"] - open_set[j].y
            if dx * dx + dy * dy > open_set[j].r:
                continue

            # Remove the triangle and add it's edges to the edge list.
            edges += [
                open_set[j].a, open_set[j].b,
                open_set[j].b, open_set[j].c,
                open_set[j].c, open_set[j].a
            ]
            open_set.pop(j)

        # Remove any doubled edges.
        dedup(edges)

        # Add a new triangle for each edge.
        j = len(edges)
        while j:
            j -= 1
            b = edges[j]
            j -= 1
            a = edges[j]
            c = vertices[i]
            # Avoid adding colinear triangles
            #   (which have error-prone circumcircles)
            aa = b["x"] - a["x"]
            bb = b["y"] - a["y"]
            gg = 2 * (aa * (c["y"] - b["y"]) - bb * (c["x"] - b["x"]))
            if abs(gg) > epsilon:
                open_set.append(Triangle(a, b, c))

    # Copy any remaining open triangles to the closed list, and then
    # remove any triangles that share a vertex with the supertriangle.
    for triangle in open_set:
        closed_set.append(triangle)

    i = len(closed_set)
    while i:
        i -= 1
        if closed_set[i].a["__sentinel"] or \
           closed_set[i].b["__sentinel"] or \
           closed_set[i].c["__sentinel"]:
            closed_set.pop(i)

    return closed_set
