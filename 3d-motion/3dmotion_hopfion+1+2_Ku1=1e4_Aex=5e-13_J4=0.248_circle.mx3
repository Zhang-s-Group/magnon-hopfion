CellSize	:= 0.5e-9
SetGridSize(100, 100, 100)
SetCellSize(CellSize, CellSize, CellSize)
DefRegion(1, XRange(24.5e-9, 25e-9))
DefRegion(2, XRange(-25e-9, -24.5e-9))
OpenBC		= true
EnableDemag	= false

// MnSi parameters
Ms		:= 1.51e5
Msat		= Ms
A		:= 0.5e-12
Aex		= -A
//Kc1		= 1e3
//anisC1	= vector(1, 0, 0)
//anisC2	= vector(0, 1, 0)
Ku1		= 1e4
anisU		= vector(0, 0, 1)
alpha		= 0.005
//Dbulk		= 0.115e-3

// Extra Exchange Field (J4)
mx2	:= Shifted(m,2,0,0)
mx_2	:= Shifted(m,-2,0,0)
my2	:= Shifted(m,0,2,0)
my_2	:= Shifted(m,0,-2,0)
mz2	:= Shifted(m,0,0,2)
mz_2	:= Shifted(m,0,0,-2)
laplacian2 := Add(Add(Add(Add(Add(mx2, mx_2), my2), my_2), mz2), mz_2)

Bex	:= A*0.248
BField	:= Mul( Const(-2.0/Ms * Bex/(CellSize*CellSize)), laplacian2)
BEdens	:= Mul( Const(Bex/(CellSize*CellSize)), Dot(laplacian2, m))

AddFieldTerm(BField)
AddEdensTerm(BEdens)

// Spin Configuration
m.LoadFile("stable-state-h+1+2.ovf")

// Spin Wave
// Start the Simulation
B_sw1	:= 2.0
B_sw2	:= 2.0
f_sw	:= 440e9 * 2*pi
f_curve := 2*pi / 10e-9
phi_shift := pi*25./180
B_ext.setRegion(1, Vector(B_sw1 * sin(f_sw*t), B_sw1 * sin(f_sw*t + f_curve*t + phi_shift), 0))
B_ext.setRegion(2, Vector(B_sw2 * sin(f_sw*t), B_sw2 * sin(f_sw*t + f_curve*t - phi_shift), 0))

autosave(m, 5e-11)
run(25e-9)
