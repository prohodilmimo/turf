from packages import distance

# Takes a reference {@link Point|point} and a FeatureCollection of Features
# with Point geometries and returns the
# point from the FeatureCollection closest to the reference. This calculation
# is geodesic.
#
# @name nearest
# @param {Feature<Point>} targetPoint the reference point
# @param {FeatureCollection<Point>} points against input point set
# @return {Feature<Point>} the closest point in the set to the reference point
# @example
# var point = {
#   "type": "Feature",
#   "properties": {
#     "marker-color": "#0f0"
#   },
#   "geometry": {
#     "type": "Point",
#     "coordinates": [28.965797, 41.010086]
#   }
# };
# var against = {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [28.973865, 41.011122]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [28.948459, 41.024204]
#       }
#     }, {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Point",
#         "coordinates": [28.938674, 41.013324]
#       }
#     }
#   ]
# };
#
# var nearest = turf.nearest(point, against);
# nearest.properties['marker-color'] = '#f00';
#
# var resultFeatures = against.features.concat(point);
# var result = {
#   "type": "FeatureCollection",
#   "features": resultFeatures
# };
#
# //=result
def nearest(target_point, points):
    nearest_point = None
    min_dist = float("inf")
    for i in range(len(points["features"])):
        distance_to_point = distance(target_point, points["features"][i],
                                     'miles')
        if distance_to_point < min_dist:
            nearest_point = points["features"][i]
            min_dist = distance_to_point

    return nearest_point

