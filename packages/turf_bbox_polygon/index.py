from geojson import Polygon

# Takes a bbox and returns an equivalent {@link Polygon|polygon}.
#
# @name bboxPolygon
# @param {Array<number>} bbox extent in [minX, minY, maxX, maxY] order
# @return {Feature<Polygon>} a Polygon representation of the bounding box
# @example
# var bbox = [0, 0, 10, 10];
#
# var poly = turf.bboxPolygon(bbox);
#
# //=poly

def bbox_polygon (bbox):
    low_left = [bbox[0], bbox[1]]
    top_left = [bbox[0], bbox[3]]
    top_right = [bbox[2], bbox[3]]
    low_right = [bbox[2], bbox[1]]

    return Polygon(([
        low_left,
        low_right,
        top_right,
        top_left,
        low_left
    ],))
