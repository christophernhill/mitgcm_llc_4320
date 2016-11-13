import sys
import os
import errno
import numpy as np
import llcTMesh

nx=4320
ny=4320
tx=1080
ty=540
mInfo=llcTMesh.llcTMesh(nx,ny,tx,ty)

dList=['./',                                              \
       '/nobackupp8/dmenemen/llc/llc_4320/MITgcm/run',    \
       '/nobackupp2/dmenemen/llc_4320/MITgcm/run_485568', \
       '/nobackupp2/dmenemen/llc_4320/grid']

itList=[485568, \
        485712, \
        485856, \
        486000, \
        486144, \
        486288, \
        486432, \
        486576, \
        486720, \
        486864, \
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


# Read tile for the given tile, field code and iterantion number and read
# basic grid information for tile.
tNo=360  # Gulf of Mexico
# tNo=310  # Alaska coast
kLev=1
itNo=486864
itNo=itList[16]
fCode='Theta'
fldarr,fNameRead = mInfo.getStdTileXY(tNo,fCode,itNo=itNo,kLev=kLev,dList=dList)
xcarr, fNameRead = mInfo.getStdTileXY(tNo,'XC',dList=dList)
ycarr, fNameRead = mInfo.getStdTileXY(tNo,'YC',dList=dList)
xgarr, fNameRead = mInfo.getStdTileXY(tNo,'XG',dList=dList)
ygarr, fNameRead = mInfo.getStdTileXY(tNo,'YG',dList=dList)

# Write extracted tile data ( '>f4' == in big-endian, '<f4' == little endian)
odirRoots=['/nobackupp8/cnhill1/llc_4320_tiles','.']
# Output directory pattern t_{tNo}/grid t_{tNo}/fCode/itNo/t_{tNo}.fCode.{itNo}.k_{kLev}.data
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
dList.append( "%s/%s/t_%3.3d"%(dOutPath,'tiled_output',tNo) )
dList.append( "%s/%s/t_%3.3d/grid"%(dOutPath,'tiled_output',tNo) )
dList.append( "%s/%s/t_%3.3d/%s"%(dOutPath,'tiled_output',tNo,fCode) )
dList.append( "%s/%s/t_%3.3d/%s/i_%15.15d"%(dOutPath,'tiled_output',tNo,fCode,itNo) )
print dList
for d in dList:
 if not os.path.exists(d):
    try:
        os.makedirs(d)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

# Write field array
if fldarr is not None:
 b=bytearray(fldarr.astype('>f4').tobytes(order='F'))
 fDir="%s/%s/t_%3.3d/%s/i_%15.15d"%(dOutPath,'tiled_output',tNo,fCode,itNo)
 ffName="%s.%10.10d.t_%4.4d.k_%4.4d.data"%(fCode,itNo,tNo,kLev)
 fName="%s/%s"%(fDir,ffName)
 f=file(fName,'wb')
 f.write(b)
 f.close()

# Write grid arrays
# XC
if xcarr is not None:
 b=bytearray(xcarr.astype('>f4').tobytes(order='F'))
 fDir="%s/%s/t_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
 ffName="XC.t_%4.4d.data"%(tNo)
 fName="%s/%s"%(fDir,ffName)
 f=file(fName,'wb')
 f.write(b)
 f.close()

# YC
if ycarr is not None:
 b=bytearray(ycarr.astype('>f4').tobytes(order='F'))
 fDir="%s/%s/t_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
 ffName="YC.t_%4.4d.data"%(tNo)
 fName="%s/%s"%(fDir,ffName)
 f=file(fName,'wb')
 f.write(b)
 f.close()

# XG
if xgarr is not None:
 b=bytearray(xgarr.astype('>f4').tobytes(order='F'))
 fDir="%s/%s/t_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
 ffName="XG.t_%4.4d.data"%(tNo)
 fName="%s/%s"%(fDir,ffName)
 f=file(fName,'wb')
 f.write(b)
 f.close()

# YG
if ygarr is not None:
 b=bytearray(ygarr.astype('>f4').tobytes(order='F'))
 fDir="%s/%s/t_%3.3d/grid"%(dOutPath,'tiled_output',tNo)
 ffName="YG.t_%4.4d.data"%(tNo)
 fName="%s/%s"%(fDir,ffName)
 f=file(fName,'wb')
 f.write(b)
