# Standard libraries
import sys
sys.path.insert(0,'/usr/lib/python2.7/dist-packages')
sys.path.insert(0,'/usr/local/lib/python2.7/dist-packages')

import numpy as np
import os

# LLC tiled mesh library
import llcTMesh

fieldFile='Depth.data'
# fieldFile='Theta.0001366128.data'
fieldFile='Theta.0001366128.k_1.data'
fieldFile='Theta.0000486864.k_1.data'
fieldFile='Theta.0000486864.data'
# filename='YC.data'
# filename='XC.data'

nx=4320;
ny=4320;
tx=1080;
ty=540;
wl=4;
skipK=nx*ny*13;

mesh=llcTMesh.llcTMesh(nx,ny,tx,ty)
# Choose tile to extract
tNo=288;  # Hawaii
# tNo=371;  # Mid-Atlantic coast
tNo=383;  # Cape cod
tNo=310;  # Gulf of Alaska
tNo=360;  # Gulf of Mexico
kLev=30;
# tNo=61;   # Equatorial eastern Atlantic
# tNo=62;   # Equatorial eastern Atlantic
# tNo=17;   # Antarctica
# tNo=255;  # North New Zealand
# tNo=42;  # North New Zealand
# Get face number for this tile
myF=mesh.getTileF(tNo)
print myF
# Get skip to start of face
skipF=mesh.getFaceOffset(myF)
print skipF
# Get skip to start of tile from start of face
skipT=mesh.getTileOffsetInFace(tNo)
print skipT
# Get stride between lines
skipStr=mesh.getFaceStride(myF)
print skipStr

nBlk=tx
nSkip0=skipF*4+skipT*4
nSkipStr=skipStr*4

# Read patch from filename into array
filename=fieldFile
array=np.zeros((tx,ty),dtype='f4',order='F')

with open(filename,'rb') as f:
  data=np.fromfile(f,dtype='>f4',count=3*4320*4320)
print data.max()
print data.min()

with open(filename,'rb') as f:
 # Seek to start of level
 f.seek((skipK*(kLev-1))*4, os.SEEK_SET)
 # Seek to start of tile at this level
 f.seek(nSkip0, os.SEEK_CUR)
 for j in range(1,ty+1):
  # Read row
  data=np.fromfile(f,dtype='>f4',count=nBlk) 
  # Seek to next row for tile
  f.seek(nSkipStr-nBlk*4, os.SEEK_CUR)
  arrayRow=np.reshape(data,[nBlk],order='F')
  print arrayRow[0:4 ]
  array[:,j-1]=arrayRow

 print 'the end', arrayRow[0:4 ]
 print arrayRow[-1]
 print array
fldArray=array
maskedfldArray=np.ma.masked_array(fldArray,fldArray==0.)
# maskedfldArray=np.ma.masked_array(fldArray,fldArray==0.)
fldArray=maskedfldArray
# sys.exit()

filename='XC.data'
array=np.zeros((tx,ty),dtype='f4',order='F')
with open(filename,'rb') as f:
 f.seek(nSkip0, os.SEEK_SET)
 for j in range(1,ty+1):
  data=np.fromfile(f,dtype='>f4',count=nBlk)      # P8 Pacific rotated
  f.seek(nSkipStr-nBlk*4, os.SEEK_CUR)
  arrayRow=np.reshape(data,[nBlk],order='F')
  print arrayRow[0:4 ]
  array[:,j-1]=arrayRow

 print 'the end', arrayRow[0:4 ]
 print arrayRow[-1]
 print array
xcArray=array

filename='YC.data'
array=np.zeros((tx,ty),dtype='f4',order='F')
array=array+9999.
with open(filename,'rb') as f:
 f.seek(nSkip0, os.SEEK_SET)
 for j in range(1,ty+1):
  data=np.fromfile(f,dtype='>f4',count=nBlk)      # P8 Pacific rotated
  f.seek(nSkipStr-nBlk*4, os.SEEK_CUR)
  arrayRow=np.reshape(data,[nBlk],order='F')
  print arrayRow[0:4 ]
  array[:,j-1]=arrayRow

 print 'the end', arrayRow[0:4 ]
 print arrayRow[-1]
 print array
ycArray=array

sys.exit()

# Now try plotting

import matplotlib.pyplot as plt
import sys
import mpl_toolkits.basemap
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import seawater as sw

# fig = plt.figure(facecolor='w', figsize=(12.,8.5))

import sys
# print dir(__builtins__)
sys.path.insert(0,'/usr/lib/python2.7/dist-packages')
sys.path.insert(0,'/usr/local/lib/python2.7/dist-packages')

latmin=ycArray.min()
latmax=ycArray.max()
lonmin=xcArray.min()
lonmax=xcArray.max()
# exit()

# lonmin=-85;
# lonmax=-50;
# latmin=25;
# latmax=55;
lat_1=latmin;
lon_0=lonmin;
proj="lcc";
lw=.1;
fs=10.;
fl="fl";
ft="ft";
re=6400000;

plt.close('all')
m=Basemap(llcrnrlon=lonmin,   \
          llcrnrlat=latmin,   \
          urcrnrlon=lonmax,   \
          urcrnrlat=latmax,   \
          rsphere=(re,re),    \
          resolution='i',     \
          area_thresh=1000.,  \
          projection=proj,    \
          lat_1=lat_1,        \
          lon_0=lon_0         \
         );

lonti,latti = np.meshgrid(np.linspace(lonmin,lonmax,3),np.linspace(latmin,latmax,3))
# print lonti
# print latti
xgt,ygt = m(lonti,latti)
print xgt
print ygt

# 
m.drawparallels(np.arange(latmin, latmax, 4),
    labels=[1, 0, 0, 0], linewidth=lw, 
    fontsize=fs, fontweight='medium')
m.drawmeridians(np.arange(lonmin, lonmax+4, 7),
    labels=[0, 0, 0, 1], dashes=[1,1], linewidth=lw, 
    fontsize=fs, fontweight='medium')

# fig = plt.figure(facecolor='w', figsize=(12.,8.5))
m.fillcontinents(color='.60',lake_color='none');
m.drawcoastlines();

ny=fldArray.shape[0]
print ny
nx=fldArray.shape[1]
print nx
plons, plats = m.makegrid(nx,ny)
# px, py = m(plons,plats)
px, py = m(xcArray,ycArray)
print px

fmax=fldArray.max()
fmin=fldArray.min()
fstd=fldArray.std()
fave=fldArray.mean()
vmin=fave-fstd*2.
vmax=fave+fstd*2.
m.pcolor(px,py,fldArray,vmin=vmin,vmax=vmax)


# x = np.linspace(0, 3*np.pi, 500)
# plt.plot(x, np.sin(x**2))
plt.title('A Coastline Map');
plt.show();
plt.savefig('model_snapshot_speed',dpi=300,bbox_inches='tight')


# print mpl_toolkits.basemap.Basemap



