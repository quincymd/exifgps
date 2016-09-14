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


