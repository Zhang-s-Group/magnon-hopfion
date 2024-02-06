#!/usr/bin/python

import sys
import numpy as np
import ovf

from numpy import pi, arcsin, abs, arctan2, exp, sqrt, cos, sin, tan, log, where, arange, power

import matplotlib.cm as cm
import matplotlib.pyplot as plt

def main(argv):
	# mesh & grid
	xstepsize = ystepsize = zstepsize = 0.5e-9
	xnodes = ynodes = znodes = 100
	xmin = ymin = zmin = (xnodes - 1) * xstepsize * 0.5
	y, z, x = np.meshgrid(arange(ynodes), arange(znodes), arange(xnodes))
	x, y, z = x * xstepsize - xmin, y * ystepsize - ymin, z * zstepsize - zmin
	
	# hopfion parameters
	P = -1
	Q = -1
	HopfRad = 7e-9 # 3.2e-9
	x /= HopfRad
	y /= HopfRad
	z /= HopfRad
	phi = arctan2(y, x)
	rho = sqrt(x*x + y*y)
	r = sqrt(x*x + y*y + z*z)
	bipolar	= log((rho+z*1j + 1) / (rho+z*1j - 1))
	sPhi	= P * bipolar.imag + Q * phi - pi/2 + pi*0.1
	sTheta	= rho**2 * exp(1. - rho**2 - z**2*2)
	sTheta	= arcsin(sTheta) * 2
	# sPhi	= arctan2(-bipolar.real, bipolar.imag) + phi

	# fill in the 'config' sheet
	config = {}
	config['xnodes'], config['ynodes'], config['znodes'] = xnodes, ynodes, znodes
	config['xbase'] = config['ybase'] = config['zbase'] = 0.25e-9
	config['xstepsize'], config['ystepsize'], config['zstepsize'] = xstepsize, ystepsize, zstepsize

	# fill in the 'data' sheet
	m = np.zeros([znodes, ynodes, xnodes, 3])
	m[:,:,:,0] = sin(sTheta) * cos(sPhi)
	m[:,:,:,1] = sin(sTheta) * sin(sPhi)
	m[:,:,:,2] = cos(sTheta)
	
	ovf.writeOvf(argv[1], config, m)



	fig, ax = plt.subplots(1,1)
	scatter = m[:, 50, :, :]
	ax.quiver(scatter[:, :, 1], scatter[:, :, 2], scale=2, scale_units='xy')
	im = ax.imshow(scatter[:, :, 1], cmap=cm.hsv)
	cbar = fig.colorbar(im, ax=ax)
	ax.set_xlabel('y')
	ax.set_ylabel('z')
	plt.savefig(argv[1] + '.png', dpi=600)



if __name__ == "__main__":
	main(sys.argv)
