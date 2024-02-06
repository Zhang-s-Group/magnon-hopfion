#!/usr/bin/python

import sys

import numpy as np
from numpy import arange, array, where
import ovf
from plotvf import drawVectorField, drawScalarField
#from sift import computeKeypointsWithOrientations, generateDescriptors

def main(argv):
	ovf1 = ovf.readOvf(argv[1], ovf.SCALAR_FIELD)
	config = ovf1['config']
	e1 = ovf1['data']

	# unzip the configuration
	xnodes, ynodes, znodes = config['xnodes'], config['ynodes'], config['znodes']
	stepsize = xstepsize, ystepsize, zstepsize = config['xstepsize'], config['ystepsize'], config['zstepsize']
	base = xbase, ybase, zbase = config['xbase'], config['ybase'], config['zbase']

	# represent antiferromagnet in the form of ferromagnet
	# y, z, x = np.meshgrid(arange(ynodes), arange(znodes), arange(xnodes))
	# e1 = where((x + y + z) % 2 == 0, -e1, e1)
	# x1 = e1[:, :, :, 0]
	print(e1[10,20,20])
	scale = 1.0
	if len(argv) > 2:
		scale = float(argv[2])
	offset = 0.0
	if len(argv) > 3:
		offset = float(argv[3])
	e1 = np.clip((e1 + offset) / scale, -1., 1.)

	drawScalarField(e1, [20, 40, 40], [40, 60, 60], stepsize=stepsize, base=base)	
#	drawVectorField(m1, [0, 30, 30], [60, 90, 90], stepsize=stepsize, base=base)
#	drawVectorField(m1, [20, 40, 40], [40, 60, 60], stepsize=stepsize, base=base)
#	drawVectorField(m1, [27, 40, 61], [47, 60, 81], stepsize=stepsize, base=base)


if __name__ == "__main__":
	main(sys.argv)
