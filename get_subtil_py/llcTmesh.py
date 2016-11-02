import numpy as np

class llcTMesh:
 name=''
 fNTx=[0,0,0,0,0]
 fNTy=[0,0,0,0,0]
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
