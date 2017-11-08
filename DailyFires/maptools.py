#!/usr/bin/env python
from mpl_toolkits.basemap import Basemap, shiftgrid
from pylab import *
import cPickle
#import mysettings
import os


def select_map(maptype):
    """ Function returns a Basemap instance with a chosen projection
        Valid choices are:
    
    if   maptype == 'North America Albers':   
    elif maptype == 'Global Cylinder':    
    elif maptype == 'US Conformal':    
    elif maptype == 'North America Ortho':    
    elif maptype == 'Europe Albers':   
    elif maptype == 'Europe Ortho':    
    elif maptype == 'Europe Conformal':    
    elif maptype == 'EurAsia Albers': 
    elif maptype == 'EurAsia Cylinder': 
    elif maptype == 'Polar Stereo':    
    elif maptype == 'South America Albers':    
    elif maptype == 'America Africa Albers':    
    elif maptype == 'Moscow Albers':    
    elif maptype == 'Netherlands Albers':
    elif maptype == 'Netherlands Albers Lies':
    elif maptype == 'Netherlands Albers Zoom':  """

    if maptype == 'North America Albers':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','NorthAmerica_Albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 10.0
            urcrnrlat = 75.0
            llcrnrlon = -125.0
            urcrnrlon = -30.0
            standardpar = 24.5
            standardpar2 = 51.5
            centerlon=-90.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    elif maptype == 'Global Cylinder':    
        mapfile = os.path.join('/Users/botia','biomecomparison','GlobalCylinder.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup cylindrical equidistant map projection (global domain).
            m = Basemap(llcrnrlon=-180.,llcrnrlat=-90,urcrnrlon=180.,urcrnrlat=90.,\
                        resolution='l',area_thresh=10000.,projection='cyl')
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = 360 ; ny=180

    elif maptype == 'EurAsia Cylinder':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','EurAsiaCylinder.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup cylindrical equidistant map projection (global domain).
            m = Basemap(llcrnrlon=-10.,llcrnrlat=20,urcrnrlon=180.,urcrnrlat=90.,\
                        resolution='c',area_thresh=10000.,projection='cyl')
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = 190 ; ny = 70


    elif maptype == 'US Conformal':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','US_Conformal.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            llcrnrlat = 22.0
            urcrnrlat = 48.0
            latminout = 22.0
            llcrnrlon = -125.0
            urcrnrlon = -60.0
            standardpar = 50.0
            centerlon=-105.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='lcc',
                        lat_1=standardpar,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    elif maptype == 'North America Ortho':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','NorthAmericaOrtho.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup of basemap ('ortho' = orthographic projection)
            m = Basemap(projection='ortho',
                        resolution='c',area_thresh=10000.,lat_0=40,lon_0=-90)
            # transform to nx x ny regularly spaced native projection grid
            #dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        # nx and ny chosen to have roughly the same horizontal res as original image.
        dx = 2.*pi*m.rmajor/360
        nx = int((m.xmax-m.xmin)/dx)+1; ny = int((m.ymax-m.ymin)/dx)+1

    if maptype == 'Europe Albers':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','Europe_albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 28.0
            urcrnrlat = 66.0
            llcrnrlon = -7.0
            urcrnrlon = 70.0
            standardpar = 34.5
            standardpar2 = 61.5
            centerlon=18.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    elif maptype == 'Europe Ortho':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','EuropeOrtho.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup of basemap ('ortho' = orthographic projection)
            m = Basemap(projection='ortho',
                        resolution='c',area_thresh=10000.,lat_0=51,lon_0=10)
            # transform to nx x ny regularly spaced native projection grid
            #dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        # nx and ny chosen to have roughly the same horizontal res as original image.
        dx = 2.*pi*m.rmajor/360
        nx = int((m.xmax-m.xmin)/dx)+1; ny = int((m.ymax-m.ymin)/dx)+1

    elif maptype == 'Europe Conformal':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','Europe_Conformal.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            llcrnrlat = 28.0
            urcrnrlat = 66.0
            llcrnrlon = -7.0
            urcrnrlon = 70.0
            standardpar = 34.5
            standardpar2 = 61.5
            centerlon=18.
            latminout = 22.0
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='lcc',
                        lat_1=standardpar,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    if maptype == 'EurAsia Albers':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','EurAsia_albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 28.0
            urcrnrlat = 90.0
            llcrnrlon = 10.0
            urcrnrlon = 160.0
            standardpar = 34.5
            standardpar2 = 61.5
            centerlon=70.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    elif maptype == 'Polar Stereo':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','Polar_Stereo.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(lon_0=-0.0,boundinglat=30,
                        resolution='c',area_thresh=10000.,projection='npstere')
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
	
    elif maptype == 'South America Albers':   
    	mapfile = os.path.join('/Users/botia','Maps','SouthAmerica_albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = -60.0
            urcrnrlat = 20.0
            llcrnrlon = -90.0
            urcrnrlon = -35.0
            standardpar = 0.0
            standardpar2 = -30.0
            centerlon=-75.0
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    elif maptype == 'America Africa Albers':    
        mapfile= os.path.join(mysettings.pylibdir,'maps','AmericaAfrica_albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = -60.0
            urcrnrlat = 20.0
            llcrnrlon = -90.0
            urcrnrlon = +55.0
            standardpar = 10.0
            standardpar2 = -20.0
            centerlon=-35.0
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='l',area_thresh=5000.,projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    if maptype == 'Moscow Albers':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','Moscow_albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 30.0
            urcrnrlat = 70.0
            llcrnrlon = 20.0
            urcrnrlon = 90.0
            standardpar = 34.5
            standardpar2 = 61.5
            centerlon=50.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='h',projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    if maptype == 'Netherlands Albers':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','Netherlands_albers.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 47.0
            urcrnrlat = 56.0
            llcrnrlon = -1.0
            urcrnrlon = 15.0
            standardpar = 34.5
            standardpar2 = 61.5
            centerlon=5.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='h',projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1

    if maptype == 'Netherlands Albers Lies':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','Netherlands_albers_lies.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 50.49
            urcrnrlat = 53.99+0.0875
            llcrnrlon = 2.64
            urcrnrlon = 8.36+0.143
            standardpar = 40.5
            standardpar2 = 50.5
            centerlon=5.5
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='h',projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1


    if maptype == 'Netherlands Albers Zoom':   
        mapfile= os.path.join(mysettings.pylibdir,'maps','Netherlands_albers_zoom.map.pickle')
        try:
            m = cPickle.load(open(mapfile,'rb'))
        except:     
            # setup albers equal area map projection 
            llcrnrlat = 50.5
            urcrnrlat = 54.0
            llcrnrlon = 3.0
            urcrnrlon = 8.0
            standardpar = 40.5
            standardpar2 = 50.5
            centerlon=5.
            # create Basemap instance for Lambert Conformal Conic projection.
            m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
                        urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
                        rsphere=6371200.,
                        resolution='h',projection='aea',
                        lat_1=standardpar,lat_2=standardpar2,lon_0=centerlon)
            dummy = cPickle.dump(m,open(mapfile,'wb'),-1)
        # transform to nx x ny regularly spaced native projection grid
        nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1


    return m,nx,ny

if __name__ =="__main__":
    m,nx,ny=select_map('Netherlands Albers Zoom')    
    a=zeros((180,360,))+1.0

    lons=-179.5+arange(360)
    lats=-89.5+arange(180)

    flux = m.transform_scalar(a,lons,lats,nx,ny)
    q=imshow(a)
    m.drawcoastlines()
    m.drawcountries()
    parallels = arange(-60,40,20)
    m.drawparallels(parallels,labels=[1,0,0,1],fontsize=10)
    meridians = arange(-180,180,20)
    m.drawmeridians(meridians,labels=[1,1,1,1],fontsize=10)
    show()


