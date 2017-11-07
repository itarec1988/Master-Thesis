#!/usr/bin/env python

import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot  as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.basemap import Basemap
from maptools import select_map
from copy import copy
import os,sys

biomes_sib=['No biome specified',                     #0
            'Tall Broadleaf-Evergreen Trees',         #1
            'Tall Broadleaf-Deciduous Trees',         #2
            'Tall Broadleaf and Needleleaf Trees',    #3
            'Tall Needleleaf Trees',                  #4
            'Tall Needleleaf-DECIDUOUS Trees',        #5
            'Short Vegetation (Savanna)',             #6
            'Short Vegetation (Grasslands)',          #7 
            'Short Vegetation (None)',                #8
            'Short Broadleaf Shrubs with Bare Soil',  #9
            'Short Ground Cover (Tundra)',            #10
            'No Vegetation (Low Latitude Desert)',    #11
            'Agriculture']                            #12

clrs_sib=['lightgray',     #0
          'green',         #1
          'magenta',       #2
          'orange',        #3
          'darkgreen',     #4
          'yellow',        #5
          'tan',           #6
          'lawngreen',     #7
          'purple',        #8
          'orangered',     #9
          'brown',         #10
          'wheat',         #11
          'darkslateblue'] #12

koppen_names=['Ocean',                                     #0
              'Tropical/Rainforest',                       #1
              'Tropical/Monsoon',                          #2 
              'Tropical/Savannah',                         #3
              'Arid/Desert/Hot',                           #4
              'Arid/Desert/Cold',                          #5
              'Arid/Steppe/Hot',                           #6
              'Arid/Steppe/Cold',                          #7
              'Temperate/Dry_Summer/Hot_Summer',           #8
              'Temperate/Dry_Summer/Warm_Summer',          #9
              'Temperate/Dry_Summer/Cold_Summer',          #10
              'Temperate/Dry_Winter/Hot_Summer',           #11
              'Temperate/Dry_Winter/Warm_Summer',          #12
              'Temperate/Dry_Winter/Cold_Summer',          #13
              'Temperate/Without_dry_season/Hot_Summer',   #14
              'Temperate/Without_dry_season/Warm_Summer',  #15
              'Temperate/Without_dry_season/Cold_Summer',  #16
              'Cold/Dry_Summer/Hot_Summer',                #17
              'Cold/Dry_Summer/Warm_Summer',               #18
              'Cold/Dry_Summer/Cold_Summer',               #19
              'Cold/Dry_Summer/Very_Cold_Summer',          #20
              'Cold/Dry_Winter/Hot_Summer',                #21
              'Cold/Dry_Winter/Warm_Summer',               #22
              'Cold/Dry_Winter/Cold_Summer',               #23
              'Cold/Dry_Winter/Very_Cold_Winter',          #24
              'Cold/Without_dry_season/Hot_Summer',        #25
              'Cold/Without_dry_season/Warm_Summer',       #26
              'Cold/Without_dry_season/Cold_Summer',       #27
              'Cold/Without_dry_season/Very_Cold_Winter',  #28
              'Polar/Tundra',                              #29
              'Polar/Frost']                               #30

clrs_koppen=['white',          #0
             'darkblue',       #1
             'blue',           #2 
             'lightblue',      #3 
             'red',            #4
             'salmon',         #5
             'darkorange',     #6
             'orange',         #7
             'yellow',         #8
             'rosybrown',      #9
             'brown',          #10
             'lightgreen',     #11
             'forestgreen',    #12
             'darkgreen',      #13
             'yellowgreen',    #14
             'limegreen',      #15
             'lawngreen',      #16
             'darkmagenta',    #17
             'magenta',        #18
             'purple',         #19
             'mediumpurple',   #20
             'lavender',       #21
             'violet',         #22
             'darkviolet',     #23
             'dodgerblue',     #24
             'cyan',           #25
             'deepskyblue',    #26
             'lightseagreen',  #27
             'steelblue',      #28
             'lightgray',      #29
             'gray']           #30

