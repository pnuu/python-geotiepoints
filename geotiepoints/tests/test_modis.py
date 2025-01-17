#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2021 Python-geotiepoints developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for python-geotiepoints: MODIS examples."""

import unittest
import numpy as np
import h5py
import os

FILENAME_250M_RESULT = os.path.join(
    os.path.dirname(__file__), '../../testdata/250m_lonlat_section_result.h5')
FILENAME_250M_INPUT = os.path.join(
    os.path.dirname(__file__), '../../testdata/250m_lonlat_section_input.h5')

FILENAME_FULL = os.path.join(
    os.path.dirname(__file__), '../../testdata/test_5_to_1_geoloc_full.h5')
FILENAME_5KM = os.path.join(
    os.path.dirname(__file__), '../../testdata/test_5_to_1_geoloc_5km.h5')

from geotiepoints import (modis5kmto1km, modis1kmto250m)

from geotiepoints import get_scene_splits


class TestUtils(unittest.TestCase):

    """Class for unit testing the ancillary interpolation functions
    """

    def setUp(self):
        pass

    def test_get_numof_subscene_lines(self):
        """Test getting the number of sub-scene lines dependent on the number
        of CPUs and for various number of lines in a scan"""

        ncpus = 3
        scene_splits = get_scene_splits(1060,
                                        10, ncpus)


class TestMODIS(unittest.TestCase):

    """Class for system testing the MODIS interpolation.
    """

    def setUp(self):
        pass

    def test_5_to_1(self):
        """test the 5km to 1km interpolation facility
        """

        with h5py.File(FILENAME_FULL) as h5f:
            glons = h5f['longitude'][:] / 1000.
            glats = h5f['latitude'][:] / 1000.

        with h5py.File(FILENAME_5KM) as h5f:
            lons = h5f['longitude'][:] / 1000.
            lats = h5f['latitude'][:] / 1000.

        tlons, tlats = modis5kmto1km(lons, lats)

        self.assert_(np.allclose(tlons, glons, atol=0.05))
        self.assert_(np.allclose(tlats, glats, atol=0.05))

    def test_1000m_to_250m(self):
        """test the 1 km to 250 meter interpolation facility
        """

        with h5py.File(FILENAME_250M_RESULT) as h5f:
            glons = h5f['longitude'][:] / 1000.
            glats = h5f['latitude'][:] / 1000.

        with h5py.File(FILENAME_250M_INPUT) as h5f:
            lons = h5f['longitude'][:] / 1000.
            lats = h5f['latitude'][:] / 1000.

        tlons, tlats = modis1kmto250m(lons, lats)

        self.assert_(np.allclose(tlons, glons, atol=0.05))
        self.assert_(np.allclose(tlats, glats, atol=0.05))

        tlons, tlats = modis1kmto250m(lons, lats, cores=4)

        self.assert_(np.allclose(tlons, glons, atol=0.05))
        self.assert_(np.allclose(tlats, glats, atol=0.05))
