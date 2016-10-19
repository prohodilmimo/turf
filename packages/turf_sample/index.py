# http://stackoverflow.com/questions/11935175/sampling-a-random-subset-from-an-array
from geojson import FeatureCollection
from random import random
import math

# Takes a {@link FeatureCollection} and returns a FeatureCollection with
#   given number of {@link Feature|features} at random.
#
# @name sample
# @param {FeatureCollection} featurecollection set of input features
# @param {number} num number of features to select
# @return {FeatureCollection} a FeatureCollection with `n` features
# @example
# var points = turf.random('points', 1000);
#
# //=points
#
# var sample = turf.sample(points, 10);
#
# //=sample
def sample(featurecollection, num):
    return FeatureCollection(
        get_random_subarray(featurecollection.features, num)
    )

def get_random_subarray(arr, size):
    shuffled = arr[:]
    i = len(arr)
    min = i - size

    while i > min:
        i -= 1
        index = math.floor((i + 1) * random())
        temp = shuffled[index]
        shuffled[index] = shuffled[i]
        shuffled[i] = temp

    return shuffled.slice(min)