biomes_sib_koppen=['No biome specified',                                         #0
                  'Tall Broadleaf-Evergreen Trees, Climate = Trop. Rainforest',  #1
                  'Tall Broadleaf-Evergreen Trees, Climate = Trop. Monsoon',     #2
                  'Tall Broadleaf-Evergreen Trees, Climate = Trop. Savannah',    #3
                  'Tall Broadleaf-Evergreen Trees, Outside South America',       #4
                  'Tall Broadleaf-Deciduous Trees',                              #5
                  'Tall Broadleaf and Needleleaf Trees',                         #6
                  'Tall Needleleaf Trees',                                       #7
                  'Tall Needleleaf-Deciduous Trees',                             #8
                  'Short Vegetation (Savanna)',                                  #9
                  'Short Vegetation (Grasslands)',                               #10 
                  'Short Vegetation (None)',                                     #11
                  'Short Broadleaf Shrubs - Bare Soil',                          #12
                  'Short Ground Cover (Tundra)',                                 #13
                  'No Vegetation (Low Latitude Desert)',                         #14
                  'Agriculture']                                                 #15

biomes_sib_koppen2=['No biome specified',                                         #0
                  'Tall Broadleaf-Evergreen Trees,\nClimate = Trop. Rainforest', #1
                  'Tall Broadleaf-Evergreen Trees,\nClimate = Trop. Monsoon',    #2
                  'Tall Broadleaf-Evergreen Trees,\nClimate = Trop. Savannah',   #3
                  'Tall Broadleaf-Evergreen Trees,\nOutside South America',      #4
                  'Tall Broadleaf-Deciduous Trees',                              #5
                  'Tall Broadleaf and Needleleaf Trees',                         #6
                  'Tall Needleleaf Trees',                                       #7
                  'Tall Needleleaf-Deciduous Trees',                             #8
                  'Short Vegetation (Savanna)',                                  #9
                  'Short Vegetation (Grasslands)',                               #10 
                  'Short Vegetation (None)',                                     #11
                  'Short Broadleaf Shrubs - Bare Soil',                          #12
                  'Short Ground Cover (Tundra)',                                 #13
                  'No Vegetation (Low Latitude Desert)',                         #14
                  'Agriculture']                                                 #15

clrs_sib_koppen=['lightgray',     #0
                 'darkblue',      #1
                 'blue',          #2
                 'lightblue',     #3
                 'green',         #4
                 'magenta',       #5
                 'orange',        #6
                 'darkgreen',     #7
                 'yellow',        #8
                 'tan',           #9
                 'lawngreen',     #10
                 'purple',        #11
                 'orangered',     #12
                 'brown',         #13
                 'wheat',         #14
                 'darkslateblue'] #15


