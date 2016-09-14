#!/usr/bin/python
#---------------------------------------------
# Script:   
# Name:     Javier
# Date:        Wed Sep 14 08:43:54 BST 2016
# Description:  
#---------------------------------------------

import unittest
from exifgps import Imagegps

class TestUM(unittest.TestCase):

    def setUp(self):
        self.image = Imagegps("")

        pass

    def test_set_decimal_degrees(self):
        tests = [ [{'GPS GPSLatitude': "[1, 60, 3600]", 'GPS GPSLatitudeRef': "N", 'GPS GPSLongitude': "[1, 60, 3600]", 'GPS GPSLongitudeRef': "W"}, (3.0, -3.0)],
                  [{'GPS GPSLatitude': "[1, 60, 3600]", 'GPS GPSLatitudeRef': "N", 'GPS GPSLongitude': "[1, 60, 3600]", 'GPS GPSLongitudeRef': "E"}, (3.0, 3.0)],
                  [{'GPS GPSLatitude': "[1, 60, 3600]", 'GPS GPSLatitudeRef': "S", 'GPS GPSLongitude': "[1, 60, 3600]", 'GPS GPSLongitudeRef': "E"}, (-3.0, 3.0)]
                ]
        for test in tests:
            self.assertEqual(self.image._set_decimal_degrees(test[0]),test[1])

            
    def test_long_lat_to_decimal_degrees(self):
        
        tests = [ ["[1, 60, 3600]", 3],
                  ["[10/10, 3600/60, 3600]", 3]
                ]

        for test in tests:
            self.assertEqual(self.image._long_lat_to_decimal_degrees(test[0]),test[1])

    def test_gps_to_decimal_degrees(self):

        tests = [ [("1","60","3600"), 3],
                  [("10/10","3600/60","3600"), 3],
                  [("10/10","3600/60","3600"), 3] ]

        for test in tests:
            self.assertEqual(self.image._gps_to_decimal_degrees(test[0]),test[1])



    def test_is_valid_filetype(self):
        tests = [ ["hello.jpg", True],
                  ["hello.JPG", True],
                  ["hello.jpeg", True],
                  ["hellot.JPEG", True],
                  ["hello.JpEG", True],
                  ["hello.JPg", True],
                  ["hello.txt", False],
                  ["hello.doc", False],
                  ["hello", False]
                ]
        for test in tests:
            self.assertEqual(self.image._is_valid_filetype(test[0]),test[1])
 
    def test_convert_int_float(self):
        tests = [ ["1", 1.0],
                  ["2/1", 2.0],
                  ["1/2", 0.5],
                  ["-1", -1.0],
                  ["1/10", 0.1]
                ]
        for test in tests:
            self.assertEqual(self.image._convert_int_float(test[0]), test[1])

    def test_valid_gps(self):
        tests = [[{'GPS GPSLatitude': 1, 'GPS GPSLatitudeRef': "W",
                  'GPS GPSLongitude': 2, 'GPS GPSLongitudeRef': "N"}, True],
                 [{'GPS GPSLatitude': 1, 'GPS GPSLatitudeRef': "W",
                 'GPS GPSLongitude': 2 }, False],
                 [{'GPS GPSLatitude': 1, 'GPS GPSLatitudeRef': "W"}, False],
                 [{'GPS GPSLatitude': 1}, False],
                 [{}, False],
                 [{'GPS GPSLatitude': 1, 'GPS GPSLatitudeRef': "W",
                   'GPS GPSLongitude': 2, 'GPS GPSLongitudeRef': "N",
                   'GPS GPSAltitute': 3}, True]
                 ]

        for test in tests:
            self.assertEqual(self.image._valid_gps(test[0]), test[1])

    def test_set_zoom_level(self):
        tests = [1, 2, 3, 21]
        for test in tests:
            self.image.set_zoom_level(test)
            self.assertEqual(test, self.image.get_zoom_level())

        tests = [0, -1, "hello", 122, 22]
        for test in tests:
            self.image.set_zoom_level(15)
            self.image.set_zoom_level(test)
            self.assertEqual(15, self.image.get_zoom_level())


    def test_set_google_url(self):
        '''
        Test google url generator
        '''
        tests = [ [((50.0000000, 50.0000000), 1), "https://google.co.uk/maps/@50.0000000,50.0000000,1z"],
                  [((50, 50), 1), "https://google.co.uk/maps/@50.0000000,50.0000000,1z"]
                ]
        test_count = 0 
        for test in tests:
            test_values = test[0]
            self.assertEqual(self.image._set_google_url(test_values[0], test_values[1]),test[1])



if __name__ == '__main__':
    unittest.main()


