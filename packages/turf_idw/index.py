from packages import bbox, centroid, distance, square_grid


# Takes a FeatureCollection of points with known value, a power parameter,
#   a cell depth, a unit of measurement and returns a FeatureCollection
#   of polygons in a square-grid with an interpolated value property "IDW"
#   for each grid cell.
# It finds application when in need of creating a continuous surface
#   (i.e. rainfall, temperature, chemical dispersion surface...)
#   from a set of spatially scattered points.
#
# @param  {FeatureCollection<Point>} controlPoints
#   Sampled points with known value
# @param  {String} valueField
#   GeoJSON field containing the known value to interpolate on
# @param  {Number} b
#   Exponent regulating the distance-decay weighting
# @param  {Number} cellWidth
#   The distance across each cell
# @param  {String} units
#   Units to use for cellWidth ('miles' or 'kilometers')
# @return {FeatureCollection<Polygon>} grid
#   A grid of polygons with a property field "IDW"
def idw(control_points, value_field, b, cell_width, units):
    # check if field containing data exists..
    filtered = filter(
        lambda feature: (feature["properties"] and
                         value_field in feature["properties"]),
        control_points["features"]
    )
    if len(filtered) != 0:
        # create a sample square grid
        # compared to a point grid helps visualizing the output
        sampling_grid = square_grid(bbox(control_points), cell_width, units)
        for i in range(len(sampling_grid["features"])):
            zw = 0
            sw = 0
            # calculate the distance from each control point to cell's centroid
            for j in range(len(control_points["features"])):
                d = distance(centroid(sampling_grid["features"][j]),
                             control_points["features"][j], units)
                if d == 0:
                    zw = control_points["features"][j]["properties"][value_field]
                w = 1.0 / pow(d, b)
                sw += w
                zw += w * control_points["features"][j]["properties"][value_field]
            # write IDW value for each grid cell
            sampling_grid["features"][i]["properties"]["z"] = zw / sw
        return sampling_grid
    else:
        print('Specified Data Field is Missing')
