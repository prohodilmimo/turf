from packages.turf_meta import coord_each
import json

# Takes input features and flips all of their coordinates
# from `[x, y]` to `[y, x]`.
#
# @name flip
# @param {(Feature|FeatureCollection)} input input features
# @returns {(Feature|FeatureCollection)} a feature or set of features
#   of the same type as `input` with flipped coordinates
# @example
# var serbia = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [20.566406, 43.421008]
#   }
# };
#
# //=serbia
#
# var saudiArabia = turf.flip(serbia);
#
# //=saudiArabia
def flip(input):
    # ensure that we don't modify features in-place and changes to the
    # output do not change the previous feature, including changes to nested
    # properties.
    input = json.loads(json.dumps(input))

    coord_each(input, lambda coord: reversed(coord))
    return input

