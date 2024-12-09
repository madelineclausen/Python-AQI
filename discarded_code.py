'''
def center_lat_lon(center: str) -> tuple:
    if 'NOMINATIM' in center:
        center = center.split('NOMINATIM ')
        lat, lon = nominatim_forward(center[1])
    else:
        if 'FILE' in center: 
            pass
    n_or_s, w_or_e = north_south_east_or_west(float(lat), float(lon))
    return lat, lon, n_or_s, w_or_e

def nominatim_forward(search: str) -> str:
    try:
        
    except urllib.error.HTTPError:
        print('FAILED')
        print(urllib.error.HTTPError.getcode, urllib.error.HTTPError.geturl)
        if urllib.error.HTTPError.getcode != 200:
            print('NOT 200')

def reverse(lat: float, lon: float, files='') -> str:
    try:
            
    except urllib.error.HTTPError:
        print('FAILED')
        print(urllib.error.HTTPError.getcode, urllib.error.HTTPError.geturl)
        if urllib.error.HTTPError.getcode != 200:
            print('NOT 200')
            
def north_south_east_or_west(lat: float, lon: float) -> tuple:
    if lat < 0:
        n_or_s = 'S'
    else:
        n_or_s = 'N'   
    if lon < 0:
        w_or_e = 'W'
    else:
        w_or_e = 'E'

    return n_or_s, w_or_e


def equirectangular(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    try:
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        alat = math.radians((lat1 + lat2) / 2)
        r = 3958.8
        x = dlon * math.cos(alat)
        return math.sqrt(x**2 + dlat**2) * r
    except TypeError:
        return 0

def find_aqi_locations(radius: int, lat1: float, lon1: float, file='') -> dict:
    radius_locations = {}
    try:
        if len(file) == 0:
            contents = urllib.request.urlopen('https://www.purpleair.com/data.json').read()
            aqi_data = json.loads(contents.decode('utf-8'))
        else:
            with open(file) as f:
                aqi_data = json.loads(str(f.read()))
        for item in aqi_data["data"]:
            distance = equirectangular(lat1, lon1, item[27], item[28])
            if distance <= radius and item[25] == 0 and item[4] < 3600:
                radius_locations[item[26]] = [item[1], item[27], item[28]] # {..., place : [pm, lat, long], ...}
        return radius_locations
    except urllib.error.HTTPError:
        print('FAILED')
        print(str(urllib.error.HTTPError.getcode), str(urllib.error.HTTPError.geturl))
        if urllib.error.HTTPError.getcode != 200:
            print('NOT 200')
'''
