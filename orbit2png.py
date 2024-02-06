#!/usr/bin/python

import sys

import numpy as np
from math import pi
from numpy import arange, array, where, append, linspace
from ovf import readOvf

import colorsys
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 12), tight_layout=True)
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.set_aspect('equal','box')
ax.set_frame_on(True)
ax.set_axis_on()
ax.set_autoscale_on(False)
ax.set_xbound(0, 50)
ax.set_ybound(0, 50)
ax.set_zbound(0, 50)
ax.set_xlabel('x (nm)')
ax.set_ylabel('y (nm)')
ax.set_zlabel('z (nm)')

def drawVectorFieldWithTrajectories(trajectories, scatterpoints, m, corner_start=[0, 0, 0], corner_end=[-1, -1, -1], stepsize=[1, 1, 1], base=[0, 0, 0]):
	sx = m[:, :, :, 0]
	sy = m[:, :, :, 1]
	sz = m[:, :, :, 2]
	z0, y0, x0 = corner_start
	z1, y1, x1 = corner_end
	znodes, ynodes, xnodes, temp = m.shape
	x0 = xnodes + x0 + 1 if x0 < 0 else x0
	y0 = ynodes + y0 + 1 if y0 < 0 else y0
	z0 = znodes + z0 + 1 if z0 < 0 else z0
	x1 = xnodes + x1 + 1 if x1 < 0 else x1
	y1 = ynodes + y1 + 1 if y1 < 0 else y1
	z1 = znodes + z1 + 1 if z1 < 0 else z1

	# position
	y = np.arange(y0, y1) * stepsize[1] + base[1]
	z = np.arange(z0, z1) * stepsize[2] + base[2]
	x = np.arange(x0, x1) * stepsize[0] + base[0]
	y, z, x = np.meshgrid(y, z, x)
	x = x.flatten() / 1e-9
	y = y.flatten() / 1e-9
	z = z.flatten() / 1e-9
	nspins = x.size

	# color
	sx, sy, sz = sx[z0:z1, y0:y1, x0:x1], sy[z0:z1, y0:y1, x0:x1], sz[z0:z1, y0:y1, x0:x1]
	sx = sx.flatten()
	sy = sy.flatten()
	sz = sz.flatten()
	mag = np.sqrt(sx*sx + sy*sy + sz*sz)
	maxmag = np.max(mag)
	sx = sx / maxmag
	sy = sy / maxmag
	sz = sz / maxmag
	hue = np.arctan2(sy, sx) / (pi * 2) % 1.0
	lightness = np.clip(sz * 0.5 + 0.5, 0, 1)
	saturation = np.sqrt(sx*sx + sy*sy)
	alpha = np.clip(mag / maxmag * 2, 0, 1)
	rgba = np.zeros(hue.shape + (4,))
	for i, hue1 in enumerate(hue):
		rgba[i] = to_rgba(colorsys.hls_to_rgb(hue[i], lightness[i], 1), alpha[i])
		rgba[i] = to_rgba(colorsys.hls_to_rgb(0.6, alpha[i], 1), alpha[i])
		rgba[i] = to_rgba(colorsys.hls_to_rgb(hue[i], lightness[i], saturation[i]), alpha[i])
	rgba = array(rgba)
	
	# scale
	s = np.ones(nspins) * 50

	# position
	ntracepoints = trajectories.size / 3
	nsections = trajectories.shape[0]
	trajectories = trajectories.reshape([nsections, -1, 3])
	ntrajectories = trajectories.shape[1]

	x2 = y2 = z2 = array([])
	for i in range(ntrajectories):
		x2 = np.concatenate((x2, trajectories[:, i, 0]))
		y2 = np.concatenate((y2, trajectories[:, i, 1]))
		z2 = np.concatenate((z2, trajectories[:, i, 2]))
	
	# color
	#rgba2 = np.clip(1 - arange(ntracepoints)[::-1] * 1.0 / decay, 0, 1)
	rgba2 = np.ones(ntracepoints)
	rgba2 = array([ to_rgba('k', alpha) for alpha in rgba2 ])

	# scale
	s2 = np.ones(ntracepoints) * 8

	# position
	nscatterpoints = scatterpoints.shape[0]
	x3 = scatterpoints[:, 0]
	y3 = scatterpoints[:, 1]
	z3 = scatterpoints[:, 2]

	# color
	rgba_scatterpoints = np.ones(nscatterpoints)
	rgba3 = array([ to_rgba(colorsys.hls_to_rgb(0, 0.2, 1), i) for i in rgba_scatterpoints ])
	rgba4 = array([ to_rgba(colorsys.hls_to_rgb(0, 0.5, 1), i) for i in rgba_scatterpoints ])
	rgba5 = array([ to_rgba(colorsys.hls_to_rgb(0, 0.7, 1), i) for i in rgba_scatterpoints ])
	rgba6 = array([ to_rgba(colorsys.hls_to_rgb(0, 1.0, 1), i) for i in rgba_scatterpoints ])

	# scale
	s3 = s4 = s5 = s6 = np.ones(nscatterpoints)
	s3 = s3 * 100
	s4 = s4 * 80
	s5 = s5 * 40
	s6 = s6 * 7

	# merge
	x = np.concatenate((x, x2, x3, x3+1e-12, x3+2e-12, x3+3e-12))
	y = np.concatenate((y, y2, y3, y3+1e-10, y3+1.2e-10, y3+1.4e-10))
	z = np.concatenate((z, z2, z3, z3+1e-10, z3+1.2e-10, z3+1.4e-10))
	rgba = np.concatenate((rgba, rgba2, rgba3, rgba4, rgba5, rgba6))
	rgba = rgba.reshape([-1, 4])
	s = np.concatenate((s, s2, s3, s4, s5, s6))

	ind = np.lexsort((s,x,y,z))
	xall = array([ x[i] for i in ind ])
	yall = array([ y[i] for i in ind ])
	zall = array([ z[i] for i in ind ])
	call = array([ rgba[i, :] for i in ind ])
	sall = array([ s[i] for i in ind ])

	ax.scatter(xall, yall, zall, c=call, s=sall, marker='.', edgecolors='none')


