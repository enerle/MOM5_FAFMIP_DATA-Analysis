import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'
dirout   = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/Figures'

exp   =     ["prescribed","flux-only"]
filename1 = ["ACC_Blaker_control.nc","ACC_Blaker_flux-only.nc"]
filename2=  ["MOC_Blaker_control.nc","MOC_Blaker_flux-only.nc"]
filename3 = ["OHT_Blaker_control.nc","OHT_Blaker_flux-only.nc"]

factor = 1e-9

letter = ["a","b","c","d","e","f"]

ACC   = [None]*len(exp)
time  = [None]*len(exp)
time2 = [None]*len(exp)

AMOC_41N = [None]*len(exp)
AMOC_26N = [None]*len(exp)
AMOC_30S = [None]*len(exp)
AMOC    = [None]*len(exp)
MOC     = [None]*len(exp)
MOC_GM  = [None]*len(exp)
AMOC_GM  = [None]*len(exp)
DEPTH  = [None]*len(exp)
LAT    = [None]*len(exp)
YY     = [None]*len(exp)
DEPTH2 = [None]*len(exp)
LAT2   = [None]*len(exp)

ATHT = [None]*len(exp)
GLHT = [None]*len(exp)
IPHT = [None]*len(exp)
SOHT = [None]*len(exp)

