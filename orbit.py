import numpy as np
import ovf
from numpy import arange, array, sqrt, pi, cos, sin, arctan2, arcsin, log, exp, sum, dot, cross, max
from numpy.linalg import norm
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys


# Hopfion configuration
wavenumber	= 2.10
# 
eta		= 0.161
charspeed	= 2.3

ovf0		= ovf.readOvf('udf/m-equiv.ovf')
m0		= np.swapaxes(ovf0['data'], 0, 2)
m		= m0[:-1, :-1, :-1, :]
pmpx		= (m0[1:, :-1, :-1, :] - m) / 0.5
pmpy		= (m0[:-1, 1:, :-1, :] - m) / 0.5
pmpz		= (m0[:-1, :-1, 1:, :] - m) / 0.5
fx		= sum(m * cross(pmpy, pmpz), axis=-1)
fy		= sum(m * cross(pmpz, pmpx), axis=-1)
fz		= sum(m * cross(pmpx, pmpy), axis=-1)
x = np.linspace(-24.75, 24.25, 99)
fx_itp = RegularGridInterpolator((x, x, x), fx)
fy_itp = RegularGridInterpolator((x, x, x), fy)
fz_itp = RegularGridInterpolator((x, x, x), fz)

def field(x_list):
	x_list = np.clip(x_list, -24.25, 24.25)
	f = np.stack((fx_itp(x_list), fy_itp(x_list), fz_itp(x_list)), axis=-1)
	enable = np.repeat(max(abs(x_list), axis=-1)>24.2, 3).reshape(x_list.shape)
	f = np.where(enable, 0, f)
	return f

def diff_eq(t, y_list):	
	y_list = y_list.reshape([2, -1, 3])
	x_list = y_list[0, :, :]
	k_list = y_list[1, :, :]
	numerator	= (k_list**3).flatten()
	denominator	= np.repeat(sqrt(sum(k_list**4, axis=-1)), 3)
	#numerator	= k_list.flatten()
	#denominator	= np.repeat(sqrt(sum(k_list**2, axis=-1)), 3)
	dxdt = numerator / denominator * charspeed
	dkdt = cross(dxdt.reshape([-1, 3]), field(x_list)).flatten()
	dydt = np.concatenate((dxdt, dkdt))
	return dydt

def main(argv):
	ynodes = 2
	znodes = 13
	yscale = np.linspace(-0.5, 0.5, ynodes)
	zscale = np.linspace(-4, 2, znodes)
	ry, rz = np.meshgrid(yscale, zscale, indexing='ij')
	rx = np.ones(ry.shape) * -24
	kx = np.ones(ry.shape) * wavenumber
	ky = np.zeros(ry.shape)
	kz = np.zeros(ry.shape)
	x_list = np.stack((rx, ry, rz), axis=-1).flatten()
	k_list = np.stack((kx, ky, kz), axis=-1).flatten()
	y_list = np.concatenate((x_list, k_list))

	result = solve_ivp(diff_eq, (0, 60 / wavenumber), y_list, max_step=0.2)
	# result = solve_ivp(diff_eq, (0, 60 / wavenumber), y_list, max_step=0.2)
	# total_k0 = array([ry.size * wavenumber, 0, 0])
	# k_list = result.y[:, -1].reshape([2, -1, 3])[1, :, :]
	# total_k1 = sum(k_list, axis=0)

	f = open('orbits-%.2f.csv' % wavenumber, 'w')
	for itime, time in enumerate(result.t):
		f.write('%e' % time)
		for var in result.y[:ynodes*znodes*3, itime]:
			f.write(', %e' % var)
		f.write('\n')
	f.close()

if __name__ == "__main__":
	main(sys.argv)
