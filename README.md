# magnon-hopfion
This repository contains codes for both magnon-driven hopfion motion and hopfion-induced magnon motion.
- Magnon motion is calculated using geometric optical method. This method is based on eikonal approximation and applies for magnon with high frequency. Our programs calculate the orbits of spin wave packets (magnons) and predict the momentum transferred from magnons to the hopfion. 
- Hopfion motion is simulated using MuMax3, a micromagnetic simulation software. This repository also contains the codes for hopfions to move freely in 3D space (omnidirectional motion).

## Files
### Hopfion's Omnidirectional Motion.
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

## References
[1] Zhang, Z., Lin, K., Zhang, Y., Bournel, A., Xia, K., Kläui, M., & Zhao, W. (2023). Magnon scattering modulated by omnidirectional hopfion motion in antiferromagnets for meta-learning. Science advances, 9(6), eade7439.
