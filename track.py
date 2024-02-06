#!/usr/bin/python

import sys

import numpy as np
from numpy import array, where, arctan2, abs, sin, cos, sqrt, round, clip, arange, isnan, argmax, roll
from math import pi
from ovf import readOvf
from plotvf import drawVectorField, drawScalarField

def phaseCorrelation(z1, z2):
	if z1.shape != z2.shape:
		raise Exception('The two scalar fields do not share the same configuration.')

	Z1 = np.fft.fftn(z1)
	Z2 = np.fft.fftn(z2)
	R = Z1.conj() * Z2
	abs_R = abs(R)
	abs_R = where(abs_R == 0., 1, abs_R)
	R /= abs_R
	R = where(isnan(R), 0, R)
	r = abs(np.fft.ifftn(R))

	# weighted centroid of argmax
	shift = np.unravel_index(argmax(r), r.shape)
	sum_weight = 0.0
	sum_shift = np.zeros(3)
	num_i, num_j, num_k = z1.shape
	for i in range(-1, 2):
		for j in range(-1, 2):
			for k in range(-1, 2):
				ii = (shift[0] + i) % num_i
				jj = (shift[1] + j) % num_j
				kk = (shift[2] + k) % num_k
				sum_weight += r[ii, jj, kk]
				sum_shift += array([i, j, k]) * r[ii, jj, kk]
	shift += sum_shift / sum_weight * 1.4142

	shape = array(z1.shape).astype('int')
	shift = (shift + shape / 2) % shape - shape / 2
	return shift


def main(argv):
	ovf1 = readOvf(argv[1])
	ovf2 = readOvf(argv[2])
	if ovf1['config'] != ovf2['config']:
		raise Exception("Two Ovf files have different configurations.")
	config = ovf1['config']
	m1 = ovf1['data']
	m2 = ovf2['data']

	# cut off the source region
	m1 = m1[:, :, 15:85, :]
	m2 = m2[:, :, 15:85, :]
	config['xnodes'] = 70
	config['xbase'] += 15 * config['xstepsize']

	# unzip the configuration
	xnodes, ynodes, znodes = config['xnodes'], config['ynodes'], config['znodes']
	stepsize = xstepsize, ystepsize, zstepsize = config['xstepsize'], config['ystepsize'], config['zstepsize']
	base = xbase, ybase, zbase = config['xbase'], config['ybase'], config['zbase']

	# represent antiferromagnet in the form of ferromagnet
	y, z, x, temp = np.meshgrid(arange(ynodes), arange(znodes), arange(xnodes), [0, 0, 0])
	m1 = where((x + y + z) % 2 == 0, -m1, m1)
	m2 = where((x + y + z) % 2 == 0, -m2, m2)

	# find the translation shift
	z1 = m1[:, :, :, 2]
	z2 = m2[:, :, :, 2]
	shift = phaseCorrelation(z1, z2)
	physical_shift = array([shift[2], shift[1], shift[0]]) * stepsize
	print(physical_shift),

	# find the common region between two vector fields
	shape = m1.shape
	shift = round(shift).astype('int')

	if shift[0] >= 0:
		m1 = m1[:shape[0] - shift[0], :, :, :]
		m2 = m2[shift[0]:, :, :, :]
	else:
		m2 = m2[:shape[0] + shift[0], :, :, :]
		m1 = m1[-shift[0]:, :, :, :]

	if shift[1] >= 0:
		m1 = m1[:, :shape[1] - shift[1], :, :]
		m2 = m2[:, shift[1]:, :, :]
	else:
		m2 = m2[:, :shape[1] + shift[1], :, :]
		m1 = m1[:, -shift[1]:, :, :]

	if shift[2] >= 0:
		m1 = m1[:, :, :shape[2] - shift[2], :]
		m2 = m2[:, :, shift[2]:, :]
	else:
		m2 = m2[:, :, :shape[2] + shift[2], :]
		m1 = m1[:, :, -shift[2]:, :]

	# unzip the magnetization in the common region
	x1 = m1[:, :, :, 0]
	y1 = m1[:, :, :, 1]
	z1 = m1[:, :, :, 2]
	x2 = m2[:, :, :, 0]
	y2 = m2[:, :, :, 1]
	z2 = m2[:, :, :, 2]

#	keypoints = np.where(1.-np.abs(x1) < 0.05, 1, 0)
#	corner_start = np.round(np.array(keypoints.shape)*0.35).astype('int')
#	corner_end = np.round(np.array(keypoints.shape)*0.65).astype('int')
#	drawScalarField(keypoints, corner_start, corner_end)
#	keypoints = array(where(1.-np.abs(x1) < 0.05)).transpose()
	
	theta1 = arctan2(sqrt(1 - z1 * z1), z1)
	theta2 = arctan2(sqrt(1 - z2 * z2), z2)
	phi1 = arctan2(y1, x1)
	phi2 = arctan2(y2, x2)
	angle = phi2 - phi1

	expectation = 0.
	if len(argv) > 3:
		expectation = float(argv[3])
	angle -= round((angle - expectation) / (2 * pi)) * (2 * pi)
	# print(np.where(np.logical_and(abs(angle)>3., abs(z1)<0.95))[0].size)

	weight = where(abs(z1)>0.95, 0., 1.0)
	angle_avg = (angle * weight).sum() / weight.sum()
	#print((angle * weight).sum(), weight.sum())
	print(angle_avg)
	angle = (angle - angle_avg) * weight
#	drawScalarField(clip(angle, -1, 1))
	
#	x2 = sin(theta1) * cos(phi1 + angle_avg)
#	y2 = sin(theta1) * sin(phi1 + angle_avg)
#	z2 = cos(theta1)
#	x1 = x1.flatten()
#	y1 = y1.flatten()
#	z1 = z1.flatten()
#	m1 = array(zip(x1, y1, z1)).reshape(m1.shape)
#	drawVectorField(m1)


if __name__ == "__main__":
	main(sys.argv)
