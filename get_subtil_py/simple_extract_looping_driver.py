import sys
import os
import errno
import numpy as np
import llcTMesh

def createODir(odirRoots,tNo,fCode,itNo):
 # Create output directory if needed
 # Output directory pattern p_{tNo}/grid p_{tNo}/fCode/itNo/p_{tNo}.fCode.{itNo}.k_{kLev}.data
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
  dList.append( "%s/%s/p_%3.3d/%s"%(dOutPath,'tiled_output',tNo,fCode) )
  dList.append( "%s/%s/p_%3.3d/%s/i_%15.15d"%(dOutPath,'tiled_output',tNo,fCode,itNo) )
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

# List of iterations to read
itList=[486864, \
        487008, \
        487152, \
        487296, \
        487440, \
        487584, \
        487728, \
        487872, \
        488016, \
        488160, \
        488304]


# List of 3d fields to read
fCodeList3d=['Theta','U','V']

# Levels to read for 3d
kLevList3d=[1,2,3,4,5,10,30]

# List of 2d fields to read
fCodeList2d=['Eta']

# List of patches
# 360 - Gulf of Mexico
# 310 - Gulf of Alaska
# 372,384,396,408 - POSYDON acoustic field expt Atlantic
# 216 - Arctic Beaufort Sea
# 287,288,300,299 - Hawaii and North and East
pNoList=[360,310,372,384,396,408,216,287,288,300,299]

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
     fDir="%s/%s/p_%3.3d/%s/i_%15.15d"%(dOutPath,'tiled_output',tNo,fCode,itNo)
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
     fDir="%s/%s/p_%3.3d/%s/i_%15.15d"%(dOutPath,'tiled_output',tNo,fCode,itNo)
     ffName="%s.%10.10d.p_%4.4d.k_%4.4d.data"%(fCode,itNo,tNo,kLev)
     fName="%s/%s"%(fDir,ffName)
     f=file(fName,'wb')
     f.write(b)
     f.close()

for pNo in pNoList:
 xcarr, fNameRead = mInfo.getStdTileXY(pNo,'XC',dList=dList)
 ycarr, fNameRead = mInfo.getStdTileXY(pNo,'YC',dList=dList)
 xgarr, fNameRead = mInfo.getStdTileXY(pNo,'XG',dList=dList)
 ygarr, fNameRead = mInfo.getStdTileXY(pNo,'YG',dList=dList)
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
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
  ffName="YC.p_%4.4d.data"%(tNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
  f.close()

 # XG
 if xgarr is not None:
  b=bytearray(xgarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
  ffName="XG.p_%4.4d.data"%(tNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
  f.close()

 # YG
 if ygarr is not None:
  b=bytearray(ygarr.astype('>f4').tobytes(order='F'))
  fDir="%s/%s/p_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
  ffName="YG.p_%4.4d.data"%(tNo)
  fName="%s/%s"%(fDir,ffName)
  f=file(fName,'wb')
  f.write(b)
