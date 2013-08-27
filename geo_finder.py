"""
 Program to find all the states that lay in a shortest line between 2 addresses.
 The formulas for how to calculate the line and the rest of the spherical
 geometry are taken mostly from:
 http://en.wikipedia.org/wiki/Great-circle_navigation
 How it works:
 The latitude and longitude coordinates for 2 addresses are calculated. Then
 certain variables for a spherical line that traverses the shortest distance
 between these coordinates is calculated. Then the line is traversed, a certain
 amount of kilometers at a time, and the new latitude and longitude coordinates
 are run through google in order to retrieve the currect state. All new states
 are appended to a list, whihc is printed out in the end.

 by Ethan Wright, 7/30/13
"""

import json
import urllib
from math import *
import time

EARTH_RADIUS = 6371.009
RADS_TO_DEGS = 57.2957795
DEGS_TO_RADS = 0.0174532925

def get_coordinates(address):
    """Return the latitude and longitude coordinates for an address"""

    google_conn = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % address)
    try:
        location = google_conn.read()
    finally:
        google_conn.close()

    location = json.loads(location)

    if location['status'] == 'ZERO_RESULTS':
        raise Exception("Error looking up address")

    if 'bounds' in location['results'][0]['geometry']:
        bounds = location['results'][0]['geometry']['bounds']
        latitude = (bounds['northeast']['lat'] + bounds['southwest']['lat']) / 2
        longitude = (bounds['northeast']['lng'] + bounds['southwest']['lng']) / 2
    elif 'location' in location['results'][0]['geometry']:
        latitude = location['results'][0]['geometry']['location']['lat']
        longitude = location['results'][0]['geometry']['location']['lng']
    else:
        raise Exception("Error looking up address")

    return latitude, longitude

def search_line(address1, address2):
    """Search various points along a spherical line"""

    state_list = []
    latitude1, longitude1 = get_coordinates(address1)
    latitude2, longitude2 = get_coordinates(address2)

    azimuth, sigma_0_2, sigma_1, lambda_0 = calc_vars(
            latitude1, longitude1, latitude2, longitude2)

    #Setup vars
    cos_az = cos(azimuth)
    sin_az = sin(azimuth)
    distance = EARTH_RADIUS * sigma_0_2

    #Solve for new locations
    for d in xrange(1, int(floor(distance)), 50):
        new_sigma = sigma_1 + d/EARTH_RADIUS #Location to get coordinates for
        sin_new_sigma = sin(new_sigma)
        new_lat = asin(cos_az * sin_new_sigma)
        new_lng = atan2(sin_az * sin_new_sigma, cos(new_sigma)) + lambda_0
        new_lat *= RADS_TO_DEGS
        new_lng *= RADS_TO_DEGS
        if new_lng > 180:
            new_lng = new_lng - 360
        elif new_lng < -180:
            new_lng = new_lng + 360
        state = get_state(new_lat, new_lng)
        if state not in state_list:
            state_list.append(state)
    return state_list

def calc_vars(lat1, lng1, lat2, lng2):
    """Calculate variables needed to calculate points on the spherical line"""

    lng_diff = lng2 - lng1
    if lng_diff > 180:
        lng_diff = lng_diff - 360
    elif lng_diff < -180:
        lng_diff = lng_diff + 360

    #Covert to radians
    lat1 *= DEGS_TO_RADS
    lat2 *= DEGS_TO_RADS
    lng1 *= DEGS_TO_RADS
    lng2 *= DEGS_TO_RADS
    lng_diff *= DEGS_TO_RADS

    """Variable caluclations"""
    #alpha_1    = Initial course
    #alpha_1    = Final course
    #sigma_0_2  = Angular measurment of central angle from start to end
    #azimuth    = Angular measurement
    #sigma_1    = Angular distance from start to measurment point
    #sigma_2    = Angular distance from measurment point to end
    #lambda_0_1 =  longitude at the node of the great circle
    #lambda_0   = original longitude = labda_0_1

    alpha_1 = atan2(sin(lng_diff), (cos(lat1) * tan(lat2) - sin(lat1) * cos(lng_diff)))
    alpha_2 = atan2(sin(lng_diff), (-(cos(lat2) * tan(lat1)) + sin(lat2) * cos(lng_diff)))
    sigma_0_2 = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lng_diff))
    azimuth = asin(sin(alpha_1) * cos(lat1))

    sigma_1 = atan2(tan(lat1), cos(alpha_1))
    if sigma_1 < 0:
        sigma_2 = sigma_0_2 + sigma_1
    else:
        sigma_2 = sigma_0_2 - sigma_1
    lambda_0_1 = atan2(sin(azimuth) * sin(sigma_1), cos(sigma_1))
    lambda_0 = lng1 - lambda_0_1

    return (azimuth, sigma_0_2, sigma_1, lambda_0)

def get_state(latitude, longitude):
    """Get a state based of it's latitude and longitude"""

    google_conn = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" % (latitude, longitude))
    try:
        location = google_conn.read()
    finally:
        google_conn.close()

    location = json.loads(location)
    for listing in location['results'][0]['address_components']:
        if 'administrative_area_level_1' in listing['types']:
            state = listing ['long_name']
    if state == '':
        raise Exception("Error looking up state at %s, %s" % (latitude, longitude))
    time.sleep(.1)

    return state

def main():
    address1="575 shotwell st san francisco CA"
    address2="2601 alnwick rd Bryn Athyn PA 19009"
    state_list = search_line(address1, address2)
    for state in state_list:
        print state


if __name__ == '__main__':
    main()
