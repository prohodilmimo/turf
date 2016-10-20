from geojson import GeoJSON, Feature, FeatureCollection
from numbers import Number


def get_coord(obj):
    # type: (Any) -> list[Number]
    """
    Unwrap a coordinate from a Feature with a Point geometry, a Point geometry,
        or a single coordinate.

    :type   obj:    Any
    :param  obj:    any value
    :rtype:         list[Number]
    :return:        a coordinate
    """
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


def assert_geojson_type(value, geojson_type, name):
    # type: (GeoJSON, str, str) -> None
    """
    Enforce expectations about types of GeoJSON objects for Turf

    :type   value:          GeoJSON
    :param  value:          value any GeoJSON object
    :type   geojson_type:   str
    :param  geojson_type:   type expected GeoJSON type
    :type   name:           str
    :param  name:           name name of calling function
    :raises ValueError:     if input is unspecified or if assertion has failed
    """
    if not geojson_type or not name:
        raise ValueError("type and name required")

    if not value or value["type"] != geojson_type:
        raise ValueError("Invalid inside to {0}: must be a {1}, given {2}"
                         .format(name, geojson_type, value["type"]))


def feature_of(feature, geojson_type, name):
    # type: (Feature, str, str) -> None
    """
    Enforce expectations about types of {@link Feature} inputs for Turf.
    Internally this uses {@link geojsonType} to judge geometry types.

    :type   feature:        Feature
    :param  feature:        feature a feature with an expected geometry type
    :type   geojson_type:   str
    :param  geojson_type:   expected GeoJSON type
    :type   name:           str
    :param  name:           name of calling function
    :raises ValueError:     if value is not the expected type
    """
    if not name:
        raise ValueError(".featureOf() requires a name")

    if not feature or feature["type"] != "Feature" or not feature["geometry"]:
        raise ValueError(
            "Invalid inside to {0}, Feature with geometry required"
            .format(name)
        )

    if "geometry" not in feature or \
       feature["geometry"]["type"] != geojson_type:
        raise ValueError(
            "Invalid inside to {0}: must be a {1}, given {2}"
            .format(name, geojson_type, feature["geometry"]["type"])
        )


def collection_of(feature_collection, geojson_type, name):
    # type: (FeatureCollection, str, str) -> None
    """
    Enforce expectations about types of {@link FeatureCollection}
        inputs for Turf.
    Internally this uses {@link geojsonType} to judge geometry types.

    :type   feature_collection: FeatureCollection
    :param  feature_collection: a FeatureCollection for which features
                                will be judged
    :type   geojson_type:       str
    :param  geojson_type:       expected GeoJSON type
    :type   name:               str
    :param  name:               name of calling function
    :raises ValueError:         if value is not the expected type
    """
    if not name:
        raise ValueError(".collectionOf() requires a name")

    if not feature_collection or \
       feature_collection["type"] != "FeatureCollection":
        raise ValueError(
            "Invalid inside to {0}, FeatureCollection required"
            .format(name)
        )

    for i in range(len(feature_collection["features"])):
        feature = feature_collection.features[i]

        if not feature or feature["type"] != "Feature" or \
           not feature["geometry"]:
            raise ValueError(
                "Invalid inside to {0}, Feature with geometry required"
                .format(name)
            )

        if "geometry" not in feature or \
           feature["geometry"]["type"] != geojson_type:
            raise ValueError(
                "Invalid inside to {0}: must be a {1}, given {2}"
                .format(name, geojson_type, feature["geometry"]["type"])
            )


__all__ = [
    "assert_geojson_type",
    "collection_of",
    "feature_of",
    "get_coord"
]
