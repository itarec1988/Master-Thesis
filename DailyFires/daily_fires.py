#!/usr/bin/env python3

import sys
import os
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
import netCDF4 as cdf 
import numpy as np
import pylab as plb
from tm5tools import globarea
import calendar

biofireparamdirs=[
'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr/', #SiBCASA-GFED4
'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr_gfas_fires/', #GFAS
#'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr_finn_fires/', #FINN
#'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/casa-gfed4-3h-fires-monthly-bio/', #CASA-GFED4 fires 3h
#'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/casa-gfed4-daily-fires-monthly-bio/',#CASA-GFED4 fires daily
]

labels = ['SiBCASA-GFED4','GFAS','FINN']
colors_bf = ['red','orange','green','purple','blue','grey']
#colors_bf = ['red','orange','limegreen','deepskyblue','mediumpurple']

fig = plt.figure(1,figsize=(15,8))
ax = fig.add_axes([0.1,0.2,0.8,0.7])
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

glarea = globarea(im=720,jm=360)
glarea2 = globarea(im=360,jm=180)
fac = 86400.*365.*12./1.e15
fac_gfas = 86400.*365.*12./(44.01*1.e12)

#Amazon mask
f = cdf.Dataset('CO2FA.nc')
gpp = f.variables['gpptot'][:]
f.close()
gpp = gpp.mean(axis=0)
gpp = gpp[::-1]
mask = np.zeros((360,720))
mask[138:192,200:270] = gpp
index = np.where(mask > 0)
mask[index] = 1
test_mask = np.zeros((180,360))
for i in range(180):
    for j in range(360):
        test_mask[i,j]=mask[i*2,j*2]
mask = np.ma.masked_where(mask == 0,mask)
test_mask = np.ma.masked_where(test_mask == 0,test_mask)

test = True 
priors = True 
daily = True  #(False = yearly) 
if not daily:
    minyear = 2001
else: minyear = 2010   
if priors:
    for ii,dirbf in enumerate(biofireparamdirs):
        if daily and not 'daily' in dirbf: continue
        print dirbf
        alltimes = []
        allbb = []
        if not daily:
            if 'sibcasa_gfed3' in dirbf:
                maxyear = 2011
            if 'gfas' in dirbf or 'finn' in dirbf:   
                maxyear = 2013 
            else: maxyear = 2012
        else: maxyear = 2012
        for y in range(minyear,maxyear):
            if calendar.isleap(y):
                days_in_y = 366
            else: days_in_y = 365
            included_check = False        
            for fname in os.listdir(dirbf):
                if not int(fname[-9:-5]) == y: continue
                included_check = True
                print fname
                bf = cdf.Dataset(dirbf+fname)
                if 'co2fire' in bf.variables.keys():
                    bb = np.float32(bf.variables['co2fire'][:])
                else: bb = bf.variables['bb'][:]
                if bb.shape[0] == 180: 
                    bb.resize(1,180,360)
                if bb[0,0,0] is np.ma.masked:
                    bb[bb.mask] = 0
                if daily:
                    m = int(fname[-5:-3])
                    days = calendar.monthrange(y,m)[1]
                    for d in range(1,days+1):
                        dd = dt.datetime(y,m,d,0,0)
                        #print dd
                        alltimes.append(dd)
                        #alltimes.append((float(dd.strftime("%j"))-1) / days_in_y + float(dd.strftime("%Y")))
                        bb_sum = bb[(d-1)*8:d*8,:,:].mean(axis=0)
                        if test:
                            allbb.append((bb_sum*test_mask*glarea2*fac).sum())
                        else: 
                            bb2=np.zeros((360,720))
                            for i in range(360):
                                 for j in range(720):
                                     bb2[i,j] = bb_sum[round(i/2),round(j/2)]
                            allbb.append((bb2*mask*glarea*fac).sum())
                else:
                    if int(fname[-5:-3]) == 1: 
                        dd = dt.datetime(y,7,1,0,0)
                        alltimes.append((float(dd.strftime("%j"))-1) / days_in_y + float(dd.strftime("%Y")))
                        bb_sum = bb
                    else: bb_sum = np.append(bb_sum,bb,axis=0)
                bf.close()   
            if included_check and not daily:
                bb_sum = bb_sum.mean(axis=0)
                if test:
                    allbb.append((bb_sum*test_mask*glarea2*fac).sum())
                else:    
                    bb2=np.zeros((360,720))
                    for i in range(360):
                         for j in range(720):
                             bb2[i,j] = bb_sum[round(i/2),round(j/2)]
                    allbb.append((bb2*mask*glarea*fac).sum())
               
        alltimes = np.array(alltimes)
        allbb = np.array(allbb)
        ax.plot(alltimes,allbb,label=labels[ii],lw=4,color=colors_bf[ii],zorder=10-ii)
        #ax.plot(alltimes,allbb,label=dirbf.split('/')[7],lw=4,color=colors_bf[ii],zorder=10-ii)

if not daily:
    ax.plot([2010.5,2011.5],[0.51,0.30],'x',label='Gatti et al. (2014)',color='black',zorder=10,markersize=16,mew=4)

if daily:
    ymax = 6
    ax.set_xlim(dt.date(minyear,1,1),dt.date(maxyear,1,1))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b\n%Y'))
    ax.grid(True, ls='-', color='0.75')
else: 
    ymax = 0.8
    ax.set_xticks(np.arange(minyear+0.5,maxyear+0.5,1).tolist())
    ax.set_xticklabels([str(l) for l in range(minyear,maxyear)])
    ax.set_xlim(minyear,maxyear)
    ax.yaxis.grid(True, ls='-', color='0.75')
ax.set_ylim(0,ymax)
for i in range(minyear,maxyear,2):
    sd = i
    ed = i+1
    plt.fill([sd,ed,ed,sd],[0,0,ymax,ymax],color="0.8",zorder=0)
ax.set_ylabel('Biomass burning CO$_2$ flux [PgC/yr]',fontsize=20)
dummy=[lab.set_fontsize(20) for lab in ax.get_xticklabels()]
dummy=[lab.set_fontsize(20) for lab in ax.get_yticklabels()]
ax.tick_params(axis='x', pad=12)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
if daily:
    ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.14),ncol=2,prop={'size':16})
    fig.savefig('Fig2_Daily_fires_2010-2011.png')
else: 
    ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.14),ncol=3,prop={'size':16})
    fig.savefig('Yearly_fires_2001-2012.png')
plt.show()


