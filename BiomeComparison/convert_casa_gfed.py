import netCDF4 as cdf
import os,sys
import h5py as hdf
import numpy as np
import matplotlib.pyplot as plt
from calendar import monthrange,isleap

indir='/Storage/CO2/carbontracker/input/Fires/CASA-GFED4_original_files/'

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
mask1x1 = np.zeros((180,360))
for i in range(180):
    for j in range(360):
        mask1x1[i,j]=mask[i*2,j*2]
mask = np.ma.masked_where(mask == 0,mask)
mask1x1 = np.ma.masked_where(mask1x1 == 0,mask1x1)
#global
#mask1x1=np.zeros((180,360))+1

fac=12./1.e15 #gC/m2/month -> PgC/m2/yr
alldays_fire = []
allmonths_fire = []
allmonths_nbe = []
allmonths_npp = []

for y in range(2000,2001):
    infile=os.path.join(indir,'GFED4.1s_%i.hdf5'%y)
    infile2=os.path.join(indir,'GFED4.1s_%i_Andy.hdf5'%y)
    f=hdf.File(infile,'r')
    f2=hdf.File(infile2,'r')
    #keys=f.keys()

    regions = np.array(f.get('ancill/basis_regions'))[::-1]
    area = np.array(f.get('ancill/grid_cell_area'))[::-1]
    
    if isleap(y): daysinyear = 366 
    else: daysinyear = 365
    
    for m in range(12):
        #if m<>8:continue
        print m+1,y
        daysinmonth = monthrange(y,m+1)[1]
        
        #Monthly emissions and fluxes
        monthly_emis_orig = (np.array(f.get('emissions/%02d/C'%(m+1))))[::-1]*area*fac
        monthly_emis_1x1=np.zeros((180,360),float)
        monthly_npp_orig = (np.array(f.get('biosphere/%02d/NPP'%(m+1))))[::-1]*area*fac
        monthly_rh_orig = (np.array(f2.get('biosphere/%02d/Rh'%(m+1))))[::-1]*area*fac
        monthly_npp_1x1=np.zeros((180,360),float)
        monthly_rh_1x1=np.zeros((180,360),float)
        for i in range(180):
            for j in range(360):
                monthly_emis_1x1[i,j]=monthly_emis_orig[i+i*3:(i+1)*4,j+j*3:(j+1)*4].sum()
                monthly_npp_1x1[i,j]=monthly_npp_orig[i+i*3:(i+1)*4,j+j*3:(j+1)*4].sum()
                monthly_rh_1x1[i,j]=monthly_rh_orig[i+i*3:(i+1)*4,j+j*3:(j+1)*4].sum()
        allmonths_fire.append((monthly_emis_1x1*mask1x1).sum())
        allmonths_npp.append((monthly_npp_1x1*mask1x1).sum())
        allmonths_nbe.append(((-1.*monthly_npp_1x1+monthly_rh_1x1)*mask1x1).sum())
        
        #Daily emissions and fluxes
        '''for d in range(daysinmonth):
            print d+1,m+1,y
            daily_frac = np.array(f.get('emissions/%02d/daily_fraction/day_%i'%(m+1,d+1)))[::-1]
            daily_emis_orig = (np.array(f.get('emissions/%02d/C'%(m+1)))[::-1])*area*daily_frac*fac
            daily_emis_1x1=np.zeros((180,360),float)
            for i in range(180):
                for j in range(360):
                    daily_emis_1x1[i,j]=daily_emis_orig[i+i*3:(i+1)*4,j+j*3:(j+1)*4].sum()
            daily_emis = (daily_emis_1x1)
            alldays_fire.append((daily_emis*mask1x1).sum()*daysinmonth)'''
    f.close()

allmonths_fire = np.array(allmonths_fire)
allmonths_nbe = np.array(allmonths_nbe)
allmonths_npp = np.array(allmonths_npp)
#alldays_fire = np.array(alldays_fire)
#plt.plot(alldays,'bo')
plt.plot(allmonths_nbe,'g-')
#plt.plot(allmonths_fire,'r-')
plt.savefig('test.png')
plt.show()


