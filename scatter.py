import numpy as np
import ovf
from numpy import arange, array, sqrt, pi, cos, sin, arctan2, arcsin, log, exp, sum, dot, cross, max
from numpy.linalg import norm
# from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# scatter-K4xF-3eta-stable-parallel

# Hopfion configuration
wavenumber	= 2*pi / 2
eta		= 0.161
c_veloc	        = 2.3

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
	numerator	= ((k_list**2 + eta) * k_list).flatten()
	denominator	= np.repeat(sqrt(sum((k_list**2 + eta)**2, axis=-1) - 3 * eta**2), 3)
	#numerator	= k_list.flatten()
	#denominator	= np.repeat(sqrt(sum(k_list**2, axis=-1)), 3)
	dxdt = numerator / denominator * c_veloc
	dkdt = cross(dxdt.reshape([-1, 3]), field(x_list)).flatten()
	dydt = np.concatenate((dxdt, dkdt))
	return dydt

def calc(output_prefix=''):
	nodes = 463
	scale = np.linspace(-20, 20, nodes)
	ry, rz = np.meshgrid(scale, scale)
	rx = np.ones(ry.shape) * -24
	kx = np.ones(ry.shape) * wavenumber
	ky = np.zeros(ry.shape)
	kz = np.zeros(ry.shape)
	x_list = np.stack((rx, ry, rz), axis=-1).flatten()
	k_list = np.stack((kx, ky, kz), axis=-1).flatten()
	y_list = np.concatenate((x_list, k_list))

	# result = odeint(diff_eq, y_list, t)
	result = solve_ivp(diff_eq, (0, 60 / wavenumber), y_list, max_step=0.2)
	# result = solve_ivp(diff_eq, (0, 50), y_list, max_step=0.5)
	total_k0 = array([ry.size * wavenumber, 0, 0])
	k_list = result.y[:, -1].reshape([2, -1, 3])[1, :, :]
	total_k1 = sum(k_list, axis=0)

	inc_k = (total_k0 - total_k1) / (nodes**2)
	print('%e, %s' % (wavenumber, inc_k.__repr__()))

        if output_prefix != '':
                config = {}
                config['xnodes'], config['ynodes'], config['znodes'] = nodes, nodes, 1
                config['xstepsize'] = config['ystepsize'] = config['zstepsize'] = 0.5e-9
                config['xbase'] = config['ybase'] = config['zbase'] = 0.25e-9
                ovf.writeOvf('%s-k-%.2f.ovf' % (output_prefix, wavenumber), config, k_list.reshape(nodes, nodes, 1, 3))

	"""
	fig = plt.figure(tight_layout=True)
	ax = fig.add_subplot(1, 1, 1, projection='3d')
	tnodes = result.t.size
	x_list = result.y[:, :].reshape([2, -1, 3, tnodes])[0, :, :, :]
	print(x_list.shape)
	for i in range(x_list.shape[0]):
		ax.scatter(x_list[i, 0, :], x_list[i, 1, :], x_list[i, 2, :])
	plt.show()
	"""

def main():
        global wavenumber
        for wavenumber in 2*pi*arange(0.050, 0.451, 0.019):
                calc('scatter-asc-p-1-q-2')