# Python program to generate and submit jobs to extract all iterations and fields
# for a given standard tile.
#
#
import subprocess
import errno
import sys
import os
import select
import llcExtractJobFuncs
import yaml

#
# This is done on batches of N-way parallel jobs submitted to a queue and running 
# python extraction script

# Set tile number to fetch
# Defaults
# Hawaii
tNo=288
# North of Hawaai HOTS region
tNo=299
# Environment variable override
if os.getenv('LLC_TEXTRACT_TNO') != None:
 tNoStr=os.environ['LLC_TEXTRACT_TNO']
 try:
  tNo=int(tNoStr)
 except ValuerError:
  raise ValueError('Environment variable LLC_TEXTRACT_TNO value is not an integer')


itLo=10368
itHi=1365840+144*2
## itHi=10368+144*4
itStride=144
itList=range(itLo,itHi+1,itStride)

# Config settings
# Edit this to use relevant ids, key and host
cFile="config.yaml"
with open(cFile,"r") as f:
 yconfig=yaml.load(f)
remoteLoginCmd=yconfig['remoteLoginCmd']
remoteStoreDirRoot=yconfig['remoteStoreDirRoot']
tmout=10
tmout=8

# remoteLoginCmd=""
# remoteStoreDir=""
# tmout=1

# Set local directory for writing job files that will be transferred to submission system.
jobFilePref="tile_tar_job"
jobFileDir="job_staging"
# Environment variable override
if os.getenv('LLC_JOBFILE_DIR') != None:
 jobFileDir=os.environ['LLC_JOBFILE_DIR']

# Set remote directory where job files will be transferred and submited
remJobFileDir='job_staging'

# Create jobFileDir directory if it does not exist
try:
 os.makedirs(jobFileDir)
except OSError as exc:
 if exc.errno == errno.EEXIST and os.path.isdir(jobFileDir):
  pass
 else:
  raise

ni=len(itList)
print '# ',ni,' iterations requested to be tar archived for transfer'
print '# start=',itList[0]
print '#   end=',itList[-1]

jFuncs=llcExtractJobFuncs.llcExtractJobFuncs(tmout,tNo, itList, remoteStoreDirRoot, remoteLoginCmd, remJobFileDir, jobFileDir, jobFilePref)

# Check to see if expected directories exist
#### ierr=jFuncs.checkRemTileDirPresent()
#### if ierr != 0:
####  exit()

# Now check if directories contain expected numbers of files - to make sure the extract stage has completed.
#### ierr=jFuncs.checkRemFileCount()
#### if ierr != 0:
####  exit()

# Create tar jobs
print "# Generating tile extract jobs for tile %d"%tNo,"iteration count, %d, and iteration range = %d-%d"%(len(itList),itLo,itHi)
# Create blocks of tar commands that each archive multiple i_ directories
jfList=jFuncs.writeTarJob(tNo,itList)
print jfList

# Create in memory tar file
tInMem=jFuncs.writeTarInMem(jfList)

# Transfer jobs to temporary staging directory created on remote host
tpath=jFuncs.unTarOnRemote(tInMem)

print 'tpath=',tpath
# exit()

# Start jobs

#
# == Submit the jobs ===
#
print '# submiting jobs.'
rc=remoteLoginCmd.split()
p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0)
p.stdin.write("cd %s\n"%tpath)
for jf in jfList:
 p.stdin.write("qsub %s\n"%jf)
print "# reading stdout"
pr=1
while pr != []:
 pr,pw,px=select.select([p.stdout],[],[],tmout)
 if pr != []:
  l=pr[0].readline()
  if len(l) != 0:
   print "stdout ",l
  else:
   pr=[]

exit()
