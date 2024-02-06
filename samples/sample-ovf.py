#!/usr/bin/python

import sys

import numpy as np
from numpy import arange, array, where
from ovf import readOvf
from plotvf import drawVectorField, drawScalarField
#from sift import computeKeypointsWithOrientations, generateDescriptors

def main(argv):
	ovf1 = readOvf(argv[1])
	config = ovf1['config']
	m1 = ovf1['data']

	# unzip the configuration
	xnodes, ynodes, znodes = config['xnodes'], config['ynodes'], config['znodes']
	stepsize = xstepsize, ystepsize, zstepsize = config['xstepsize'], config['ystepsize'], config['zstepsize']
	base = xbase, ybase, zbase = config['xbase'], config['ybase'], config['zbase']

	# represent antiferromagnet in the form of ferromagnet
	y, z, x, temp = np.meshgrid(arange(ynodes), arange(znodes), arange(xnodes), [0, 0, 0])
	m1 = where((x + y + z) % 2 == 0, -m1, m1)
	x1 = m1[:, :, :, 0]

	drawVectorField(m1, stepsize=stepsize, base=base)


if __name__ == "__main__":
	main(sys.argv)
