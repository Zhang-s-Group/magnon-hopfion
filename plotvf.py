#!/usr/bin/python

import colorsys
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.figure import figaspect
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import pi, sin, cos, tan

num_scalar_figures = 0
num_vector_figures = 0

def drawScalarField(f, corner_start=[0, 0, 0], corner_end=[-1, -1, -1], stepsize=[1, 1, 1], base=[0, 0, 0]):
    fig = plt.figure(tight_layout=True)
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    z0, y0, x0 = corner_start
    z1, y1, x1 = corner_end
    znodes, ynodes, xnodes = f.shape
    x0 = xnodes + x0 + 1 if x0 < 0 else x0
    y0 = ynodes + y0 + 1 if y0 < 0 else y0
    z0 = znodes + z0 + 1 if z0 < 0 else z0
    x1 = xnodes + x1 + 1 if x1 < 0 else x1
    y1 = ynodes + y1 + 1 if y1 < 0 else y1
    z1 = znodes + z1 + 1 if z1 < 0 else z1

    y = np.arange(y0, y1) * stepsize[1] + base[1]
    z = np.arange(z0, z1) * stepsize[2] + base[2]
    x = np.arange(x0, x1) * stepsize[0] + base[0]
    y, z, x = np.meshgrid(y, z, x)
    f = f[z0:z1, y0:y1, x0:x1]
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    f = f.flatten()

    # f = f**11
    hue = np.where(f > 0, 0, 0.667)
    saturation = np.abs(f)
    alpha = saturation
    rgba = np.zeros(hue.shape + (4,))
    for i, hue1 in enumerate(hue):
        rgba[i] = colors.to_rgba(colorsys.hsv_to_rgb(hue[i], saturation[i], 1), alpha[i])
    ax.scatter(x, y, z, c=rgba, linewidths=1)
    # ax.view_init(elev=30, azim=20)
    ax.set_frame_on(False)

    global num_scalar_figures
    num_scalar_figures += 1
    plt.savefig('sf-' + num_scalar_figures.__repr__() + '.png', dpi=300)



def drawVectorField(m, corner_start=[0, 0, 0], corner_end=[-1, -1, -1], stepsize=[1, 1, 1], base=[0, 0, 0]):
    fig = plt.figure(tight_layout=True)
    ax = fig.add_subplot(1, 1, 1, projection='3d')

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

    y = np.arange(y0, y1) * stepsize[1] + base[1]
    z = np.arange(z0, z1) * stepsize[2] + base[2]
    x = np.arange(x0, x1) * stepsize[0] + base[0]
    y, z, x = np.meshgrid(y, z, x)
    sx, sy, sz = sx[z0:z1, y0:y1, x0:x1], sy[z0:z1, y0:y1, x0:x1], sz[z0:z1, y0:y1, x0:x1]
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    sx = sx.flatten()
    sy = sy.flatten()
    sz = sz.flatten()

    hue = np.arctan2(sy, sx) / (pi * 2) % 1.0
    lightness = np.clip(sz * 0.5 + 0.5, 0, 1)
    alpha = np.clip(1.0 - sz * 1.4, 0, 1)
    rgba = np.zeros(hue.shape + (4,))
    for i, hue1 in enumerate(hue):
        rgba[i] = colors.to_rgba(colorsys.hls_to_rgb(hue[i], lightness[i], 1), alpha[i])
    ax.scatter(x, y, z, c=rgba, linewidths=1)
    # ax.view_init(elev=30, azim=20)
    ax.set_frame_on(False)

    global num_vector_figures
    num_vector_figures += 1
    plt.savefig('vf-' + num_vector_figures.__repr__() + '.png')
    # plt.savefig('vf-' + num_vector_figures.__repr__() + '.png', dpi=300)



def drawHoneycombVectorField(m, corner_start=[0, 0], corner_end=[-1, -1], stepsize=[1, 1], base=[0, 0]):
    y0, x0 = corner_start
    y1, x1 = corner_end
    znodes, ynodes, xnodes, temp = m.shape
    x0 = xnodes + x0 + 1 if x0 < 0 else x0
    y0 = ynodes + y0 + 1 if y0 < 0 else y0
    x1 = xnodes + x1 + 1 if x1 < 0 else x1
    y1 = ynodes + y1 + 1 if y1 < 0 else y1
    
    w, h = (y1-y0) / 10 * figaspect((y1-y0) / (x1-x0 + 0.5*(y1-y0)) * (tan(pi/3) / 2))
    fig = plt.figure(figsize=(w, h), tight_layout=True)
    ax = fig.add_subplot(1, 1, 1)

    sx, sy, sz = m[0, y0:y1, x0:x1, 0], m[0, y0:y1, x0:x1, 1], m[0, y0:y1, x0:x1, 2]
    y = np.arange(y0, y1) * stepsize[1]*sin(pi/3) + base[1]
    x = np.arange(x0, x1) * stepsize[0] + base[0]
    y, x = np.meshgrid(y, x, indexing='ij')
    x += y / tan(pi/3) # Honeycomb
    

    bounds = np.linspace(-1, 1, 65)
    norm = colors.BoundaryNorm(bounds, ncolors=256, clip=True)
    pcm = ax.pcolormesh(x[:, :], y[:, :], sz[:, :], cmap='bwr', shading='nearest', norm=norm)
    q = ax.quiver(x[:, :], y[:, :], sx[:, :], sy[:, :], color='black', width=0.001, scale=1.0/0.01, pivot="mid")
    
    ax.set_frame_on(False)
    ax.set_axis_off()

    global num_vector_figures
    num_vector_figures += 1
    plt.savefig('vf-' + num_vector_figures.__repr__() + '.png')
    # plt.savefig('vf-' + num_vector_figures.__repr__() + '.png', dpi=300)


