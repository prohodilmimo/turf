from packages import distance

# Takes a bounding box and calculates the minimum square bounding box that
# would contain the input.
#
# @name square
# @param {Array<number>} bbox extent in [minX, minY, maxX, maxY] order
# @return {Array<number>} a square surrounding `bbox`
# @example
# var bbox = [-20,-20,-15,0];
#
# var squared = turf.square(bbox);
#
# var features = {
#   "type": "FeatureCollection",
#   "features": [
#     turf.bboxPolygon(bbox),
#     turf.bboxPolygon(squared)
#   ]
# };
#
# //=features
def square(bbox):
    horizontal_distance = distance(bbox.slice(0, 2), [bbox[2], bbox[1]],
                                   'miles')
    vertical_distance = distance(bbox.slice(0, 2), [bbox[0], bbox[3]], 'miles')
    if horizontal_distance >= vertical_distance:
        vertical_midpoint = (bbox[1] + bbox[3]) / 2
        return [
            bbox[0],
            vertical_midpoint - ((bbox[2] - bbox[0]) / 2),
            bbox[2],
            vertical_midpoint + ((bbox[2] - bbox[0]) / 2)
        ]
    else:
        horizontal_midpoint = (bbox[0] + bbox[2]) / 2
        return [
            horizontal_midpoint - ((bbox[3] - bbox[1]) / 2),
            bbox[1],
            horizontal_midpoint + ((bbox[3] - bbox[1]) / 2),
            bbox[3]
        ]
