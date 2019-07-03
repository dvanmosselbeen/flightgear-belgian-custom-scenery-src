#!/usr/bin/python
"""
Little script that check PNG files for useless alpha channel and remove the
alpha channel if not used. For this it use a little hack by making use of the
histogram of the alpha layer. Which seems to be correct, cheap and the fastest
and most optimal way.

Usage:
======
./alpha_cleanup.py /some/path/*.png
"""

import Image, sys

def main(files):
    for infile in files:
        try:
            im = Image.open(infile)
            # If image has alpha channel
            if im.mode == "RGBA":
                # Split up the image in bands
                R, G, B, A = 0, 1, 2, 3
                source = im.split()
                # Using the histogram on the alpha layer as check, should be ways
                # faster as per pixel check 
                histogram = source[A].histogram()
                # If the alpha band histogram is all 0 except the last value,
                # we guess it's full translucent.
                if sum(histogram[:-1]) == 0:
                    print "Removed alpha layer of file %s" % (im.filename)
                    # Finally convert back the RGBA to RGB
                    im = im.convert("RGB").save(infile)

        except IOError:
            print "Cannot read file", infile

if __name__ == "__main__": 
    main(sys.argv[1:])

