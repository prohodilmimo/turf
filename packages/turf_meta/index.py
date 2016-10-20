from geojson import GeoJSON
from numbers import Number


def coord_each(layer, callback, exclude_wrap_coord=False):
    # type: (GeoJSON, FunctionType, bool) -> None
    """
    Iterate over coordinates in any GeoJSON object, similar to Array.forEach

    :type   layer:              GeoJSON
    :param  layer:              any GeoJSON object
    :type   callback:           FunctionType
    :param  callback:           a method that takes (value)
    :type   exclude_wrap_coord: bool
    :param  exclude_wrap_coord: whether or not to include the final coordinate
                                of LinearRings that wraps the ring in
                                its iteration

    @example
    var point = { type: 'Point', coordinates: [0, 0] };
    coord_each(point, function(coords) {
      // coords is equal to [0, 0]
    });
    """
    is_feature_collection = layer["type"] == 'FeatureCollection'
    is_feature = layer["type"] == 'Feature'
    stop = len(layer["features"]) if is_feature_collection else 1

    # This logic may look a little weird. The reason why it is that way
    # is because it's trying to be fast. GeoJSON supports multiple kinds
    # of objects at its root: FeatureCollection, Features, Geometries.
    # This function has the responsibility of handling all of them, and that
    # means that some of the `for` loops you see below actually
    # just don't apply to certain inputs.
    # For instance, if you give this just a Point geometry, then both loops are
    # short-circuited and all we do is gradually rename the input until
    # it's called 'geometry'.
    #
    # This also aims to allocate as few resources as possible: just a
    # few numbers and booleans, rather than any temporary arrays as would
    # be required with the normalization approach.
    for i in range(stop):
        geometry_maybe_collection = \
            layer["features"][i]["geometry"] if is_feature_collection else \
            layer["geometry"] if is_feature else \
            layer

        is_geometry_collection = \
            geometry_maybe_collection["type"] == "GeometryCollection"

        stop_g = len(geometry_maybe_collection["geometries"]) \
            if is_geometry_collection else 1

        for g in range(stop_g):
            geometry = geometry_maybe_collection["geometries"][g] \
                if is_geometry_collection else geometry_maybe_collection
            coords = geometry["coordinates"]

            wrap_shrink = 1 if (exclude_wrap_coord and
                                (geometry["type"] == "Polygon" or
                                 geometry["type"] == "MultiPolygon")) else 0

            if geometry["type"] == "Point":
                callback(coords)

            elif geometry["type"] in ["LineString", "MultiPoint"]:
                for coord_pair in coords:
                    callback(coord_pair)

            elif geometry["type"] in ["Polygon", "MultiLineString"]:
                for shape in coords:
                    for k in range(len(shape) - wrap_shrink):
                        callback(shape[k])

            elif geometry["type"] == "MultiPolygon":
                for polygon in coords:
                    for shape in polygon:
                        for l in range(len(shape) - wrap_shrink):
                            callback(shape[l])

            elif geometry["type"] == "GeometryCollection":
                for geometry_ in geometry["geometries"]:
                    coord_each(geometry_, callback, exclude_wrap_coord)

            else:
                raise ValueError("Unknown Geometry Type")


def coord_reduce(layer, callback, memo, exclude_wrap_coord):
    # type: (GeoJSON, FunctionType, Any, bool) -> Any
    """
    Reduce coordinates in any GeoJSON object into a single value,
        similar to how Array.reduce works.
    However, in this case we lazily run the reduction, so an array of
        all coordinates is unnecessary.

    :type   layer:              GeoJSON
    :param  layer:              any GeoJSON object
    :type   callback:           FunctionType
    :param  callback:           a method that takes (memo, value) and
                                returns a new memo
    :type   memo:               *
    :param  memo:               the starting value of memo: can be any type
    :type   exclude_wrap_coord: bool
    :param  exclude_wrap_coord: whether or not to include the final coordinate
                                of LinearRings that wraps the ring in
                                its iteration
    :rtype:                     *
    :return:                    combined value
    """
    local_vars = {"memo": memo}

    def callback_wrapper(coord):
        local_vars["memo"] = callback(local_vars["memo"], coord)

    coord_each(layer, callback_wrapper, exclude_wrap_coord)

    return local_vars["memo"]


def prop_each(layer, callback):
    # type: (GeoJSON, FunctionType) -> None
    """
    Iterate over property objects in any GeoJSON object,
        similar to Array.forEach

    :type   layer:      GeoJSON
    :param  layer:      any GeoJSON object
    :type   callback:   FunctionType
    :param  callback:   a method that takes (value)

    @example
    var point = { type: 'Feature', geometry: null, properties: { foo: 1 } };
    prop_each(point, function(props) {
      // props is equal to { foo: 1}
    });
    """
    if layer["type"] == 'FeatureCollection':
        for feature in layer["features"]:
            callback(feature["properties"])

    elif layer["type"] == 'Feature':
        callback(layer["properties"])


def prop_reduce(layer, callback, memo):
    # type: (GeoJSON, FunctionType, Any) -> Any
    """
    Reduce properties in any GeoJSON object into a single value,
        similar to how Array.reduce works.
    However, in this case we lazily run the reduction,
        so an array of all properties is unnecessary.

    :type   layer:      GeoJSON
    :param  layer:      any GeoJSON object
    :type   callback:   FunctionType
    :param  callback:   a method that takes (memo, coord) and returns
                        a new memo
    :type   memo:       Any
    :param  memo:       the starting value of memo: can be any type
    :rtype:             Any
    :return:            combined value

    @example
    // an example of an even more advanced function that gives you the
    // javascript type of each property of every feature
    function propTypes (layer) {
      opts = opts || {}
      return prop_reduce(layer, function (prev, props) {
        for (var prop in props) {
          if (prev[prop]) continue
          prev[prop] = typeof props[prop]
        }
      }, {})
    }
    """
    local_vars = {"memo": memo}

    def callback_wrapper(prop):
        local_vars["memo"] = callback(local_vars["memo"], prop)

    prop_each(layer, callback_wrapper)

    return local_vars["memo"]


def feature_each(layer, callback):
    # type: (GeoJSON, FunctionType) -> None
    """
    Iterate over features in any GeoJSON object, similar to Array.forEach

    :type   layer:      GeoJSON
    :param  layer:      any GeoJSON object
    :type   callback:   FunctionType
    :param  callback:   a method that takes (value)

    @example
    var feature = { type: 'Feature', geometry: null, properties: {} };
    feature_each(feature, function(feature) {
      // feature == feature
    });
    """
    if layer["type"] == 'Feature':
        callback(layer)

    elif layer["type"] == 'FeatureCollection':
        for feature in layer["features"]:
            callback(feature)


def coord_all(layer):
    # type: (GeoJSON) -> list[list[Number]]
    """
    Get all coordinates from any GeoJSON object,
        returning an array of coordinate arrays

    :type   layer:  GeoJSON
    :param  layer:  any GeoJSON object
    :rtype:         list[list[Number]]
    :return:        coordinate position array
    """
    coords = []

    coord_each(layer, lambda coord: coords.append(coord))

    return coords


__all__ = [
    "coord_each",
    "feature_each"
]
