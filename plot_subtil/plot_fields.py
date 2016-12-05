# search path as needed
import sys
sys.path.insert(0,'/usr/lib/python2.7/dist-packages')
sys.path.insert(0,'/usr/local/lib/python2.7/dist-packages')

# core os stuff
import os

# plotting and math
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

# calendar stuff
import datetime
#print (datetime.datetime(2011,9,10)+datetime.timedelta(seconds=3)).strftime("%B %d %Y, %T")

nx=1080; ny=540; nz=90;
trootDir='tiled_output';
pno=372;
fldCode='Theta';
ino=486864;
kHlev=1;
yLat=29;

dpath='%s/p_%3.3d/%s/i_%15.15d'% (trootDir,pno,fldCode,ino)
gpath='%s/p_%3.3d/%s'% (trootDir,pno,'grid')
tstr=(datetime.datetime(2011,9,10)+datetime.timedelta(seconds=ino*25)).strftime("%B %d %Y, %T")

xcfile='%s/XC.p_%4.4d.data'%(gpath,pno)
ycfile='%s/YC.p_%4.4d.data'%(gpath,pno)
rcfile='%s/RC.p_%4.4d.data'%(gpath,pno)
with open(xcfile,'rb') as f:
  data=np.fromfile(f,dtype='>f4',count=nx*ny)
  XC=np.reshape(data,[nx,ny],order='F')
with open(ycfile,'rb') as f:
  data=np.fromfile(f,dtype='>f4',count=nx*ny)
  YC=np.reshape(data,[nx,ny],order='F')
with open(rcfile,'rb') as f:
  data=np.fromfile(f,dtype='>f4',count=nx*ny)
  RC=np.reshape(data,[nz],order='F')

# Make some plots
plt.figure()

# Subplot of a horizontal level
plt.subplot(2,1,2)
klev=kHlev;

fnam='%s.%10.10d.p_%4.4d.k_%4.4d.data'%(fldCode,ino,pno,klev)
filename='%s/%s'%(dpath,fnam)
with open(filename,'rb') as f:
  data=np.fromfile(f,dtype='>f4',count=nx*ny)
  data2d=np.reshape(data,[nx,ny],order='F')

data2dMasked=ma.masked_values(data2d,0.)

axMin=XC.min()
axMax=XC.max()
ayMin=YC.min()
ayMax=YC.max()

plt.subplot(1,2,2)
plt.pcolormesh(XC,YC,data2dMasked)
plt.ylabel('Latitude (%s)'%(r'$^{\circ}{\rm N}$'))
plt.xlabel('Longitude (%s)'%(r'$^{\circ}{\rm E}$'))
dstr='\nz=%.2fm,k=%d'%(RC[klev-1],klev)
plt.title(('%s%s%s%s%s'%('LLC4320 Theta\n(potential temperature, ',r'${\theta}_{0}$)','\n',tstr,dstr)))
cb=plt.colorbar(fraction=0.07)
cb.ax.set_ylabel(r'$\theta_{0}(^{\circ}\rm{C})$')
plt.axis('tight')
plt.axis('square')
plt.axis([axMin,axMax,ayMin,ayMax])
# Draw line showing vertical section
plt.plot([axMin,axMax],[yLat,yLat])

# subplots of a vertical longitude-height section
yLatUse=yLat;
phi=abs(YC[:,1]-yLatUse)
jmin=phi.argmin()
yatmin=YC[jmin,1]
dataXZ=np.zeros([nz,ny])
for k in range(1,nz+1):
 fnam='%s.%10.10d.p_%4.4d.k_%4.4d.data'%(fldCode,ino,pno,k)
 filename='%s/%s'%(dpath,fnam)
 with open(filename,'rb') as f:
  data=np.fromfile(f,dtype='>f4',count=nx*ny)
  data2d=np.reshape(data,[nx,ny],order='F')
  dataXZ[k-1,:]=data2d[jmin,:]
dataXZ=ma.masked_values(dataXZ,0.)

plt.subplot(2,2,1)
kShallow=49;
X,Y=np.meshgrid(XC[jmin,:],RC[0:kShallow])
plt.pcolormesh(X,Y,dataXZ[0:kShallow,:])
plt.axis([axMin,axMax,RC[kShallow],RC[0]])
cb=plt.colorbar()
cb.ax.set_ylabel(r'$\theta_{0}(^{\circ}\rm{C})$')
plt.title('Latitude = %.2f%s'%(yatmin,r'$^{\circ}{\rm N}$'))
plt.axis('tight')
plt.xlabel('Longitude (%s)'%(r'$^{\circ}{\rm E}$'))
plt.ylabel('Depth (m)')
plt.subplot(2,2,3)
kDeep=50
X,Y=np.meshgrid(XC[jmin,:],RC[kDeep:])
plt.pcolormesh(X,Y,dataXZ[kDeep:,:])
plt.axis([axMin,axMax,RC[-1],RC[kDeep]])
plt.axis('tight')
plt.xlabel('Longitude (%s)'%(r'$^{\circ}{\rm E}$'))
plt.ylabel('Depth')
cb=plt.colorbar()
cb.ax.set_ylabel(r'$\theta_{0}(^{\circ}\rm{C})$')


plt.savefig('foo.png', bbox_inches='tight', dpi=150.)
# plt.show()
