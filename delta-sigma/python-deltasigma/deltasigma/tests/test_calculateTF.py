# -*- coding: utf-8 -*-
# test_calculateTF.py
# This module provides the tests for the calculateTF() function.
# Copyright 2014 Giuseppe Venturini & Shayne Hodge
# This file is part of python-deltasigma.
#
# python-deltasigma is a 1:1 Python replacement of Richard Schreier's
# MATLAB delta sigma toolbox (aka "delsigma"), upon which it is heavily based.
# The delta sigma toolbox is (c) 2009, Richard Schreier.
#
# python-deltasigma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LICENSE file for the licensing terms.

import unittest
import numpy as np
import deltasigma as ds
from deltasigma._utils import cplxpair


class TestCalculateTF(unittest.TestCase):
    """Test function for calculateTF()"""

    def setUp(self):
        ABCD = [[1.0, 0.0, 0.0, 0.044408783846879, -0.044408783846879],
                [0.999036450096481, 0.997109907515262, -0.005777399147297,
                 0.0, 0.499759089304780],
                [0.499759089304780, 0.999036450096481, 0.997109907515262,
                 0.0, -0.260002096136488],
                [0.0, 0.0, 1.0,  0.0, 0.0]]
        ABCD = np.array(ABCD)
        ntf, stf = ds.calculateTF(ABCD)
        ntf_zeros, ntf_poles, _ = ntf
        stf_zeros, stf_poles, _ = stf
        mntf_poles = np.array((1.498975311463384, 1.102565142679772,
                               0.132677264750882))
        mntf_zeros = np.array((0.997109907515262 + 0.075972576202904j,
                               0.997109907515262 - 0.075972576202904j,
                               1.000000000000000 + 0.000000000000000j))
        mstf_zeros = np.array((-0.999999999999996,))
        mstf_poles = np.array((1.498975311463384, 1.102565142679772,
                               0.132677264750882))

        # for some reason, sometimes the zeros are in different order.
        self.ntf_zeros, self.mntf_zeros = (cplxpair(ntf_zeros),
                                           cplxpair(mntf_zeros))
        self.stf_zeros, self.mstf_zeros = (cplxpair(stf_zeros),
                                           cplxpair(mstf_zeros))
        self.ntf_poles, self.mntf_poles = (cplxpair(ntf_poles),
                                           cplxpair(mntf_poles))
        self.stf_poles, self.mstf_poles = (cplxpair(stf_poles),
                                           cplxpair(mstf_poles))

    def test_calculateTF1(self):
        """Test function for calculateTF() 1/4"""
        # ntf zeros
        self.assertTrue(np.allclose(self.ntf_zeros, self.mntf_zeros, rtol=1e-5,
                        atol=1e-8))
        # ntf poles
        self.assertTrue(np.allclose(self.ntf_poles, self.mntf_poles, rtol=1e-5,
                        atol=1e-8))
        # stf zeros
        self.assertTrue(np.allclose(self.stf_zeros, self.mstf_zeros, rtol=1e-5,
                        atol=1e-8))
        # stf poles
        self.assertTrue(np.allclose(self.stf_poles, self.mstf_poles, rtol=1e-5,
                        atol=1e-8))

    def test_calculateTF2(self):
        """Test function for calculateTF() 2/4"""
        # test an easy TF
        ABCD = np.array([[1., 1., -1.],
                        [1., 0., 0.]])
        k = 1.
        ntf, stf = ds.calculateTF(ABCD, k) 
        ntf_zeros, ntf_poles, ntf_gain = ntf
        stf_zeros, stf_poles, stf_gain = stf
        self.assertTrue(np.allclose(stf_poles, [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(not len(stf_zeros))
        self.assertTrue(np.allclose(stf_gain, 1., rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntf_poles, [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntf_zeros, [1.], rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntf_gain, 1., rtol=1e-5, atol=1e-8))

    def test_calculateTF3(self):
        """Test function for calculateTF() 3/4"""
        # test for the default k value
        ABCD = np.array([[1., 1., -1.],
                        [1., 0., 0.]])
        ntf, stf = ds.calculateTF(ABCD)
        ntf_zeros, ntf_poles, ntf_gain = ntf
        stf_zeros, stf_poles, stf_gain = stf
        self.assertTrue(np.allclose(stf_poles, [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(not len(stf_zeros))
        self.assertTrue(np.allclose(stf_gain, 1., rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntf_poles, [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntf_zeros, [1.], rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntf_gain, 1., rtol=1e-5, atol=1e-8))

    def test_calculateTF4(self):
        """Test function for calculateTF() 4/4"""
        # Easy test for a 2-quantizers system
        # MASH 1-0 cascade
        ABCD = [[1, 1, -1, 0],
                [1, 0, 0, 0],
                [1, 0, -1, 0]]
        ABCD = np.array(ABCD, dtype=np.float_)
        k = [1., 1.]
        # here we get back arrays of transfer functions
        ntfs, stfs = ds.calculateTF(ABCD, k=k)
        # stfs
        self.assertTrue(np.allclose(stfs[0][1], [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(not len(stfs[0][0]))
        self.assertTrue(np.allclose(stfs[0][2], 1., rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(stfs[1][1], [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(not len(stfs[1][0]))
        self.assertTrue(np.allclose(stfs[1][2], 1., rtol=1e-5, atol=1e-8))
        # e1 to V1
        self.assertTrue(np.allclose(ntfs[0, 0][1], [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntfs[0, 0][0], [1.], rtol=1e-5, atol=1e-8))
        self.assertTrue(np.allclose(ntfs[0, 0][2], 1., rtol=1e-5, atol=1e-8))
        # e1 to V2
        self.assertTrue(np.allclose(ntfs[1, 0][1], [0.], rtol=1e-5, atol=1e-8))
        self.assertTrue(not len(ntfs[1, 0][0]))
        self.assertTrue(np.allclose(ntfs[1, 0][2], -1., rtol=1e-5, atol=1e-8))
        # e2 to V2
        self.assertTrue(not len(ntfs[1, 1][0]))
        self.assertTrue(not len(ntfs[1, 1][1]))
        self.assertTrue(np.allclose(ntfs[1, 1][2], 1., rtol=1e-5, atol=1e-8))
        # e2 to V1
        self.assertTrue(np.allclose(ntfs[0, 1][2], 0., rtol=1e-5, atol=1e-8))

