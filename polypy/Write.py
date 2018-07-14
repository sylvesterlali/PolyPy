import os as os
import sys as sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import math as mt

import Generic as ge
import Read as rd
import TrajectoryAnalysis as ta
import Write as wr

def msd_plot(msd_data):
    '''
    MSDPlot - Plot MSD 
    
    Parameters 
    ----------
    first  : 1D array
             Timesteps
    second : 1D array
             MSD values
    third  : 1D array
             XMSD values
    fourth : 1D array
             YMSD values
    filth  : 1D array
             ZMSD values
             
    Return
    ------
    matplotlib plot - png
    
    '''
    
    YMax = np.amax(msd_data['msd'])
    XMax = np.amax(msd_data['time'])
    plt.ylim(ymin=0, ymax=YMax)
    plt.xlim(xmin=0, xmax=XMax)
    plt.scatter(msd_data['time'], msd_data['msd'], color="crimson", label="MSD", s=5)
    plt.scatter(msd_data['time'], msd_data['xmsd'], color="blue", label="XMSD",  s=5)
    plt.scatter(msd_data['time'], msd_data['ymsd'], color="black", label="YMSD",  s=5)
    plt.scatter(msd_data['time'], msd_data['zmsd'], color="darkgreen", label="ZMSD",s=5)
    plt.tick_params(labelsize=12)
    
    plt.xlabel("Timestep (ps)", fontsize=15)
    plt.ylabel("MSD", fontsize=15)
    plt.savefig("MSD.png", dpi=600)
    plt.show()
    plt.close()
    
def diffusion_output(DiffusionCo, XDiffusionCo, YDiffusionCo, ZDiffusionCo, conductivity=None):
    '''
    DiffusionOutput - Write out diffusion coefficients to a file
    
    Parameters
    ----------
    first  : float
             Diffusion coefficient
    second : float
             Diffusion coefficient in x
    third  : float
             Diffusion coefficient in y
    fourth : float
             Diffusion coefficient in z
    
    Return
    ------
    Text file
    
    '''
    DiffusionCo = str(DiffusionCo)
    XDiffusionCo = str(XDiffusionCo)
    YDiffusionCo = str(YDiffusionCo)
    ZDiffusionCo = str(ZDiffusionCo)
    Output = open("Diffusion.txt", "w")
    Output.write("3D Diffusion Coefficient: " + DiffusionCo + " m^2/s (10^-9)\n")
    Output.write("2D X Diffusion Coefficient: " + XDiffusionCo + " m^2/s (10^-9)\n")
    Output.write("2D Y Diffusion Coefficient: " + YDiffusionCo + " m^2/s (10^-9)\n")
    Output.write("2D Z Diffusion Coefficient: " + ZDiffusionCo + " m^2/s (10^-9)\n")
    if conductivity:
        con = str(conductivity)
        Output.write("Conductivity: " + con + "(S/cm)\n")
        c = np.log(conductivity)
        c = str(c)
        Output.write("Log of Conductivity: " + c + "log (S/cm)")
    else:       
        Output.close()    

def plane_msd_output(Diffusion, UL, LL, nt, conductivity=None):
    '''
    plane_msd_output - Write out the diffusion coefficient for a region of a configuration to a file
   
    Parameters
    ----------
    first  : numpy object
             Diffusion coefficient 
    second : float
             upper limit of bin
    third  : float
             lower limit of bin
            
    Return 
    ------
    text file
   
  
    '''
    if conductivity:
        conductivity = conductivity 
        l = np.log(conductivity)
        l = str(l)
        C = str(conductivity)

        con = True
    else:
        con = False
    
    UL = str(UL)
    LL = str(LL)
    M = str("-")
    
    D = str(Diffusion)
    nt = str(nt)
    Name = LL + M + UL
    
    Output = open(Name, "w")
    
    Output.write("Diffusion Coefficient within region spanning - " + LL + " - " + UL + " : " + D +  " m^2/s (10^-9)\n")
    if con == True:
            Output.write("Conductivity within region spanning - " + LL + " - " + UL + " : " + C +  " (S cm^-1) \n")
            Output.write("Log of Conductivity within region spanning - " + LL + " - " + UL + " : " + l +  " (log S cm^-1) \n")


    Output.write("Number of Trajectories used: " + nt) 
    Output.close()
 
def one_dimensional_density_sb_output(plane, UL, LL, output):
    
    UL = str(UL)
    LL = str(LL)
    plane = str(plane)
    Output = open(output, "w")
    Output.write("Total Number of species within region spanning - " + LL + " - " + UL + " : " + plane)
    Output.close()
    
   
def line_plot(X, Y, XLab, YLab, output):
    '''
    LinePlot - Simple line plot
    
    Parameters
    ----------
    first  : numpy object
             X axis values
    second : numpy object
             Y axis values
    third  : str
             X label
    fourth : str
             Y label
             
    Return
    ------
    matplotlib plot
    
    '''
        
    plt.plot(X, Y, color="crimson")
    plt.xlabel(XLab, fontsize=13)
    plt.ylabel(YLab, fontsize=13)
    plt.tight_layout()
    plt.tick_params(labelsize=12)
    plt.savefig(output, dpi=600)
    plt.show()
    plt.close()


def contour_plot(X, Y, Z, output, log):
    '''
    CountourPlot - Contour plotting tool
    
    Parameters 
    ----------
    first  : numpy 
             X axis
    second : numpy 
             Y axis
    third  : 2D numpy array
             grid
             
    Return
    ------
    matplotlib plot
    
    '''
    if log == True:
        plt.contourf(X, Y, Z, cmap="Reds", norm = colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
    else:
        plt.contourf(X, Y, Z, cmap="Reds")
    plt.xlabel("X Coordinate (" r'$\AA$' ")", fontsize=15)
    plt.ylabel("Y Coordinate (" r'$\AA$' ")", fontsize=15)
    plt.tick_params(labelsize=12)

    plt.savefig(output, dpi=600)
    plt.show()
    plt.close()
    
def combined_density_plot(X, Y, Y2, Z, output, log):
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    if log == True:
        ax1.contourf(X, Y, Z, cmap="hot", norm = colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
    else:
        ax1.contourf(X, Y, Z, cmap="hot")
    ax1.set_xlabel("X Coordinate (" r'$\AA$' ")", fontsize=15)
    ax1.set_ylabel("Y Coordinate (" r'$\AA$' ")", fontsize=15)
    ax1.set_xlim([np.amin(X), np.amax(X)]) 
    ax1.tick_params(labelsize=12)
    ax2.plot(X, Y2, color="white")
    ax2.set_ylabel("Number Density", fontsize=15)
    ax2.tick_params(labelsize=12)
    plt.show()