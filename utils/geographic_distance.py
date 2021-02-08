import math

def geographic_distance(lat_runway,long_runway,lat_stand,long_stand):
    
    '''
    Computes distance between two sets of coordinates:
    - (lat_runway, long_runway): geographical coordinates of RUNWAY
    - (lat_stand,long_stand): geographical coordinates of STAND.
    '''

    EARTH_RADIUS = 6371

    lat_runway_rad = math.radians(lat_runway)
    long_runway_rad = math.radians(long_runway)
    lat_stand_rad = math.radians(lat_stand)
    long_stand_rad = math.radians(long_stand)

    dist_long = long_stand_rad - long_runway_rad
    dist_lat =  lat_stand_rad - lat_runway_rad

    a = sin(dist_lat / 2)**2 +cos(lat_stand_rad) * cos(lat_runway_rad)
    a *= sin(dist_long / 2)**2

    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))

    distance = EARTH_RADIUS*c

    return distance