#---> Get the ACC
for i in range(len(filename1)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    ACC[i] = file.variables['ACC'][:]
    ACC[i] = np.squeeze(ACC[i])
    file.close()

#---> Get the AMOC
for i in range(len(filename2)):  
    fn = os.path.join(datadir,filename2[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time2[i] = file.variables['TIME'][:]/365 -2188.0
    AMOC_41N[i] = file.variables['MOC_41N'][:]
    AMOC_26N[i] = file.variables['MOC_26N'][:]
    AMOC_30S[i] = file.variables['MOC_30S'][:]
    LAT[i]     = file.variables['YU_OCEAN'][:]
    DEPTH[i]   = file.variables['ST_OCEAN'][:]
    AMOC[i]    = file.variables['AMOC'][:,:]
    AMOC_GM[i] = file.variables['AMOC_GM'][:,:]
    MOC[i]     = file.variables['MOC'][:,:]
    MOC_GM[i]  = file.variables['MOC_GM'][:,:]
    file.close()

#---> Get the OHT
PW = 1e-15

for i in range(len(filename3)):  
    fn = os.path.join(datadir,filename3[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    YY[i] = file.variables['YU_OCEAN'][:]
    ATHT[i] = file.variables['ATOHT'][:]*PW
    GLHT[i] = file.variables['GLOHT'][:]*PW
    IPHT[i] = file.variables['IPOHT'][:]*PW
    SOHT[i] = file.variables['SOOHT'][:]*PW
    file.close()

#===============================================================================================
#                            PLOTING
#===============================================================================================

#-----------------------------------------------------------------------
#                       Time series of ACC
###---------------------------------------------------------------------

fontbig    = 20
fontaxis   = 16
fonttitle  = 14
fontsmall  = 12
fonttiny   = 10
font8      = 8
fontlegend = 12
aa = 120
bb = 160
colors = ['green','red','red','blue','black','gray']
styles = ['solid','solid','dashed','solid','solid','solid']

rc('figure', figsize=(11.69,8.27))

fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
for i in range(len(exp)):
    ax.plot(time[i],ACC[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])
ax.grid() 
ax.set_ylabel("ACC [Sv]",fontsize=fontaxis)
ax.set_ylim(-aa,aa)
ax.legend(loc=3,ncol=2, fontsize=fontlegend)
v = [0,70,110,120]
ax.axis(v)
ax.set_xlabel("Time [years]",fontsize=fontaxis)
plt.yticks(fontsize=fontaxis)
plt.xticks(fontsize=fontaxis)
plt.xticks(np.arange(0,80,10))
plt.show()
#plt.savefig("%s/%s" % (dirout,'ACC_ctl.eps'), format='eps',transparent = True)
#plt.savefig('./Figures/ACC_ctl.png',transparent = True, bbox_inches='tight',dpi=600)

#-----------------------------------------------------------------------
#                       Time series of AMOC
###--------------------------------------------------------------------
aa = 14
bb = 22

rc('figure', figsize=(11.69,8.27))

fig = plt.figure(3)
ax = fig.add_subplot(1,1,1)               
for i in range(len(exp)):
    ax.plot(time2[i],AMOC_41N[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])
ax.grid()
ax.set_ylabel("AMOC [Sv]",fontsize=fonttitle)
ax.legend(loc=3,ncol=2, fontsize=fontsmall)
v = [0,70,15,22]
ax.axis(v)
ax.set_xlabel("Time [years]",fontsize=fontaxis)
plt.yticks(fontsize=fontaxis)
plt.xticks(fontsize=fontaxis)
plt.xticks(np.arange(0,80,10))
#plt.show()
plt.savefig("%s/%s" % (dirout,'AMOC41N_ctl.eps'), format='eps',transparent = True)

###

fig = plt.figure(5)
ax = fig.add_subplot(1,1,1)
for i in range(len(exp)):
    ax.plot(time2[i],AMOC_26N[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])
ax.grid()
ax.set_ylabel("AMOC [Sv]",fontsize=fonttitle)
ax.legend(loc=3,ncol=2, fontsize=fontsmall)
v = [0,70,15,22]
ax.axis(v)
ax.set_xlabel("Time [years]",fontsize=fontaxis)
plt.yticks(fontsize=fontaxis)
plt.xticks(fontsize=fontaxis)
plt.xticks(np.arange(0,80,10))
plt.show()
#plt.savefig("%s/%s" % (dirout,'AMOC26N_ctl.eps'), format='eps',transparent = True)

##

fig = plt.figure(7)
ax = fig.add_subplot(1,1,1)
for i in range(len(exp)):
    ax.plot(time2[i],AMOC_30S[i],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])
ax.grid()
ax.set_ylabel("AMOC [Sv]",fontsize=fonttitle)
ax.legend(loc=3,ncol=2, fontsize=fontsmall)
v = [0,70,15,22]
ax.axis(v)
ax.set_xlabel("Time [years]",fontsize=fontaxis)
plt.yticks(fontsize=fontaxis)
plt.xticks(fontsize=fontaxis)
plt.xticks(np.arange(0,80,10))
#plt.show()
plt.savefig("%s/%s" % (dirout,'AMOC30S_ctl.eps'), format='eps',transparent = True)

#			Atlantic MOC
###---------------------------------------------------------------------

#cmap = plt.cm.bwr
cmap = plt.cm.RdBu_r

kmin = -30
kmax = 30
clevs_a = np.arange(kmin,kmax+1.0,1.0)
clevs_b = np.arange(kmin/2,(kmax/2)+1.0,1.0)
clevs   = np.arange(-20,22,2)
v= [-30,90,0,5500]

rc('figure', figsize=(8.27,11.69))
fig = plt.figure(9)
for i in range(len(exp)):
    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(8,1,i+1)
    cs = plt.contourf(LAT2[i],DEPTH2[i],AMOC[i],levels=clevs_a,cmap=cmap,extend='both')
    cc = plt.contour (LAT2[i],DEPTH2[i],AMOC[i],levels=clevs_a,colors='k',linewidths=0.25)
    plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=fonttiny)
    plt.clim(kmin,kmax)
    plt.annotate(exp[i],xy=(60,5000),fontsize=fonttiny,color='k')
    plt.axis(v)
    plt.yticks(fontsize=fonttiny)
    plt.xticks(fontsize=fonttiny)
    
    ax.tick_params(labelbottom='off')
    ax.tick_params(direction='out')
    ax.set_ylabel('Depth (m)', fontsize=fonttiny)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(8,1,3)
cs = plt.contourf(LAT2[i],DEPTH2[i],AMOC[0]-AMOC[1],levels=clevs_a,cmap=cmap,extend='both')
cc = plt.contour (LAT2[i],DEPTH2[i],AMOC[0]-AMOC[1],levels=clevs_a,colors='k',linewidths=0.25)

plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=fonttiny)
plt.clim(kmin,kmax)
plt.annotate("Diff",xy=(60,5000),fontsize=fonttiny,color='k')
plt.axis(v)
plt.yticks(fontsize=fonttiny)
plt.xticks(fontsize=fonttiny)
plt.xticks([-20,0,20,40,60,80],['20S', '0', '20N', '40N', '60S','80S'])
ax.tick_params(labelbottom='off')
ax.set_ylabel('Depth (m)', fontsize=fonttiny)
ax.tick_params(direction='out')
ax.set_xlabel("Latitude", fontsize=fonttiny)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#Add a colorbar and adjust.
cbar_ax = axes([0.90, 0.35, 0.02, 0.3])
cbar = plt.colorbar(cs, cax=cbar_ax,extend='both',orientation='vertical')
cbar.set_label('Sv', rotation=0, size=fonttiny)

plt.subplots_adjust(hspace = .1, wspace = .1, bottom = 0.15,right=.85,left=.1)
plt.show()
#plt.savefig('./Figures/AMOC_ctl.eps',format='eps',transparent = True)

#----------------------------------------------------------------------- 
#			Global MOC
###---------------------------------------------------------------------
cmap = plt.cm.RdBu_r
cmap.set_bad(color = 'k', alpha = 1.)

clevs = np.arange(-40,40,4)
v= [-80,90,0,5500]

rc('figure', figsize=(8.27,11.69))
fig = plt.figure(10)

for i in range(len(exp)):
    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(8,1,i+1)
    cs = plt.contourf(LAT2[i],DEPTH2[i],MOC[i],levels=clevs_a,cmap=cmap,extend='both')
    cc = plt.contour (LAT2[i],DEPTH2[i],MOC[i],levels=clevs_a,colors='k',linewidths=0.25)
    
    plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=fonttiny)
    plt.clim(kmin,kmax)
    plt.annotate(exp[i],xy=(60,5000),fontsize=fonttiny,color='k')
    plt.axis(v)
    plt.yticks(fontsize=fonttiny)
    plt.xticks(fontsize=fonttiny)
    ax.tick_params(labelbottom='off')
    ax.tick_params(direction='out')
    ax.set_ylabel('Depth (m)', fontsize=fonttiny)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(8,1,3)
cs = plt.contourf(LAT2[i],DEPTH2[i],MOC[0]-MOC[1],levels=clevs_a,cmap=cmap,extend='both')
cc = plt.contour (LAT2[i],DEPTH2[i],MOC[0]-MOC[1],levels=clevs_a,colors='k',linewidths=0.25)

plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=fonttiny)
plt.clim(kmin,kmax)
plt.annotate("diff",xy=(60,5000),fontsize=fonttiny,color='k')
plt.axis(v)
plt.yticks(fontsize=fonttiny)
plt.xticks(fontsize=fonttiny)
plt.xticks([-60,-40,-20,0,20,40,60,80],['60S','40S','20S', '0', '20N', '40N', '60S','80S'])
ax.tick_params(labelbottom='off')
ax.set_ylabel('Depth (m)', fontsize=fonttiny)
ax.tick_params(direction='out')
ax.set_xlabel("Latitude", fontsize=fonttiny)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#Add a colorbar and adjust.
cbar_ax = axes([0.90, 0.35, 0.02, 0.3])
cbar = plt.colorbar(cs, cax=cbar_ax,extend='both',orientation='vertical')
cbar.set_label('Sv', rotation=0, size=fonttiny)