if __name__ == "__main__":

    fig=plt.figure(figsize=(15,8))
    ax=fig.add_axes([0.01,0.1,0.7,0.8])

    #Read Sibcasa biomes
    ff='/Users/ingrid/SiBCASA/sib_param_TI.nc'
    f=cdf.Dataset(ff)
    biomes=f.variables['biome'][:]
    latindex=f.variables['latindex'][:]
    lonindex=f.variables['lonindex'][:]
    f.close()

    #Convert sibcasa-biomes to 1x1
    biomes1x1=np.zeros((180,360),float)
    for i in range(14538):
        lat=latindex[i]
        lon=lonindex[i]
        biomes1x1[lat-1,lon-1]=biomes[i]

    #Read Koppen
    ff='/Users/ingrid/python/code/biome_ecoregions_maps/koppen_climate_map.nc'
    f=cdf.Dataset(ff)
    koppen=f.variables['Band1'][:]
    f.close()
    koppen=koppen[::-1]
    index=[np.ma.getmaskarray(koppen)]
    koppen[index]=0
    index=np.where(koppen == 31)
    koppen[index]=29
    index=np.where(koppen == 32)
    koppen[index]=30

    #Read Transcom regions
    ff='/Storage/CO2/carbontracker/input/ctdas_2012/regions.nc'
    f=cdf.Dataset(ff)
    tc=f.variables['transcom_regions'][:]
    f.close()

    #Find Koppen regions in South America Evergreen forest
    koppen_sam = copy(koppen)
    koppen_sam_adj = copy(koppen)
    for i in range(180):
        for j in range(360):
            if not (tc[i,j] == 3 or tc[i,j] == 4):
                koppen_sam[i,j] = -2
            elif not biomes1x1[i,j] == 1:
                koppen_sam[i,j] = -1
    sam_options = np.unique(koppen_sam)
    sam_options = np.array(sam_options)      
    #print 'Koppen numbers in South America evergreen forest: ', sam_options 
    for i in sam_options:
        counter=np.zeros((180,360))
        index = np.where(koppen_sam == i)
        counter[index]=1
        #print i, counter.sum()

    #For Koppen numbers with very small occurence in evergreen forest, put with the 3 major options (Rainforest, Monsoon, Savannah).
    index = np.where(koppen_sam == 4)
    koppen_sam[index] = 1
    koppen_sam_adj[index] = 1
    index = np.where(koppen_sam == 11)
    koppen_sam[index] = 3
    koppen_sam_adj[index] = 3
    index = np.where(koppen_sam == 12)
    koppen_sam[index] = 3
    koppen_sam_adj[index] = 3
    index = np.where(koppen_sam == 14)
    koppen_sam[index] = 3
    koppen_sam_adj[index] = 3
    index = np.where(koppen_sam == 15)
    koppen_sam[index] = 3
    koppen_sam_adj[index] = 3 
    #The following fills those grid cells that have no Koppen region specified, but do have SiBCASA land cover. The closest attached Koppen region was selected in those cases. This is only used for 5 grid cells.
    index = np.where(koppen_sam == 0)
    koppen_sam[index] = 3
    koppen_sam_adj[index] = 3 
    koppen_sam[88,129] = 2
    koppen_sam_adj[88,129] = 2 

    #Merge Sibcasa biomes with Koppen climate zones for SAM evergreen forest
    sib_plus_koppen = copy(biomes1x1)
    for i in range(180):
        for j in range(360):
            if sib_plus_koppen[i,j] > 0:
                sib_plus_koppen[i,j] = sib_plus_koppen[i,j] + 3 
    index = np.where(koppen_sam == 1)
    sib_plus_koppen[index] = 1
    index = np.where(koppen_sam == 2)
    sib_plus_koppen[index] = 2 
    index = np.where(koppen_sam == 3)
    sib_plus_koppen[index] = 3

    #Amazon mask
    f = cdf.Dataset('/Users/ingrid/python/code/sam/CO2FA.nc')
    gpp = f.variables['gpptot'][:]
    f.close()
    gpp = gpp.mean(axis=0)
    gpp = gpp[::-1]
    mask = np.zeros((360,720))
    mask[138:192,200:270] = gpp
    index = np.where(mask > 0)
    mask[index] = 1

    lons=np.arange(-179.75,180,1)
    lats=np.arange(-89.75,90,1)

    m,nx,ny=select_map('South America Albers')
    m.drawcoastlines(color='grey',linewidth=0.5)
    m.drawcountries(color='grey',linewidth=0.5)
    #m.drawmapboundary(fill_color='#9bcdff')
    #m.fillcontinents(color='#d8d8d8',lake_color='#9bcdff')
    m.drawparallels(np.arange(-90,91,10),color='grey',linewidth=0.5,dashes=[1,0.0001],labels=[1,0,0,0],fontsize=20)
    m.drawmeridians(np.arange(-180,180,15),color='grey',linewidth=0.5,dashes=[1,0.0001],labels=[0,0,0,1],fontsize=20)


    for i in np.arange(120.,200.,1):
        for j in np.arange(200.,290.,1):
            if mask[i,j] == mask[i,j+1]-1:  #West
                y=np.arange(i/2,i/2+1,0.5)-90.
                x=np.zeros(y.shape[0])+j/2-179.5
                line=[x,y]
                linet=m(*line)
                m.plot(linet[0],linet[1],color='white',linewidth=3)
            if mask[i,j] == mask[i,j-1]-1:  #East
                y=np.arange(i/2,i/2+1,0.5)-90.
                x=np.zeros(y.shape[0])+j/2-180
                line=[x,y]
                linet=m(*line)
                m.plot(linet[0],linet[1],color='white',linewidth=3)
            if mask[i,j] == mask[i+1,j]-1:  #South
                x=np.arange(j/2,j/2+1,0.5)-180.
                y=np.zeros(x.shape[0])+i/2-89.5
                line=[x,y]
                linet=m(*line)
                m.plot(linet[0],linet[1],color='white',linewidth=3)
            if mask[i,j] == mask[i-1,j]-1:  #North
                x=np.arange(j/2,j/2+1,0.5)-180.
                y=np.zeros(x.shape[0])+i/2-90
                line=[x,y]
                linet=m(*line)
                m.plot(linet[0],linet[1],color='white',linewidth=3)
    
    labs = ['RPB','SAN','TAB','ALF','RBA','NAT','ABP','TDF']
    lon = [-59.432,-54.95,-70.07,-56.79,-67.6,-35.2603,-38.17,-68.3106]
    lat = [13.165,-2.85,-5.95,-8.92,-9.36,-5.5147,-12.77,-54.8484]
    for i in range(len(labs)):
        x,y = m(lon[i],lat[i])
        if labs[i] == 'TDF':
            xt,yt = m(lon[i]-1,lat[i]+2)
        elif labs[i] == 'TAB' or labs[i] == 'NAT': 
            xt,yt = m(lon[i]-2.5,lat[i]+1.5)
        elif labs[i] == 'SAN':
            xt,yt = m(lon[i]-6,lat[i]-1)
        elif labs[i] == 'RPB' or labs[i] == 'ABP':
            xt,yt = m(lon[i]+2,lat[i]-1)
        elif labs[i] == 'RBA' or labs[i] == 'ALF':
            xt,yt = m(lon[i]+1.6,lat[i]-2)
        else: xt,yt = m(lon[i]-3,lat[i]-4)
        plt.plot(x,y,'o',color='white',markersize=10)
        if labs[i] in ['SAN','TAB']:
            plt.annotate(labs[i],xy=(x,y),xycoords='data',xytext=(xt,yt),fontsize=14,fontweight='bold',color='white')
        else: plt.annotate(labs[i],xy=(x,y),xycoords='data',xytext=(xt,yt),fontsize=14,fontweight='bold',color='black')    
     
    #option='koppen'
    #option='koppen-sam-adj'
    #option='sib'
    option='sib-koppen'
    if option == 'koppen':
        clrs = clrs_koppen
        plotmap = koppen
        maxnr = len(koppen_names)
        labels = koppen_names
        savename = 'Koppen_map.png'
    if option == 'koppen-sam-adj':
        clrs = clrs_koppen
        plotmap = koppen_sam_adj
        maxnr = len(koppen_names)
        labels = koppen_names
        savename = 'Koppen_sam_adj_map.png'
    if option == 'sib':
        clrs = clrs_sib
        plotmap = biomes1x1
        maxnr = len(biomes_sib)
        labels = biomes_sib
        savename = 'Sibcasa_biome_map.png'
    if option == 'sib-koppen':
        clrs = clrs_sib_koppen
        plotmap = sib_plus_koppen
        maxnr = len(biomes_sib_koppen)
        labels = biomes_sib_koppen
        savename = 'Sibcasa_Koppen_biome_map.png'

            
    cmap = mpl.colors.ListedColormap(clrs)
    plotmap = m.transform_scalar(plotmap,lons,lats,nx,ny,order=0)
    im=m.imshow(plotmap,cmap=cmap)
    #im=m.imshow(plotmap,cmap=cmap)
    #im=m.pcolor(x,y,plotmap,cmap=cmap)

    bounds=np.arange(-0.5,maxnr+0.5,1)
    ticks=np.arange(0,maxnr+1,1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.2)
    cbar=plt.colorbar(im,boundaries=bounds,ticks=ticks,cax=cax)
    cbar.ax.set_yticklabels(labels,va='center',fontsize=16)

    fig.savefig('Fig1_%s'%savename)
    plt.show()
