from numbers import Number


factors = {
    "miles":            3960,
    "nauticalmiles":    3441.145,
    "degrees":          57.2957795,
    "radians":          1,
    "inches":           250905600,
    "yards":            6969600,
    "meters":           6373000,
    "metres":           6373000,
    "kilometers":       6373,
    "kilometres":       6373
}


def radians_to_distance(radians, units="kilometers"):
    # type: (Number, str) -> Number
    """
    Convert a distance measurement from radians to a more friendly unit

    :type   radians:    Number
    :param  radians:    distance in radians across the sphere
    :type   units:      str
    :param  units:      units: one of miles, nauticalmiles, degrees, radians,
                        inches, yards, metres, meters, kilometres, kilometers
    :rtype:             Number
    :return:            distance
    :raises ValueError: when fed with an invalid unit type
    """

    factor = factors[units]

    if factor is None:
        raise ValueError('Invalid unit')

    return radians * factor


def distance_to_radians(distance, units="kilometers"):
    # type: (Number, str) -> Number
    """
    Convert a distance measurement from a real-world unit into radians

    :type   distance:   Number
    :param  distance:   distance in real units
    :type   units:      str
    :param  units:      one of miles, nauticalmiles, degrees, radians,
                        inches, yards, metres, meters, kilometres, kilometers
    :rtype:             Number
    :return:            radians
    :raises ValueError: when fed with an invalid unit type
    """
    factor = factors[units]

    if factor is None:
        raise ValueError("Invalid unit")

    return distance / factor


def distance_to_degrees(distance, units="kilometers"):
    # type: (Number, str) -> Number
    """
    Convert a distance measurement from a real-world unit into degrees

    :type   distance:   Number
    :param  distance:   distance in real units
    :type   units:      str
    :param  units:      one of miles, nauticalmiles, degrees, radians,
                        inches, yards, metres, meters, kilometres, kilometers
    :rtype:             Number
    :return:            degrees
    :raises ValueError: when fed with an invalid unit type
    """
    factor = factors[units]

    if factor is None:
        raise ValueError("Invalid unit")

    return (distance / factor) * 57.2958


__all__ = [
    "factors",
    "radians_to_distance",
    "distance_to_radians",
    "distance_to_degrees"
]
