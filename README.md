# magnon-hopfion
Geometric Optical Method for Magnon-Hopfion Interaction. The package also includes the micromagnetic simulation code for hopfions to move freely in 3D space (omnidirectional motion).

## Files
### Hopfion's omnidirectional motion.
- "ovf.py" is a package used to deal with the Vector Field File Format (OVF)
- "plotvf.py" is a package used to plot OVF files.
- Programs in "samples" exemplifies the usage of these two packages.
- "3d-motion" contains the MuMax3 files simulating the omnidirectional motion of the hopfion.
- "track.py" locates the hopfion in the space.
- "track.sh" exemplifies the usage of "track.py"

### Magnon orbits and Momentum Transfer.
- "udf/m-equiv.ovf" is the spin configuration
- "scatter.py" calculates the momentum transferred from magnons to the hopfion for various wavnumbers.
- "orbit.py" calculates the magnon orbits.
- "orbit2png.py" shows the magnon orbits in a picture containing the F field.
- "orbit2png.sh" exemplifies the usage of "orbits2png.py".
