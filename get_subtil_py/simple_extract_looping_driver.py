import sys
import os
import errno
import numpy as np
import llcTMesh

def createODir(odirRoots,tNo,fCode,itNo):
 # Create output directory if needed
 # Output directory pattern p_{tNo}/grid p_{tNo}/itNo/fCode/p_{tNo}.fCode.{itNo}.k_{kLev}.data
 dOutPath=None
 for d in odirRoots:
  if os.path.exists(d):
   dOutPath=d
   break

 # Skip writing if no root directory to use found
 if dOutPath is None:
  sys.exit()

 # Make tile, iteration, field code tree
 dList=[]
 dList.append( "%s/%s"%(dOutPath,'tiled_output') )
 dList.append( "%s/%s/p_%3.3d"%(dOutPath,'tiled_output',tNo) )
 dList.append( "%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',tNo) )
 if fCode is not None:
  dList.append( "%s/%s/p_%3.3d/i_%15.15d"%(dOutPath,'tiled_output',tNo,itNo) )
  dList.append( "%s/%s/p_%3.3d/i_%15.15d/%s"%(dOutPath,'tiled_output',tNo,itNo,fCode) )
 # print dList
 for d in dList:
  if not os.path.exists(d):
   try:
    os.makedirs(d)
   except OSError as error:
    if error.errno != errno.EEXIST:
     raise
 return dOutPath


# Set basic index for mesh
nx=4320
ny=4320
tx=1080
ty=540
mInfo=llcTMesh.llcTMesh(nx,ny,tx,ty)

# Places to look for input files (read from first copy found)
dList=['./',                                              \
       '/nobackupp8/dmenemen/llc/llc_4320/MITgcm/run',    \
       '/nobackupp2/dmenemen/llc_4320/MITgcm/run_485568', \
       '/nobackupp2/dmenemen/llc_4320/grid']

# Places to write output (write to first one found)
odirRoots=['/nobackupp8/cnhill1/llc_4320_tiles','.']

na=len(sys.argv)
if na > 1:
 argList=sys.argv[1].split(",")
 if len(argList) == 3:
  a0=argList[0]
  a1=argList[1]
  a2=argList[2]
  print a0,a1,a2
  try:
   a0i=int(a0)
  except ValuerError:
   raise ValueError('argument 1 is not an integer')
  try:
   a1i=int(a1)
  except ValuerError:
   raise ValueError('argument 2 is not an integer')
  try:
   a2i=int(a2)
  except ValuerError:
   raise ValueError('argument 3 is not an integer')
 
  if a0i % 144 != 0:
   print a0i, ' is not a multiple of 144.'
   exit()

  if a2i != 144:
   print a2i, ' is not 144.'
   exit()


  ar=range(a0i,a1i,a2i)
  if len(ar) > 3:
   for it1,it2 in [ (ar[i], ar[i+2]) for i in range(0,len(ar)-2,3) ]:
    print "python ",sys.argv[0], ' ', "%d,%d,144"%(it1,it2)
 else:
  exit()

if len(ar) != 2:
 exit()
else:
 itList=ar

# List of iterations to read
##itList=[486864, \
##        487008, \
##        487152, \
##        487296, \
##        487440, \
##        487584, \
##        487728, \
##        487872, \
##        488016, \
##        488160, \
##        488304]
##itList=[486864,487008]
## it0=486864;
## icount=100;
## # icount=3;
## istride=144;
## itList=range(it0,it0+icount*istride+1,istride)


# List of 3d fields to read
fCodeList3d=['Theta','U','V','Salt','W']
# fCodeList3d=['Theta']

# Levels to read for 3d
kLevList3d=[1,2,3,4,5,10,30]
kLevList3d=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
kLevList3d=np.arange(1,91)
# kLevList3d=[1]

# List of 2d fields to read
fCodeList2d=['Eta','oceTAUX','oceTAUY','PhiBot','KPPhbl','oceFWflx','oceQnet','oceQsw','oceSflux']

# List of patches
# 360 - Gulf of Mexico
# 310 - Gulf of Alaska
# 372,384,396,408 ,69,65 - POSYDON acoustic field expt Atlantic
# 216 - Arctic Beaufort Sea
# 287,288,300,299 - Hawaii and North and East
# pNoList=[360,310,372,384,396,408,69,65,216,287,288,300,299]
# pNoList=[216]
pNoList=[372,384,396,408,69,65,216]
# pNoList=[69,65]

# Samoan Passage (9.5S,168.75W)
pNoList=[278]


# Read tile for the given tile, field code and iterantion number and read
# basic grid information for tile.
# file crossing 
for itNo in itList:
 for fCode in fCodeList3d:
  # within file
  for tNo in pNoList:
   for kLev in kLevList3d:
    # Create output directory if needed
    dOutPath=createODir(odirRoots,tNo,fCode,itNo)
    fldarr,fNameRead = mInfo.getStdTileXY(tNo,fCode,itNo=itNo,kLev=kLev,dList=dList)
    # Write extracted tile data ( '>f4' == in big-endian, '<f4' == little endian)
    # Write field array
    if fldarr is not None:
     b=bytearray(fldarr.astype('>f4').tobytes(order='F'))
     fDir="%s/%s/p_%3.3d/i_%15.15d/%s"%(dOutPath,'tiled_output',tNo,itNo,fCode)
     ffName="%s.%10.10d.p_%4.4d.k_%4.4d.data"%(fCode,itNo,tNo,kLev)
     fName="%s/%s"%(fDir,ffName)
     f=file(fName,'wb')
     f.write(b)
     f.close()

# Read tile for the given tile, field code and iterantion number and read
# basic grid information for tile.
# file crossing 
for itNo in itList:
 for fCode in fCodeList2d:
  # within file
  for tNo in pNoList:
   for kLev in [1]:
    # Create output directory if needed
    dOutPath=createODir(odirRoots,tNo,fCode,itNo)
    fldarr,fNameRead = mInfo.getStdTileXY(tNo,fCode,itNo=itNo,kLev=kLev,dList=dList)
    # Write extracted tile data ( '>f4' == in big-endian, '<f4' == little endian)
    # Write field array
    if fldarr is not None:
     b=bytearray(fldarr.astype('>f4').tobytes(order='F'))
     fDir="%s/%s/p_%3.3d/i_%15.15d/%s"%(dOutPath,'tiled_output',tNo,itNo,fCode)
     ffName="%s.%10.10d.p_%4.4d.k_%4.4d.data"%(fCode,itNo,tNo,kLev)
     fName="%s/%s"%(fDir,ffName)
     f=file(fName,'wb')
     f.write(b)
     f.close()

for pNo in pNoList:
 xcarr,    fNameRead = mInfo.getStdTileXY(pNo,'XC',dList=dList)
 ycarr,    fNameRead = mInfo.getStdTileXY(pNo,'YC',dList=dList)
 xgarr,    fNameRead = mInfo.getStdTileXY(pNo,'XG',dList=dList)
 ygarr,    fNameRead = mInfo.getStdTileXY(pNo,'YG',dList=dList)
 deptharr, fNameRead = mInfo.getStdTileXY(pNo,'Depth',dList=dList)
 # Create output directories as needed (grid only has tile directories)
 dOutPath=createODir(odirRoots,pNo,None,None)
 # Write grid arrays
 # XC
 if xcarr is not None:
  b=bytearray(xcarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="XC.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
  f.close()

 # YC
 if ycarr is not None:
  b=bytearray(ycarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="YC.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
  f.close()

 # XG
 if xgarr is not None:
  b=bytearray(xgarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="XG.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
  f.close()

 # YG
 if ygarr is not None:
  b=bytearray(ygarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="YG.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)

 # Depth
 if deptharr is not None:
  b=bytearray(deptharr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="Depth.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)

# Now get vertical grid spacing info
# % ls -altr /nobackupp2/dmenemen/llc_4320/grid/DRC* /nobackupp2/dmenemen/llc_4320/grid/RC* /nobackupp2/dmenemen/llc_4320/grid/DRF* /nobackupp2/dmenemen/llc_4320/grid/RF*
# -rw-r--r-- 1 dmenemen g26209 144 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/DRF.meta
# -rw-r--r-- 1 dmenemen g26209 360 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/DRF.data
# -rw-r--r-- 1 dmenemen g26209 144 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/DRC.meta
# -rw-r--r-- 1 dmenemen g26209 364 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/DRC.data
# -rw-r--r-- 1 dmenemen g26209 144 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/RC.meta
# -rw-r--r-- 1 dmenemen g26209 360 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/RC.data
# -rw-r--r-- 1 dmenemen g26209 144 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/RF.meta
# -rw-r--r-- 1 dmenemen g26209 364 Jan 18  2014 /nobackupp2/dmenemen/llc_4320/grid/RF.data
for pNo in pNoList:
 rfarr,    fNameRead = mInfo.getStdFile('RF',dList=dList)
 drfarr,   fNameRead = mInfo.getStdFile('DRF',dList=dList)
 rcarr,    fNameRead = mInfo.getStdFile('RC',dList=dList)
 drcarr,   fNameRead = mInfo.getStdFile('DRC',dList=dList)
 dOutPath=createODir(odirRoots,pNo,None,None)

 if rfarr is not None:
  b=bytearray(rfarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="RF.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)

 if drfarr is not None:
  b=bytearray(drfarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="DRF.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)

 if rcarr is not None:
  b=bytearray(rcarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="RC.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)

 if drcarr is not None:
  b=bytearray(drcarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',pNo)
  ffName="DRC.p_%4.4d.data"%(pNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
