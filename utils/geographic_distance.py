import numpy as np

def geographic_distance(lat_runway,long_runway,lat_stand,long_stand):
    '''
    Computes distance between two sets of coordinates:
    - (lat_runway, long_runway): geographical coordinates of RUNWAY
    - (lat_stand,long_stand): geographical coordinates of STAND.
    '''

    EARTH_RADIUS = 6371

    lat_runway_rad = np.radians(lat_runway)
    long_runway_rad = np.radians(long_runway)
    lat_stand_rad = np.radians(lat_stand)
    long_stand_rad = np.radians(long_stand)

    dist_long = long_stand_rad - long_runway_rad
    dist_lat =  lat_stand_rad - lat_runway_rad

    a = np.sin(dist_lat / 2)**2 +np.cos(lat_stand_rad) * np.cos(lat_runway_rad)
    a*= np.sin(dist_long / 2)**2

    c = 2 * np.arctan2(np.sqrt(a),np.sqrt(1-a))

    distance = EARTH_RADIUS * c

    return distance
