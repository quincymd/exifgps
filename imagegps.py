#!/usr/bin/python
#---------------------------------------------
# Name:     Javier
# Date:        Mon Sep 12 17:07:17 BST 2016
# Description:  
#---------------------------------------------
'''
Imagegps Package
================

This package reads EXIF information in  jpg or tiff images.
It converts the GPS information into the equivalent Google
Maps url.

SETUP
=====

- Requires exifread module to be installed


USAGE
=====

Methods:
-------

    
- read(image_filename)    : Returns single imagepgs object
- process_exif()          : Converts EXIF GPS information to google url 

- search(directory)       : Searches recursivley directory and Returns list of processed imagegps objects

- set_zoom_level(integer) : Set google maps zoom level (1-21)
- get_zoom_level()        : Returns current zoom level

- get_filename()          : Return filename
- get_url()               : Return google_url if EXIF present. Returns "" if no EXIF information

    
EXAMPLES
========

Single Image
::

    import imagegps

    image = imagegps.read(image_filename)
    image.process_exif()
    print image.get_url()

Search Directory
::

    import imagegps

    image_list = imagegps.search(directory)
    for image in image_list:
        print image.get_url()
        print image.get_filename()
'''

import exifread
import logging
import re
import os
import copy
import warnings

lat_regex = re.compile(r'''
        .(([0-9\/]+)..
        ([0-9\/]+)..
        ([0-9\/]+)).*''', re.VERBOSE)

MAX_ZOOM_LEVEL = 21
MIN_ZOOM_LEVEL = 1

class Imagegps(object):
    def __init__(self, filename):
        self._has_gps = False
        self._url = ""
        self._filename = filename
        self._zoom = 16

    def _is_valid_filetype(self, filename):
        '''
        Takes a filename
        Return True/False if filename has valid extension
        '''
        valid_extensions = ("jpg", "jpeg", "tiff")
        filename = filename.lower()
        return filename.endswith(valid_extensions)

    def _convert_int_float(self, string):
        '''
        Takes string of format [0-9/], i.e. 123/3 or just digits,
        and converts to calculated float.
        Returns float
        '''
        if "/" in string:
            (numerator, denominator) = string.split("/")
            numerator = float(numerator)
            denominator = float(denominator)
            return numerator/denominator
        else:
            return float(string)

    def _long_lat_to_decimal_degrees(self, gps_tag):
        '''
        Takes a gps long/lat tag of form "[1,3,12/5]"
        Returns float decimal degrees
        '''
        matches = lat_regex.search(str(gps_tag))
        degree_data = matches.groups()
        decimal_degrees = self._gps_to_decimal_degrees(degree_data[1:])
        return decimal_degrees

    def _gps_to_decimal_degrees(self, gps_data):
        '''
        Takes a tuple of 3 strings containing digits and /
        Returns float decimal degrees
        '''
        degrees = self._convert_int_float(gps_data[0])
        minutes = self._convert_int_float(gps_data[1])
        seconds = self._convert_int_float(gps_data[2])
        return degrees + (minutes/60.0) + (seconds/3600) 

    def set_zoom_level(self, zoom_level):
        '''
        Set valid zoom_level
        '''
        if zoom_level >= MIN_ZOOM_LEVEL and zoom_level <= MAX_ZOOM_LEVEL:
            self._zoom = int(zoom_level)

    def get_zoom_level(self):
        return self._zoom

    def _read_exif(self, filename):
        '''
        Opens valid file and reads exif tags
        Returns dictionary of all GPS tags
        or None if no exif data/unable to open file
        '''
        gps = {}

        if os.path.exists(filename) == False:
            print "Error: Unable to open %s" % filename
            return None 

        with open(filename, "rb") as fh:
            tags = exifread.process_file(fh, details=False)

        if len(tags) != 0:
            for tag in tags.keys():
                if "GPS" in tag:
                    gps[tag] = tags[tag]
        return gps 

    def _set_google_url(self, decimal_degrees, zoom):
        '''
        Takes decimal degrees and converts to valid
        google maps url
        Returns google url string
        '''
        lat = decimal_degrees[0]
        long = decimal_degrees[1]
        
        url = "https://google.co.uk/maps/@%.7f,%.7f,%dz" % (lat, long, zoom)
        
        logging.debug("url is %s" % url)
        return url

    def _valid_gps(self, gps_tags):
        '''
        Return True/False if image has all tags:
            GPSLongitude,
            GPSLatitude,
            GPSLongitudeRef,
            GPSLatitudueRef
        '''
        needed_tags = [ "GPS GPSLongitude", "GPS GPSLatitude", "GPS GPSLongitudeRef", "GPS GPSLatitudeRef"]
        tags = gps_tags.keys()
        for tag in needed_tags:
            if tag not in tags:
                return False
        return True

    def _set_decimal_degrees(self, gps_tags):
        '''
        Reads image gps tags and converts to decimal degrees
        Returns tuple of (latitude, longitude)
        '''
        for key, value in gps_tags.items():
            if key == "GPS GPSLatitude":
                lat = self._long_lat_to_decimal_degrees(value)
            elif key == "GPS GPSLongitude":
                long = self._long_lat_to_decimal_degrees(value)
            elif key == "GPS GPSLongitudeRef":
                long_ref = str(value)
            elif key == "GPS GPSLatitudeRef":
                lat_ref = str(value)

        if long_ref == "W":
            long *= -1
        if lat_ref == "S":
            lat *= -1
        return (lat, long)

    def get_filename(self):
        '''
        Returns filename
        '''
        return self._filename

    def process_exif(self):
        '''
        Opens valid file, read exif information and calculates decimal degrees
        '''
        if self._is_valid_filetype(self._filename) == True:
            self._gps_tags = self._read_exif(self._filename)
            if len(self._gps_tags) != 0:
                if self._valid_gps(self._gps_tags):
                    self._has_gps = True
                    self._decimal_degrees = self._set_decimal_degrees(self._gps_tags)
         
    def get_url(self):
        '''
        Creates google_url with current zoom level
        '''
        if self._has_gps:
            self._url = self._set_google_url(self._decimal_degrees, self._zoom)
        return self._url
    
    def __str__(self):
        string = "Filename: %s\n" % self._filename
        string += "Url: %s\n" % self.get_url()
        return string

def read(filename):
    return Imagegps(filename)

def search(directory):
    image_list = []
    if os.path.exists(directory) == False:
        print "Error: Unable to open directory %s" % directory
        return
    for root, dir, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            full_path = os.path.abspath(full_path)
            image = Imagegps(full_path)
            image.process_exif()
            url = image.get_url()
            if url != "":
                image_list.append(copy.deepcopy(image))

    return image_list
