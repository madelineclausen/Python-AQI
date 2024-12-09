# Madeline Clausen
# 60633236

import urllib.request
import urllib.error
import json
import math
from pathlib import Path

class AnyError(Exception):
    '''
    If any exception is raised, it causes this AnyError
    which is caught in the run() module. It will end the
    program without printing anything other than the error
    statements.
    '''
    pass

class Location:

    def aqi_places(radius: int, lat1: float, lon1: float, aqi_data: dict) -> dict:
        '''
        Similar to the narrow function in project3.py, this function takes a
        dictionary of converted json data and filters out any bad inputs such
        as "null", None, an indoor sensor, or not recently updated. It also
        only includes results within the equirectangular distance.
        '''
        radius_locations = {}
        for item in aqi_data["data"]:
            if item[26] != "null" and item[26] is not None:
                if item[27] != "null" and item[27] is not None:
                    if item[28] != "null" and item[28] is not None:
                        if item[1] != "null" and item[1] is not None:
                            distance = Location.equirectangular(lat1, lon1, item[27], item[28])
                            if distance <= radius and item[25] == 0 and item[4] < 3600:
                                radius_locations[item[0]] = item[1] # {..., ID : pm, ...}
        return radius_locations

    def equirectangular(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        '''
        Two sets of latitude and longitude are passed in and converted to
        equirectangular form. This is used in the above function to
        determine distance.
        '''
        try:
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            alat = math.radians((lat1 + lat2) / 2)
            r = 3958.8
            x = dlon * math.cos(alat)
            return math.sqrt(x**2 + dlat**2) * r
        except TypeError:
            return 0
    
    def n_s_e_w(lat: float, lon: float) -> tuple:
        '''
        Based on a given latitude and longitude,
        the hemisphere is determined, either
        North, South, East, or West. The result
        is later printed alongside the coordinates.
        '''
        if lat < 0:
            n_or_s = 'S'
        elif lat > 0:
            n_or_s = 'N'
        else:
            n_or_s = ''
        if lon < 0:
            w_or_e = 'W'
        elif lon > 0:
            w_or_e = 'E'
        else:
            w_or_e = ''
        return n_or_s, w_or_e
        
class Nominatim:
    '''
    Handles all of the calls for Nominatim data.
    It can come from 2 places, either the API or
    a file. The class handles both instances by
    passing in a string and returning a tuple.
    '''

    def file(file: str) -> tuple:
        try:
            with open(file, encoding='utf-8') as f:
                nominatim_forward = json.load(f)
            return nominatim_forward[0]['lat'], nominatim_forward[0]['lon']
        except json.JSONDecodeError:
            print('FAILED')
            print(Path(file).absolute())
            print('FORMAT')
            raise AnyError
        except FileNotFoundError as f:
            print('FAILED')
            print(file)
            print('MISSING')
            raise AnyError
        

    def api(search: str) -> tuple:
        try:
            location = search.replace(' ', '+')
            url = 'https://nominatim.openstreetmap.org/?q=' + location + '&format=json&limit=1'
            request = urllib.request.Request(url)
            request.add_header('Referer', 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/clausenm')
            contents = urllib.request.urlopen(request)
            nominatim_forward = json.loads(contents.read().decode('utf-8'))
            return nominatim_forward[0]['lat'], nominatim_forward[0]['lon']
        except json.JSONDecodeError:
            print('FAILED')
            print(urllib.response.status, urllib.response.url)
            print('FORMAT')
            raise AnyError
        except urllib.error.HTTPError as h:
            print('FAILED')
            print(h.code, h.url)
            if h.code != 200:
                print('NOT 200')
            raise AnyError
        except urllib.error.URLError:
            print('FAILED')
            print(url)
            print('NETWORK')
            raise AnyError

    
class PurpleAir:
    '''
    Handles all of the calls for PurpleAir data.
    It can come from 2 places, either the API or
    a file. The class handles both instances.
    '''

    def file(path: str) -> dict:
        try:
            with open(path, encoding='utf-8') as file:
                aqi_data = json.load(file)    
            return aqi_data
        except json.JSONDecodeError:
            print('FAILED')
            print(Path(path).absolute())
            print('FORMAT')
            raise AnyError
        except FileNotFoundError as f:
            print('FAILED')
            print(path)
            print('MISSING')
            raise AnyError

    def api() -> dict:
        try:
            url = 'https://www.purpleair.com/data.json'
            request = urllib.request.Request(url)
            request.add_header('Referer', 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/clausenm')
            contents = urllib.request.urlopen(request)
            aqi_data = json.loads(contents.read().decode("utf-8"))
            return aqi_data
        except json.JSONDecodeError:
            print('FAILED')
            print(urllib.response.status, urllib.response.url)
            print('FORMAT')
            raise AnyError
        except urllib.error.HTTPError as h:
            print('FAILED')
            print(h.code, h.url)
            if h.code != 200:
                print('NOT 200')
            raise AnyError
        except urllib.error.URLError:
            print('FAILED')
            print(url)
            print('NETWORK')
            raise AnyError

class Center:
    '''
    Handles the call for a center determination.
    It can come from 2 places, either the API or
    a file. The class handles both instances by
    passing in a string and returning a tuple.
    '''

    def file(path: str) -> tuple:
        try:
            path = path.split('FILE ')[1]
            with open(path, encoding='utf-8') as file:
                center = json.load(file)
                lat, lon = float(center[0]['lat']), float(center[0]['lon'])
                n_or_s, w_or_e = Location.n_s_e_w(lat, lon)
            return lat, lon, n_or_s, w_or_e
        except json.JSONDecodeError:
            print('FAILED')
            print(Path(path).absolute())
            print('FORMAT')
            raise AnyError
        except FileNotFoundError as f:
            print('FAILED')
            print(path)
            print('MISSING')
            raise AnyError

    def api(center: str) -> tuple:
        center = center.split('NOMINATIM ')
        lat, lon = Nominatim.api(center[1])
        n_or_s, w_or_e = Location.n_s_e_w(float(lat), float(lon))
        return float(lat), float(lon), n_or_s, w_or_e

class Reverse:
    '''
    Handles the location description calls for
    Nominatim data. It can come from 2 places,
    either the API or a file. The class handles
    both instances.
    '''

    def file(files: list) -> list:
        try:
            names = []
            for file in files:
                with open(file, encoding='utf-8') as f:
                    nominatim_reverse = json.load(f)
                    names.append(nominatim_reverse['display_name'])
            return names
        except json.JSONDecodeError:
            print('FAILED')
            print(Path(file).absolute())
            print('FORMAT')
            raise AnyError
        except FileNotFoundError as f:
            print('FAILED')
            print(file)
            print('MISSING')
            raise AnyError

    def api(lat: float, lon: float) -> str:
        try:
            url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + str(lat) + '&lon=' + str(lon)
            request = urllib.request.Request(url)
            request.add_header('Referer', 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/clausenm')
            contents = urllib.request.urlopen(request)
            nominatim_reverse = json.loads(contents.read().decode('utf-8'))
            return nominatim_reverse['display_name']
        except json.JSONDecodeError:
            print('FAILED')
            print(urllib.response.status, urllib.response.url)
            print('FORMAT')
            raise AnyError
        except urllib.error.HTTPError as h:
            print('FAILED')
            print(h.code, h.url)
            if h.code != 200:
                print('NOT 200')
            raise AnyError
        except urllib.error.URLError:
            print('FAILED')
            print(url)
            print('NETWORK')
            raise AnyError
        
    
