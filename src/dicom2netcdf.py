""" Module to convert DICOM files to netCDF.

Author:
Edward Hartnett, 2/10/16
"""
from __future__ import print_function
import gzip
import os
import shutil
import pdb
import datetime
import argparse
import httplib2
import sys
import gnupg
import os
from pprint import pprint
import dicom
import netCDF4
from netCDF4 import Dataset

try:
    # Parse the command line arguments.
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-v', '--verbose', action="store_true", default=False,
                        help='Turn on verbose command line output.')
    PARSER.add_argument('input_file', 
                        help='Name of the DICOM file.', default=None)
    FLAGS = PARSER.parse_args()

except ImportError:
    FLAGS = None

# Define call-back functions for the dataset.walk() function
def PN_callback(ds, data_element):
    """Called from the dataset "walk" recursive function for all data
    elements."""

    print('new data element:')
    pprint(data_element)
    pdb.set_trace()
    if data_element.VR == "PN":
        data_element.value = 'joe'

def convert_file(directory, filename, verbose):
    """ Convert a DICOM file to netCDF.
    
    Args:
    directory: the directory where the file is.
    filename: name of DICOM file to convert.
    verbose: true to get printf statements.

    Returns:
    The name of the netCDF file.
    """
    verbose = 1
    if (verbose):
        print('convert_file is converting file ' + filename);

    ds = dicom.read_file(directory + '/' + filename, force=True)
    netcdf_filename = filename + '.nc'
    #pdb.set_trace()
    
    rootgrp = Dataset(netcdf_filename, "w", format="NETCDF4")
    rootgrp.description = "bogus example script"
    for tag_name in ds.dir():
        de = ds.data_element(tag_name)

        VR_exists = True
        print('data element ' + tag_name)        
        try:
            de.VR
        except AttributeError:
            VR_exists = False
        else:
            VR_exists = True

        if tag_name != 'PixelData':
            if VR_exists:
                print('data element ' + tag_name + ' ' + de.VR)
                if de.VR != 'SQ':
                    setattr(rootgrp, tag_name, de.value)
        else:
            print('copying data')
            if (verbose):
                print('creating dimension row with len ' + str(ds.Rows))
            rowdim = rootgrp.createDimension("row", ds.Rows)
            if (verbose):
                print('creating dimension col with len ' + str(ds.Columns)) 
            coldim = rootgrp.createDimension("column", ds.Columns)
            pixel_data = rootgrp.createVariable("pixel_data","i4",("row","column"))
            pixel_data[:] = ds.pixel_array
            

    #dataset.walk(PN_callback)
    rootgrp.close()
    return 'test.nc'

def main():
    """Handles command line parameters and processed data.

    """

    if FLAGS.verbose:
        print('converting DICOM file ' + FLAGS.input_file + ' to netCDF.')

    # Process the data.
    convert_file('.', FLAGS.input_file, FLAGS.verbose)

if __name__ == '__main__':
    main()
