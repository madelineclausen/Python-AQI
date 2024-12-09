# Madeline Clausen
# 60633236

import project3_classes
import urllib
import json
import time

def pm_to_aqi_conversion(locations: dict) -> dict:
    '''
    Takes in a dictionary with a location
    description for a key and a PM 2.5 number for
    a value, and returns a new dictionary in which
    the PM 2.5 values have been converted to AQI
    '''
    new_dict = {}
    for key, value in locations.items():
        try:
            if float(value) < 12.1:
               new_value = (value / 12) * 50
            elif float(value) < 35.5:
                new_value = (((value - 12.1) / 23.3) * (100 - 51)) + 51
            elif float(value) < 55.5:
                new_value = (((value - 35.5) / 19.9) * (150 - 101)) + 101
            elif float(value) < 150.5:
                new_value = (((value - 55.5) / 94.9) * (200 - 151)) + 151
            elif float(value) < 250.5:
                new_value = (((value - 150.5) / 99.9) * (300 - 201)) + 201
            elif float(value) < 350.5:
                new_value = (((value - 250.5) / 99.9) * (400 - 301)) + 301
            elif float(value) < 500.5:
                new_value = (((value - 350.5) / 149.9) * (500 - 401)) + 401
            else:
                if 500.5 <= float(value):
                    new_value = 501
            new_dict[key] = round(new_value)
        except TypeError:
            pass
    return new_dict

def narrow(locations: dict, threshold: int, max_locations: int) -> dict:
    '''
    Takes in the dictionary after AQI conversion
    and narrows options based on threshold and max
    number of locations. It does threshold first in
    order to determine which AQI places match, and
    then takes the worst of those and returns the
    final results.
    '''
    sorted_dict = {}
    sorted_names = sorted(locations, key=locations.get, reverse=True)
    for name in sorted_names:
        sorted_dict[name] = locations[name]
    threshold_dict = {}    
    for key, value in sorted_dict.items():
        if value >= threshold:
            threshold_dict[key] = value
    final_dict = {}
    x = 0
    for key, value in threshold_dict.items():
        if x < max_locations:
            final_dict[key] = value
            x += 1
    return final_dict

def run():
    '''
    The main module where code comes together and
    runs. Inputs are taken, functions are called,
    and finally, results are printed. Error handling
    also takes place to catch possible failures.
    '''
    center = input()
    miles = int(input().split()[1])
    threshold = int(input().split()[1])
    max_locations = int(input().split()[1])
    aqi_data = input()
    reverse = input()
    try:
        if ' PURPLEAIR' in aqi_data:
            file = project3_classes.PurpleAir.api()
            time.sleep(1)
        else:
            if ' FILE ' in aqi_data:
                path = aqi_data.split('FILE ')[1]
                file = project3_classes.PurpleAir.file(path)
                
        if 'NOMINATIM' in center:
            lat, lon, n_or_s, w_or_e = project3_classes.Center.api(center)
            time.sleep(1)
        else:
            if 'FILE' in center:
                lat, lon, n_or_s, w_or_e = project3_classes.Center.file(center)
                
        radius_locations_pm = project3_classes.Location.aqi_places(miles, float(lat), float(lon), file)
        radius_locations_aqi = pm_to_aqi_conversion(radius_locations_pm)
        final_list = narrow(radius_locations_aqi, threshold, max_locations)
        print('CENTER {}/{} {}/{}'.format(abs(lat), n_or_s, abs(lon), w_or_e))
        for i in range(len(final_list.keys())):
            key = list(final_list.keys())
            value = list(final_list.values())
            print('AQI', value[i])
            for item in file["data"]:
                if key[i] == item[0]:
                    latitude, longitude = item[27], item[28]
                    n_or_s, w_or_e = project3_classes.Location.n_s_e_w(latitude, longitude)
                    print('{}/{} {}/{}'.format(abs(latitude), n_or_s, abs(longitude), w_or_e))
                    if ' NOMINATIM' in reverse:
                        print(project3_classes.Reverse.api(latitude, longitude))
                        time.sleep(1)
                    else:
                        if 'FILES' in reverse:
                            paths = reverse.split('FILES ')[1].split()
                            names = project3_classes.Reverse.file(paths)
                            print(names[i])
        
    except project3_classes.AnyError:
        pass

if __name__ == '__main__':
    run()