def main(argv):
	ovf1 = readOvf(argv[1])
	config = ovf1['config']
	m1 = ovf1['data']

	# unzip the configuration
	xnodes, ynodes, znodes = config['xnodes'], config['ynodes'], config['znodes']
	stepsize = xstepsize, ystepsize, zstepsize = config['xstepsize'], config['ystepsize'], config['zstepsize']
	base = xbase, ybase, zbase = config['xbase'], config['ybase'], config['zbase']

	# read the trajectories from file
	trace = np.zeros([1000, 2*13*3+1]) # ad hoc configured
	ftrace = open(argv[2], 'r')
	lines = ftrace.readlines()
	for iline, line in enumerate(lines):
		trace[iline, :] = [ float(term) for term in line.split(',') ]
	trace = trace + 25
	nsections = int(argv[3]) + 1
	trace = trace[:nsections, 13*3+1:] # ad hoc configured
	ntrajectories = 13
	# the number of points are cut by half
	reducingfactor = int(argv[4])
	trace = trace[::reducingfactor, :]
	nsections = trace.shape[0]
	# the trajectories are reconstructed by interpolation
	toriginal = linspace(0, 1, nsections)
	tinterp = linspace(0, 1, (nsections-1)*reducingfactor*5+1)
	trajectories = np.zeros([(nsections-1)*reducingfactor*5+1, ntrajectories * 3])
	for i in range(ntrajectories * 3):
		trajectories[:, i] = np.interp(tinterp, toriginal, trace[:, i].flatten())
	# the scatter points on each trajectory are picked out
	scatterpoints = trace[-1:, :].reshape([-1, 3])

	drawVectorFieldWithTrajectories(trajectories, scatterpoints, m1, [25, 25, 25], [75, 75, 75], stepsize=stepsize, base=base)

	print(nsections)
	ax.view_init(elev=30, azim=100 + nsections*0.5)
	plt.savefig('vf-1.png')
	# plt.savefig('vf-' + num_vector_figures.__repr__() + '.png', dpi=300)


if __name__ == "__main__":
	main(sys.argv)
