import os
import numpy as np

class llcTMesh:
 name=''
 fNTx=[0,0,0,0,0]
 fNTy=[0,0,0,0,0]
 bSize=4
 skipK=0
 def __init__(this,nx,ny,tx,ty):
  this.fNx=[nx,nx,nx,3*nx,3*nx]
  this.fNy=[3*ny,3*ny,ny,ny,ny]
  this.tx=tx
  this.ty=ty
  this.fNTx=[this.fNx[0]/this.tx,
             this.fNx[1]/this.tx,
             this.fNx[2]/this.tx,
             this.fNx[3]/this.tx,
             this.fNx[4]/this.tx]
  this.fNTy=[this.fNy[0]/this.ty,
             this.fNy[1]/this.ty,
             this.fNy[2]/this.ty,
             this.fNy[3]/this.ty,
             this.fNy[4]/this.ty]
  this.fT0=[0,0,0,0,0]
  this.fT0[0]=1
  this.fT0[1]=this.fT0[0] + \
             this.fNTx[0]*this.fNTy[0]
  this.fT0[2]=this.fT0[1] + \
             this.fNTx[1]*this.fNTy[1]
  this.fT0[3]=this.fT0[2] + \
             this.fNTx[2]*this.fNTy[2]
  this.fT0[4]=this.fT0[3] + \
             this.fNTx[3]*this.fNTy[3]
  this.skipK=this.tx*this.ty*13

 def getTileF(this,tNo):
  # Get the face that a tile sits in
  i=1
  fHi=this.fNx[i-1]*this.fNy[i-1]
  if tNo*this.tx*this.ty-1 < fHi:
   return i

  i=i+1
  fHi=fHi+this.fNx[i-1]*this.fNy[i-1]
  if tNo*this.tx*this.ty-1 < fHi:
   return i

  i=i+1
  fHi=fHi+this.fNx[i-1]*this.fNy[i-1]
  if tNo*this.tx*this.ty-1 < fHi:
   return i

  i=i+1
  fHi=fHi+this.fNx[i-1]*this.fNy[i-1]
  if tNo*this.tx*this.ty-1 < fHi:
   return i

  i=i+1
  fHi=fHi+this.fNx[i-1]*this.fNy[i-1]
  if tNo*this.tx*this.ty-1 < fHi:
   return i

  return -1

 def getFaceOffset(this,myF):
  # Get the start offset of a face
  off=-1
  if myF >= 1:
   off=0
  if myF >= 2:
   off=off+this.fNx[0]*this.fNy[0]
  if myF >= 3:
   off=off+this.fNx[1]*this.fNy[1]
  if myF >= 4:
   off=off+this.fNx[2]*this.fNy[2]
  if myF >= 5:
   off=off+this.fNx[3]*this.fNy[3]
  
  return off

 def getTileOffsetInFace(this,tNo):
  # Get starting offset for tile within face
  off=-1
  myF=this.getTileF(tNo)
  t0=this.fT0[myF-1]
  tNFaceOff=tNo-t0
  offWholeRow=int(np.fix(tNFaceOff/this.fNTx[myF-1]))*this.tx*this.ty*this.fNTx[myF-1]
  tRFaceOff=tNFaceOff-int(np.fix(tNFaceOff/this.fNTx[myF-1]))*this.fNTx[myF-1]
  offPartRow=tRFaceOff*this.tx
  off=offWholeRow+offPartRow
  return off

 def getFaceStride(this,myF):
  # Get stride between each line for this face
  stride=this.fNTx[myF-1]*this.tx
  return stride

 def getStdTileXY(this,tNo,fPref,itNo=-1,kLev=-1,dList=['./'],fSuff='.data',verbose=True):
  arr=np.zeros((this.tx,this.ty),dtype='f4',order='F')
  # Make full input file name
  if itNo == -1:
   ffName=("%s.data"%fPref)
  else:
   ffName="%s.%10.10d.data"%(fPref,itNo)
  # Look for file in dList
  # exit if it is not found
  fFound=0
  for d in dList:
   if d[-1] == '/':
    ffPath="%s%s"%(d,ffName)
   else:
    ffPath="%s/%s"%(d,ffName)
   if ( os.path.isfile(ffPath) ):
    fFound=1
    break
  if fFound == 0:
   print "# File \"%s\" not found in any search directory"%(ffName)
   return None, None
  # File found
  if ( verbose ) & ( kLev == -1 ):
   print "# Beginning read XY tile %d, from file \"%s\""%(tNo,ffPath)
  else:
   print "# Beginning read XY tile %d, level %d, from file \"%s\""%(tNo,kLev,ffPath)

  # Get level skip
  skipK=this.skipK
  # Get face number for tile number, tNo
  myF=this.getTileF(tNo)
  # Get skip to start of the face
  skipF=this.getFaceOffset(myF)
  # Get skip to start of tile tNo from start of face
  skipT=this.getTileOffsetInFace(tNo)
  # Get stride between lines in tNo
  skipStr=this.getFaceStride(myF)
  # Get element size in bytes
  bSize=this.bSize

  nBlk=this.tx
  nSkip0=skipF*bSize+skipT*bSize
  nSkipStr=skipStr*bSize
  if kLev == -1:
   kLev=1

  # Read patch from filename into array
  filename=ffPath
  with open(filename,'rb') as f:
   # Seek to start of level
   f.seek((skipK*(kLev-1))*bSize, os.SEEK_SET)
   # Seek to start of tile at this level
   f.seek(nSkip0, os.SEEK_CUR)
   for j in range(1,this.ty+1):
    # Read row
    data=np.fromfile(f,dtype='>f4',count=nBlk)
    # Seek to next row for tile
    f.seek(nSkipStr-nBlk*bSize, os.SEEK_CUR)
    arrayRow=np.reshape(data,[nBlk],order='F')
    # print arrayRow[0:4 ]
    arr[:,j-1]=arrayRow

  return arr, filename