#plt.subplots_adjust(hspace = .1, wspace = .1, bottom = 0.15,right=.85,left=.1)
plt.show()
#plt.savefig('./Figures/GMOC_ctl.eps',format='eps',transparent = True)

#-----------------------------------------------------------------------
#		Plot OHT
#-----------------------------------------------------------------------

rc('figure', figsize=(11.69,8.27))

fig = plt.figure(11)

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)):
    ax.plot(YY[i],GLHT[i], color=colors[i],linewidth=1.5,linestyle=styles[i],label = exp[i])
    # plt.text(-60,1-0.2*i,'(%s) %s '%(letter[i], exp[i], fontsize=fonttitle, style='italic')
plt.title('Global',fontsize=fontaxis, style='normal')
ax.grid() 
ax.legend(loc=3,fontsize=font8, frameon=False)
v = [-90,90,-2.0,2.0]
ax.axis(v)
ax.set_ylabel("OHT anomalies [PW]",fontsize=fonttitle)
plt.yticks(fontsize=fontlegend)
plt.xticks(fontsize=fontlegend)
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'])

ax = fig.add_subplot(2,2,2)
for i in range(len(exp)):
    ax.plot(YY[i],ATHT[i], color=colors[i],linewidth=1.5,linestyle=styles[i],label = exp[i])
# plt.text(-20,1-0.2*i,'(%s) %s '%(letter[i], exp[i], fontsize=fonttitle, style='italic')
plt.title('Atlantic',fontsize=fontaxis, style='normal')
ax.grid()
ax.legend(loc=3,fontsize=font8, frameon=False)
v = [-90,90,-2.0,2.0]
ax.axis(v)
plt.yticks(fontsize=fontlegend)
plt.xticks(fontsize=fontlegend)
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'])

ax = fig.add_subplot(2,2,3)
for i in range(len(exp)):
    ax.plot(YY[i],IPHT[i], color=colors[i],linestyle=styles[i],linewidth=1.5,label = exp[i])
plt.title('IndoPacific',fontsize=fontaxis, style='normal')
ax.grid()
ax.legend(loc=1,fontsize=font8, frameon=False)
v = [-40,80,-2.0,2.0]
ax.axis(v)
ax.set_xlabel("Latitude",fontsize=fonttitle)
ax.set_ylabel("OHT anomalies [PW]",fontsize=fonttitle)
plt.yticks(fontsize=fontlegend)
plt.xticks(fontsize=fontlegend)
plt.xticks([-40,-20,0,20,40,60,80],['40S','20S','0','20N','40N','60N','80N'])
#

ax = fig.add_subplot(2,2,4)
for i in range(len(exp)):
    ax.plot(YY[i],SOHT[i],color=colors[i],linestyle=styles[i],linewidth=1.5,label = exp[i])
plt.title('Southern Ocean',fontsize=fontaxis,style='normal')
ax.grid()
ax.legend(loc=2,fontsize=font8, frameon=False)
v = [-80,-30,-2.0,2.0]
ax.axis(v)
ax.set_xlabel("Latitude",fontsize=fonttitle)
plt.yticks(fontsize=fontlegend)
plt.xticks(fontsize=fontlegend)
plt.xticks([-80,-70,-60,-50,-40,-30],['80S','70S','60S','50S','40S','30S'])

plt.show()
#plt.savefig('./Figures/OHT_ctl.eps',format='eps',transparent = True)
