from packages import centroid, distance, inside, explode
from geojson import FeatureCollection, Feature
import math

# Takes a feature and returns a {@link Point} guaranteed to be
#   on the surface of the feature.
#
# * Given a {@link Polygon}, the point will be in the area of the polygon
# * Given a {@link LineString}, the point will be along the string
# * Given a {@link Point}, the point will the same as the input
#
# @param {(Feature|FeatureCollection)} fc any feature or set of features
# @returns {Feature} a point on the surface of `input`
# @example
# // create a random polygon
# var polygon = turf.random("polygon");
#
# //=polygon
#
# var pointOnPolygon = turf.pointOnSurface(polygon);
#
# var resultFeatures = polygon.features.concat(pointOnPolygon);
# var result = {
#   "type": "FeatureCollection",
#   "features": resultFeatures
# };
#
# //=result
def pointOnSurface(feature_collection):
    # normalize
    if feature_collection.type != "FeatureCollection":
        if feature_collection.type != "Feature":
            feature_collection = Feature(feature_collection)
        feature_collection = FeatureCollection([feature_collection])

    # get centroid
    cent = centroid(feature_collection)

    # check to see if centroid is on surface
    on_surface = False
    i = 0
    while not on_surface and i < len(feature_collection["features"]):
        geom = feature_collection["features"][i]["geometry"]
        
        on_line = False
        if geom["type"] == "Point":
            if cent["geometry"]["coordinates"][0] == geom["coordinates"][0] and \
               cent["geometry"]["coordinates"][1] == geom["coordinates"][1]:
                on_surface = True
        elif geom["type"] == "MultiPoint":
            on_multi_point = False
            k = 0
            while not on_multi_point and k < len(geom["coordinates"]):
                if cent["geometry"]["coordinates"][0] == geom["coordinates"][k][0] and \
                   cent["geometry"]["coordinates"][1] == geom["coordinates"][k][1]:
                    on_surface = True
                    on_multi_point = True
                k += 1
        elif geom["type"] == "LineString":
            k = 0
            while not on_line and k < len(geom["coordinates"]) - 1:
                x = cent["geometry"]["coordinates"][0]
                y = cent["geometry"]["coordinates"][1]
                x1 = geom["coordinates"][k][0]
                y1 = geom["coordinates"][k][1]
                x2 = geom["coordinates"][k + 1][0]
                y2 = geom["coordinates"][k + 1][1]
                if point_on_segment(x, y, x1, y1, x2, y2):
                    on_line = True
                    on_surface = True
                k += 1
        elif geom["type"] == "MultiLineString":
            j = 0
            while j < len(geom["coordinates"]):
                on_line = False
                k = 0
                line = geom["coordinates"][j]
                while not on_line and k < len(line) - 1:
                    x = cent["geometry"]["coordinates"][0]
                    y = cent["geometry"]["coordinates"][1]
                    x1 = line[k][0]
                    y1 = line[k][1]
                    x2 = line[k + 1][0]
                    y2 = line[k + 1][1]
                    if point_on_segment(x, y, x1, y1, x2, y2):
                        on_line = True
                        on_surface = True
                    k += 1
                j += 1
        elif geom["type"] == "Polygon" or geom["type"] == "MultiPolygon":
            f = Feature(geom)
            if inside(cent, f):
                on_surface = True
        i += 1
    if on_surface:
        return cent
    else:
        vertices = FeatureCollection([])
        for i in range(len(feature_collection["features"])):
            vertices.features = \
                vertices["features"] + \
                explode(feature_collection["features"][i])["features"]
        closest_distance = float("inf")
        for i in range(len(vertices["feautres"])):
            dist = distance(cent, vertices["features"][i], "miles")
            if dist < closest_distance:
                closest_distance = dist
                closest_vertex = vertices.features[i]
        return closest_vertex

def point_on_segment(x, y, x1, y1, x2, y2):
    ab = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    ap = math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
    pb = math.sqrt((x2 - x) * (x2 - x) + (y2 - y) * (y2 - y))
    if ab == ap + pb:
        return True
