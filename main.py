from geohash_shape.geohash_shape import geohash_shape
from random_polygon import random_polygon
from itertools import groupby
import time
from shapely.geometry import Polygon

# studd = [(poly, geohash_shape(poly, 7))for poly in [random_polygon() for x in range(350000)]]
# b = [[(x[0], y) for y in x[1]] for x in studd]
# c= [x for y in b for x in y]
# d = [(x,y) for (y,x) in c]
# e = sorted(d, key=lambda x: x[0])
# dic = {}
# for k,g in groupby(e, key=lambda x: x[0]):
#     dic[k] = [x[1] for x in list(g)]
# pass
from utils import get_size, read_pickle, write_as_pickle

GEOHASH_LENGTH_DEFAULT = 7


def flatten_list(list_of_lists):
    return [x for y in list_of_lists for x in y]


def create_dict(buildings, geohash_length=GEOHASH_LENGTH_DEFAULT):
    buildings_with_geohashs = [(building, geohash_shape(building["shape"], geohash_length)) for building in buildings]
    flattened_buildings_with_geohashs = flatten_list([[(x[0], y) for y in x[1]] for x in buildings_with_geohashs])
    geohash_locator = lambda x: x[1]
    grouped_by_geohash_iterator = groupby(sorted(flattened_buildings_with_geohashs, key=geohash_locator), key=geohash_locator)
    dic = {}
    for k, g in grouped_by_geohash_iterator:
        dic[k] = [x[0] for x in list(g)]
    return dic


def create_random_dict(amount, geohash_length=GEOHASH_LENGTH_DEFAULT):
    return create_dict([{"id": x, "shape": random_polygon()} for x in range(amount)], geohash_length)


def calculate_trash(buildings, geometry):
    built_area_polygon = Polygon()
    for building in buildings:
        built_area_polygon = built_area_polygon.union(building["shape"])

    return [(building, calculate_singualar_trash(building["shape"], geometry, built_area_polygon.intersection(geometry).area)) for building in buildings]


def calculate_singualar_trash(building, polygon, built_area):
    return calculate_pct_of_built_area(building, polygon, built_area), calculate_pct_of_building(building, polygon), calculate_pct_of_polygon(building, polygon)


def calculate_pct_of_built_area(building ,polygon, built_area):
    return building.intersection(polygon).area / built_area if built_area > 0 else -1


def calculate_pct_of_polygon(building ,polygon):
    return building.intersection(polygon).area / polygon.area if polygon.area > 0 else -1


def calculate_pct_of_building(building ,polygon):
    return building.intersection(polygon).area / building.area if building.area > 0 else -1


def find_intersections(buildings_dict, geometry, geohash_length=GEOHASH_LENGTH_DEFAULT):
    geohashes = geohash_shape(geometry, geohash_length)
    potential_buildings = flatten_list([buildings_dict.get(x, []) for x in geohashes])
    buildings = [building  for building in potential_buildings if building["shape"].intersects(geometry)]
    buildings_with_trash = calculate_trash(buildings, geometry)
    return buildings_with_trash

rnd_dict = create_random_dict(350000)
write_as_pickle(rnd_dict, "rnd_dict.pkl")
rnd_dict = read_pickle("rnd_dict.pkl")


for i in range(5):
    test_cases =  [random_polygon() for x in range(10**i)]
    start = time.time()
    test_collisions = [(a, find_intersections(rnd_dict, a) )for a in test_cases]
    end = time.time()
    print(10**i, "   ", (end - start)/ 10**i)

pass