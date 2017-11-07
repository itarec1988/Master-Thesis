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
from Fig1_biomes_sibcasa_plus_koppen_globe import biomes_sib_koppen

biofireparamdirs=[
'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr/',
'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr_optimized_fires_withprofiles/',
'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr_gfas_fires/',
'/Storage/CO2/carbontracker/input/ctdas_2012/biosphere/gfed4_daily_sibcasa_3hr_finn_fires/',
]

gfasfile='/Users/ingrid/GFASv1_co2fire_0003.nc'

labels = ['SiBCASA-GFED4','SiBCASA-GFED4 optimized fires', 'SiBCASA-GFED3', 'CASA-GFED3', 'GFAS']
colors_bf = ['red','orange','green','purple','blue','grey']
clrs_sib_koppen=['darkblue','blue','lightblue','green','magenta','orange','darkgreen','yellow','tan','lawngreen','purple','orangered','brown','wheat','darkslateblue']

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

#Biome mask
f = cdf.Dataset('/Storage/CO2/carbontracker/input/ctdas_2012/regions_sibcasa_koppen_sam.nc')
tc = f.variables['transcom_regions'][:]
land_eco = f.variables['land_ecosystems'][:]
f.close()
land_eco[np.where(land_eco.mask)] = 0
sam = np.zeros((360,720))
biomes = np.zeros((360,720))
for i in range(360):
    for j in range(720):
        sam[i,j] = tc[round(i/2),round(j/2)]
        biomes[i,j] = land_eco[round(i/2),round(j/2)]
index = np.where(sam <> 3)
sam[index] = 0
index = np.where(sam <> 0)
sam[index] = 1
sam = np.ma.masked_where(sam == 0,sam)
biomes = np.ma.masked_where(sam == 0,biomes)
biomes = np.ma.masked_where(biomes == 0,biomes)

fig=plt.figure(1,figsize=(19,10))
ax1=plt.subplot(231)
ax1.set_title('SiBCASA-GFED4 prior',fontsize=30)
ax2=plt.subplot(234)
ax2.set_title('SiBCASA-GFED4 opt. IASI + profiles ',fontsize=30)
ax3=plt.subplot(232)
ax3.set_title('GFAS',fontsize=30)
ax4=plt.subplot(235)
ax4.set_title('FINN',fontsize=30)

biomes_seperate_years = False
minyear = 2010
maxyear = 2012
for ii,dirbf in enumerate(biofireparamdirs):
    print dirbf
    alltimes = []
    allbb = []
    for y in range(minyear,maxyear):
        if calendar.isleap(y):
            days_in_y = 366
        else: days_in_y = 365    
        for fname in os.listdir(dirbf):
            if not int(fname[-9:-5]) == y: continue
            print fname    
            bf = cdf.Dataset(dirbf+fname)
            if 'co2fire' in bf.variables.keys():
                bb = np.float32(bf.variables['co2fire'][:])
            else: bb = bf.variables['bb'][:]
            if bb.shape[0] == 180: 
                bb.resize(1,180,360)
            if int(fname[-5:-3]) == 1: 
                dd = dt.datetime(y,7,1,0,0)
                alltimes.append((float(dd.strftime("%j"))-1) / days_in_y + float(dd.strftime("%Y")))
                bb_sum = bb
            else: bb_sum = np.append(bb_sum,bb,axis=0)   
            bf.close()    
        bb_sum = bb_sum.mean(axis=0)
        bb2=np.zeros((360,720))
        for i in range(360):
             for j in range(720):
                 bb2[i,j] = bb_sum[round(i/2),round(j/2)]
        allbb.append((bb2*mask*glarea*fac).sum())
        #Biomes
        mask = mask #For Amazon
        #mask = sam  #For total SAM
        if biomes_seperate_years:
            for b in range(1,16,1):
                indexb = np.where(biomes*mask == b)
                if len(indexb[0]) == 0:
                    print '%i: %+5.4f (%i) %s'%(y,0,0,biomes_sib_koppen[b])
                else:
                    print '%i: %+5.4f (%i) %s'%(y, (bb2*mask*glarea*fac)[indexb].sum(),((bb2*mask*glarea*fac)[indexb].sum()/(bb2*mask*glarea*fac).sum())*100,biomes_sib_koppen[b])
        else:
            if y == 2010:
                bb_biomes = bb2
                print '%i: %+5.4f'%(y,(bb_biomes*mask*glarea*fac).sum())
            if y == 2011:
                bb_biomes = bb_biomes + bb2
                print '%i: %+5.4f'%(y,(bb2*mask*glarea*fac).sum())
                print '2010 + 2011: %+5.4f'%(bb_biomes*mask*glarea*fac).sum()
                pie_list = []
                for b in range(1,16,1):
                    indexb = np.where(biomes*mask == b)
                    if len(indexb[0]) == 0:
                        print '%i: %+5.4f (%i) %s'%(y,0,0,biomes_sib_koppen[b])
                        pie_list.append(0)
                    else:
                        print '%i: %+5.4f (%i) %s'%(y, (bb_biomes*mask*glarea*fac)[indexb].sum(),((bb_biomes*mask*glarea*fac)[indexb].sum()/(bb_biomes*mask*glarea*fac).sum())*100,biomes_sib_koppen[b])
                        pie_list.append(((bb_biomes*mask*glarea*fac)[indexb].sum()/(bb_biomes*mask*glarea*fac).sum())*100)
                print pie_list
                if ii == 0:
                    ax1.pie(pie_list,colors=clrs_sib_koppen,startangle=90,shadow=True)
                if ii == 1:
                    ax2.pie(pie_list,colors=clrs_sib_koppen,startangle=90,shadow=True)
                if ii == 2:
                    ax3.pie(pie_list,colors=clrs_sib_koppen,startangle=90,shadow=True)
                if ii == 3:
                    ax4.pie(pie_list,colors=clrs_sib_koppen,startangle=90,shadow=True)
                                  
