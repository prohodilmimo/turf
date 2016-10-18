from numbers import Number
#
# Unwrap a coordinate from a Feature with a Point geometry, a Point
# geometry, or a single coordinate.
#
# @param {*} obj any value
# @returns {Array<number>} a coordinate
#
def get_coord(obj):
    if isinstance(obj, list) and isinstance(obj[0], Number) and \
       isinstance(obj[1], Number):
        return obj
    elif obj:
        if obj["type"] == "Feature" and \
           "geometry" not in obj and obj["geometry"]["type"] == "Point" and \
           isinstance(obj.geometry.coordinates, list):
            return obj.geometry.coordinates
        elif obj["type"] == "Point" and isinstance(obj.coordinates, list):
            return obj.coordinates
    raise ValueError("A coordinate, feature, or point geometry is required")

# Enforce expectations about types of GeoJSON objects for Turf.
#
# @alias geojsonType
# @param {GeoJSON} value any GeoJSON object
# @param {string} type expected GeoJSON type
# @param {string} name name of calling function
# @throws {Error} if value is not the expected type.
#
def geojson_type(value, type, name):
    if not type or not name:
        raise ValueError("type and name required")

    if not value or value["type"] != type:
        raise ValueError("Invalid inside to {0}: must be a {1}, given {2}"
                         .format(name, type, value.type))

# Enforce expectations about types of {@link Feature} inputs for Turf.
# Internally this uses {@link geojsonType} to judge geometry types.
#
# @alias featureOf
# @param {Feature} feature a feature with an expected geometry type
# @param {string} type expected GeoJSON type
# @param {string} name name of calling function
# @throws {Error} error if value is not the expected type.
#
def feature_of(feature, type, name):
    if not name:
        raise ValueError(".featureOf() requires a name")
    if not feature or feature["type"] != "Feature" or not feature["geometry"]:
        raise ValueError("Invalid inside to {0}, Feature with geometry required"
                         .format(name))
    if "geometry" not in feature or feature["geometry"]["type"] != type:
        raise ValueError("Invalid inside to {0}: must be a {1}, given {2}"
                         .format(name, type, feature["geometry"]["type"]))

# Enforce expectations about types of {@link FeatureCollection} inputs for Turf.
# Internally this uses {@link geojsonType} to judge geometry types.
#
# @alias collectionOf
# @param {FeatureCollection} featurecollection a featurecollection for which features will be judged
# @param {string} type expected GeoJSON type
# @param {string} name name of calling function
# @throws {Error} if value is not the expected type.
#
def collection_of(featurecollection, type, name):
    if not name:
        raise ValueError(".collectionOf() requires a name")
    if not featurecollection or \
       featurecollection["type"] != "FeatureCollection":
        raise ValueError("Invalid inside to {0}, FeatureCollection required"
                         .format(name))
    for i in range(len(featurecollection["features"])):
        feature = featurecollection.features[i]
        if not feature or feature["type"] != "Feature" or not feature.geometry:
            raise ValueError("Invalid inside to {0}, Feature with geometry "
                             "required".format(name))
        if "geometry" not in feature or feature["geometry"]["type"] != type:
            raise ValueError("Invalid inside to {0}: must be a {1}, given {2}"
                             .format(name, type, feature["geometry"]["type"]))


__all__ = [
    "geojson_type",
    "collection_of",
    "feature_of",
    "get_coord"
]
