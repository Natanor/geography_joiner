from shapely.geometry import Polygon
import numpy as np


def is_sequence(obj):
    '''
    Returns True if obj is a sequence.
    '''
    seq = (not hasattr(obj, "strip") and
           hasattr(obj, "__getitem__") or
           hasattr(obj, "__iter__"))

    seq = seq and not isinstance(obj, dict)
    # numpy sometimes returns objects that are single float64 values
    # but sure look like sequences, so we check the shape
    if hasattr(obj, 'shape'):
        seq = seq and obj.shape != ()
    return seq


def random_polygon(segments=8, radius=0.0001, movement= 0.2):
    '''
    Generate a random polygon with a maximum number of sides and approximate radius.

    Arguments
    ---------
    segments: int, the maximum number of sides the random polygon will have
    radius:   float, the approximate radius of the polygon desired

    Returns
    ---------
    polygon: shapely.geometry.Polygon object with random exterior, and no interiors.
    '''
    angles = np.sort(np.cumsum(np.random.random(segments)*np.pi*2) % (np.pi*2))
    radii  = np.random.random(segments)*radius

    points = np.column_stack((np.cos(angles), np.sin(angles)))*radii.reshape((-1,1))
    points = points + np.random.random(2)*movement + (34.3, 31.4)
    points = np.vstack((points, points[0]))
    polygon = Polygon(points).buffer(0.0)
    if is_sequence(polygon):
        return polygon[0]
    return polygon



pass