#Now gfas:
'''maxyear = 2012
print 'gfas'
alltimes = []
allbb = []
index1 = 0
index2 = 0
f = cdf.Dataset(gfasfile)
for y in range(minyear,maxyear):
    print y
    if calendar.isleap(y):
        days_in_y = 366
    else: days_in_y = 365
    mindate = dt.datetime(y,1,1,0,0)
    timediff = (dt.datetime(y,1,1,0,0) - dt.datetime(2003,1,1,0,0)).days
    nr = 1    
    for r in range(nr):
        index1 = timediff + r
        index2 = index1 + days_in_y
        time = f.variables['time'][index1:index2]
        gfas = f.variables['co2fire'][index1:index2]
        west = gfas[:,:,360:]
        east = gfas[:,:,:360]
        gfas = np.concatenate((west,east),axis=2)
        dd = dt.datetime(y,7,1,0,0)
        alltimes.append((float(dd.strftime("%j"))-1) / days_in_y + float(dd.strftime("%Y")))
        allbb.append((gfas.mean(axis=0)*mask*glarea*fac_gfas).sum())
        #Biomes
        mask = mask #For Amazon
        #mask = sam  #For total SAM
        if biomes_seperate_years:
            for b in range(1,16,1):
                indexb = np.where(biomes*mask == b)
                if len(indexb[0]) == 0:
                    print '%i: %+5.4f (%i) %s'%(y,0,0,biomes_sib_koppen[b])
                else:
                    print '%i: %+5.4f (%i) %s'%(y, (gfas.mean(axis=0)*mask*glarea*fac_gfas)[indexb].sum(),((gfas.mean(axis=0)*mask*glarea*fac_gfas)[indexb].sum()/(gfas.mean(axis=0)*mask*glarea*fac_gfas).sum())*100,biomes_sib_koppen[b])
        else:            
            if y == 2010:
                bb_biomes_gfas = gfas.mean(axis=0) 
                print '%i: %+5.4f'%(y,(bb_biomes_gfas*mask*glarea*fac_gfas).sum())
            if y == 2011:    
                bb_biomes_gfas = bb_biomes_gfas + gfas.mean(axis=0)
                print '%i: %+5.4f'%(y,(gfas.mean(axis=0)*mask*glarea*fac_gfas).sum())
                print '2010 + 2011: %+5.4f'%(bb_biomes_gfas*mask*glarea*fac_gfas).sum()
                pie_list = []
                for b in range(1,16,1):
                    indexb = np.where(biomes*mask == b)
                    if len(indexb[0]) == 0:
                        print '%i: %+5.4f (%i) %s'%(y,0,0,biomes_sib_koppen[b])
                        pie_list.append(0)
                    else:
                        print '%i: %+5.4f (%i) %s'%(y, (bb_biomes_gfas*mask*glarea*fac_gfas)[indexb].sum(),((bb_biomes_gfas*mask*glarea*fac_gfas)[indexb].sum()/(bb_biomes_gfas*mask*glarea*fac_gfas).sum())*100,biomes_sib_koppen[b])
                        pie_list.append(((bb_biomes_gfas*mask*glarea*fac_gfas)[indexb].sum()/(bb_biomes_gfas*mask*glarea*fac_gfas).sum())*100)
                ax3=plt.subplot(143)
                ax3.set_title('GFAS',fontsize=20)
                ax3.pie(pie_list,colors=clrs_sib_koppen,startangle=90,shadow=True)
                print pie_list

f.close()'''
    
ax1.axis('equal') 
ax2.axis('equal') 
ax3.axis('equal')
ax4.axis('equal')

ax4.legend(biomes_sib_koppen[1:],loc='center left', bbox_to_anchor=(1, 1.2))
leg = plt.gca().get_legend()
ltext  = leg.get_texts()
plt.setp(ltext, fontsize='23') 
fig.savefig('Fig3_Biome_percentages_2010-2011.png')
plt.show()

