import numpy as np
import os
from polypy import read as rd
from polypy import msd as msd
import unittest
from numpy.testing import assert_almost_equal

test_history = os.path.join(os.path.dirname(__file__), 'HISTORY')
test_config = os.path.join(os.path.dirname(__file__), 'CONFIG')
test_archive = os.path.join(os.path.dirname(__file__), 'ARCHIVE')
expected_z = os.path.join(os.path.dirname(__file__), 'Expected_Z')

class TestMsd(unittest.TestCase):

    def test_msd(self):
        test_data = rd.read_history(test_history, ["CA"])
        msd_data = msd.msd(test_data, 0.1)
        expected_msd = np.array([3, 12, 27, 3, 12, 27, 48, 75, 108])
        assert_almost_equal(msd_data['msd'], expected_msd)

    def test_smooth_msd(self):
        test_data = rd.read_history(test_history, ["CA"])
        msd_data = msd.smooth_msd(test_data, 0.1)
        expected_msd = np.array([14.25, 27.75, 49, 74, 120, 159, 108, 147])
        assert_almost_equal(msd_data['msd'], expected_msd)