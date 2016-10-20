# Iterate over coordinates in any GeoJSON object, similar to
# Array.forEach.
#
# @name coord_each
# @param {Object} layer any GeoJSON object
# @param {Function} callback a method that takes (value)
# @param {boolean=} excludeWrapCoord whether or not to include
# the final coordinate of LinearRings that wraps the ring in its iteration.
# @example
# var point = { type: 'Point', coordinates: [0, 0] };
# coord_each(point, function(coords) {
#   // coords is equal to [0, 0]
# });
def coord_each(layer, callback, exclude_wrap_coord=None):
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
            geometry_maybe_collection["type"] == 'GeometryCollection'
        stop_g = len(geometry_maybe_collection["geometries"]) \
            if is_geometry_collection else 1

        for g in range(stop_g):
            geometry = geometry_maybe_collection["geometries"][g] \
                if is_geometry_collection else geometry_maybe_collection
            coords = geometry["coordinates"]

            wrap_shrink = 1 if (exclude_wrap_coord and
                                (geometry["type"] == 'Polygon' or
                                 geometry["type"] == 'MultiPolygon')) else 0

            if geometry["type"] == 'Point':
                callback(coords)
            elif (geometry["type"] == 'LineString' or
                  geometry["type"] == 'MultiPoint'):
                for j in range(len(coords)):
                    callback(coords[j])
            elif (geometry["type"] == 'Polygon' or
                  geometry["type"] == 'MultiLineString'):
                for j in range(len(coords)):
                    for k in range(len(coords[j]) - wrap_shrink):
                        callback(coords[j][k])
            elif geometry["type"] == 'MultiPolygon':
                for j in range(len(coords)):
                    for k in range(len(coords[j])):
                        for l in range(len(coords[j][k]) - wrap_shrink):
                            callback(coords[j][k][l])
            elif geometry["type"] == 'GeometryCollection':
                for j in range(len(geometry["geometries"])):
                    coord_each(geometry["geometries"][j], callback,
                               exclude_wrap_coord)
            else:
                raise ValueError('Unknown Geometry Type')

# Reduce coordinates in any GeoJSON object into a single value,
# similar to how Array.reduce works. However, in this case we lazily run
# the reduction, so an array of all coordinates is unnecessary.
#
# @name coord_reduce
# @param {Object} layer any GeoJSON object
# @param {Function} callback a method that takes (memo, value) and returns
# a new memo
# @param {*} memo the starting value of memo: can be any type.
# @param {boolean=} excludeWrapCoord whether or not to include
# the final coordinate of LinearRings that wraps the ring in its iteration.
# @returns {*} combined value
def coord_reduce(layer, callback, memo, exclude_wrap_coord):
    local_vars = {"memo": memo}
    def callback_wrapper(coord):
        local_vars["memo"] = callback(local_vars["memo"], coord)
    coord_each(layer, callback_wrapper, exclude_wrap_coord)
    return local_vars["memo"]

# Iterate over property objects in any GeoJSON object, similar to
# Array.forEach.
#
# @name prop_each
# @param {Object} layer any GeoJSON object
# @param {Function} callback a method that takes (value)
# @example
# var point = { type: 'Feature', geometry: null, properties: { foo: 1 } };
# prop_each(point, function(props) {
#   // props is equal to { foo: 1}
# });
def prop_each(layer, callback):
    if layer["type"] == 'FeatureCollection':
        for i in range(len(layer["features"])):
            callback(layer["features"][i]["properties"])
    elif layer["type"] == 'Feature':
        callback(layer["properties"])

# Reduce properties in any GeoJSON object into a single value,
# similar to how Array.reduce works. However, in this case we lazily run
# the reduction, so an array of all properties is unnecessary.
#
# @name prop_reduce
# @param {Object} layer any GeoJSON object
# @param {Function} callback a method that takes (memo, coord) and returns
# a new memo
# @param {*} memo the starting value of memo: can be any type.
# @returns {*} combined value
# @example
# // an example of an even more advanced function that gives you the
# // javascript type of each property of every feature
# function propTypes (layer) {
#   opts = opts || {}
#   return prop_reduce(layer, function (prev, props) {
#     for (var prop in props) {
#       if (prev[prop]) continue
#       prev[prop] = typeof props[prop]
#     }
#   }, {})
# }
def prop_reduce(layer, callback, memo):
    local_vars = {"memo": memo}
    def callback_wrapper(prop):
        local_vars["memo"] = callback(local_vars["memo"], prop)
    prop_each(layer, callback_wrapper)
    return local_vars["memo"]

# Iterate over features in any GeoJSON object, similar to
# Array.forEach.
#
# @name feature_each
# @param {Object} layer any GeoJSON object
# @param {Function} callback a method that takes (value)
# @example
# var feature = { type: 'Feature', geometry: null, properties: {} };
# feature_each(feature, function(feature) {
#   // feature == feature
# });
def feature_each(layer, callback):
    if layer["type"] == 'Feature':
        callback(layer)
    elif layer["type"] == 'FeatureCollection':
        for i in range(len(layer["features"])):
            callback(layer["features"][i])


# Get all coordinates from any GeoJSON object, returning an array of coordinate
# arrays.
#
# @name coord_all
# @param {Object} layer any GeoJSON object
# @returns {Array<Array<Number>>} coordinate position array
def coord_all(layer):
    coords = []
    coord_each(layer, lambda coord: coords.append(coord))
    return coords


__all__ = [
    "coord_each",
    "feature_each"
]
