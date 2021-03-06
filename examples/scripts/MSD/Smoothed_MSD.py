from polypy import read as rd
from polypy import msd as msd
from polypy import utils as ut
from polypy import write as wr
import numpy as np

data = rd.read_history("../example_data/HISTORY", ["F"])

timestep = 0.1
smsd_data = msd.smooth_msd(data, timestep, runs=10)

Diff = ut.linear_regression(smsd_data['time'], smsd_data['msd'])[0]
Diffusion_Coefficient = ut.three_d_diffusion_coefficient(Diff)

XDiff = ut.linear_regression(smsd_data['time'], smsd_data['xmsd'])[0]
XDiffusion_Coefficient = ut.three_d_diffusion_coefficient(XDiff)

YDiff = ut.linear_regression(smsd_data['time'], smsd_data['ymsd'])[0]
YDiffusion_Coefficient = ut.three_d_diffusion_coefficient(YDiff)

ZDiff = ut.linear_regression(smsd_data['time'], smsd_data['zmsd'])[0]
ZDiffusion_Coefficient = ut.three_d_diffusion_coefficient(ZDiff)

print("Three Dimensional Diffusion Coefficient", Diffusion_Coefficient, "")
print("One Dimensional Diffusion Coefficient in X", XDiffusion_Coefficient)
print("One Dimensional Diffusion Coefficient in Y", YDiffusion_Coefficient)
print("One Dimensional Diffusion Coefficient in Z", ZDiffusion_Coefficient)

wr.msd_plot(smsd_data)
wr.msd_plot(smsd_data, fit=True)

volume, time = ut.system_volume(data, timestep)

wr.volume_plot(time, volume)

Average_Volume = np.mean(volume[100:])

Number_of_Charge_Carriers = data['natoms']
Ionic_Conductivity = ut.conductivity(Number_of_Charge_Carriers, Average_Volume, Diffusion_Coefficient, 1500)
print("Ionic Conductivity :", Ionic_Conductivity)
print("Resistivity :", (1 / Ionic_Conductivity)) 

