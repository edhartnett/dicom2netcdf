import unittest
#import pdb
#from pprint import pprint
import src
from src import dicom2netcdf
from src.dicom2netcdf import convert_file

class TestDICOM2NetCDF(unittest.TestCase):
    """ Test dicom2netcdf functionality.

    """
    def test_convert_file(self):
        """ Tests simple file conversion.

        Args:
        self: pointer to test class instance.
        """
        test_data_dir = 'test/data'
        #test_filename = 'ct.001'
        test_filename = 'CR-MONO1-10-chest'
        
        output_filename = convert_file(test_data_dir, test_filename, False)
        self.assertEquals(output_filename, 'test.nc')
        
if __name__ == '__main__':
    unittest.main()
