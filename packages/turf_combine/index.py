from packages.turf_meta import feature_each
from geojson import FeatureCollection

# Combines a {@link FeatureCollection} of {@link Point},
# {@link LineString}, or {@link Polygon} features
# into {@link MultiPoint}, {@link MultiLineString}, or
# {@link MultiPolygon} features.
#
# @name combine
# @param {FeatureCollection<(Point|LineString|Polygon)>} fc a FeatureCollection
#    of any type
# @return {FeatureCollection<(MultiPoint|MultiLineString|MultiPolygon)>}
#   a FeatureCollection of corresponding type to input
# @example
# var fc = {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [19.026432, 47.49134]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [19.074497, 47.509548]
#       }
#     }
#   ]
# };
#
# var combined = turf.combine(fc);
#
# //=combined

def combine (feature_collection):
    groups = {
        "MultiPoint":       {"coordinates": [], "properties": []},
        "MultiLineString":  {"coordinates": [], "properties": []},
        "MultiPolygon":     {"coordinates": [], "properties": []}
    }

    def multi_mapping_reduce_function(memo, item):
        memo[item.replace('Multi', '')] = item
        return memo
    multi_mapping = reduce(multi_mapping_reduce_function, groups.keys())

    def add_to_group(feature, key, multi):
        if not multi:
            groups[key]["coordinates"].append(
                feature["geometry"]["coordinates"]
            )
        else:
            groups[key]["coordinates"] = groups[key]["coordinates"] + \
                                         feature["geometry"]["coordinates"]
        groups[key]["properties"].append(feature["properties"])

    def callback(feature):
        if not feature["geometry"]:
            return
        if groups[feature["geometry"]["type"]]:
            add_to_group(feature, feature["geometry"]["type"], True)
        elif multi_mapping[feature["geometry"]["type"]]:
            add_to_group(feature, multi_mapping[feature["geometry"]["type"]],
                         False)
    feature_each(feature_collection, callback)

    return FeatureCollection(
        map(
            lambda key: {
                "type": "Feature",
                "properties": {
                    "collectedProperties": groups[key]["properties"]
                },
                "geometry": {
                    "type": key,
                    "coordinates": groups[key]["coordinates"]
                }
            },
            sorted(
                filter(
                    lambda key: len(groups[key]["coordinates"]),
                    groups.keys()
                )
            )
        )
    )
