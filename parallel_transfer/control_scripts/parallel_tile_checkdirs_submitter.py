# Python program to generate and submit jobs to extract all iterations and fields
# for a given standard tile.
#
#
import subprocess
import errno
import os

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
itHi=1366128
itStride=144
itList=range(itLo,itHi+1,itStride)

# Config settings
# Edit this to use relevant ids, key and host
remoteLoginCmd="ssh -t -A -l cnh -i  ~/.ssh/id_rsa.pub eofe7.mit.edu ssh -t -A -p 20002 cnhill1@localhost"
remoteLoginCmd=""
jobFilePref="tile_extract_job"
jobFileDir="jobs"
# Environment variable override
if os.getenv('LLC_JOBFILE_DIR') != None:
 jobFileDir=os.environ['LLC_JOBFILE_DIR']

# Create directory if it does not exist
try:
 os.makedirs(jobFileDir)
except OSError as exc:
 if exc.errno == errno.EEXIST and os.path.isdir(jobFileDir):
  pass
 else:
  raise

jobHeader=[]
jobHeader.append('#PBS -S /bin/bash')
jobHeader.append('#PBS -l select=1:ncpus=16:model=san')
jobHeader.append('#PBS -l walltime=00:60:00')
jobHeader.append('#PBS -q normal')
jobHeader.append('#PBS -j oe')
jobHeader.append('#PBS -m abe')
jobHeader.append('#PBS -M cnh@mit.edu')

#PBS -S /bin/bash
#PBS -l select=1:ncpus=16:model=san
#PBS -l walltime=00:60:00
#PBS -q normal
#PBS -j oe
#PBS -m abe
#PBS -M cnh@mit.edu

module load python/2.7.10
# cd /home4/cnhill1/projects/get_alll_llc/python/mitgcm_llc_4320/get_subtil_py
cd /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_278
tar -cvf tar00090.tar \
i_000000000632448 \
i_000000000632592 \
i_000000000632880 \
i_000000000633024 \
i_000000000633312 \
i_000000000633456 \
i_000000000633744 \
i_000000000633888 \
i_000000000634176 \
i_000000000634320 \
i_000000000634608 \
i_000000000634752 \
i_000000000635040 \
i_000000000635184 \
i_000000000635472 \
i_000000000635616 \
i_000000000635904 \
i_000000000636048 \
i_000000000636336 \
i_000000000636480 \
i_000000000636768 \
i_000000000636912 \
i_000000000637200 \
i_000000000637344 \
i_000000000637632 \
i_000000000637776 \
i_000000000638064 \
i_000000000638208 \
i_000000000638496 \
i_000000000638640 \
i_000000000638928 \
i_000000000639072 \
;


jobHeader.append('module load python/2.7.10')
jobHeader.append('cd /home4/cnhill1/projects/get_alll_llc/python/mitgcm_llc_4320/get_subtil_py')
# python  simple_extract_looping_driver.py   17280,17568,144 & </dev/null

# Check connectivity
print "# Testing remote connection"
testCommand="%s %s"%(remoteLoginCmd,"pwd")
try:
 tcOut=subprocess.check_output(testCommand,stderr=subprocess.STDOUT,shell=True)
except subprocess.CalledProcessError, e:
 print "    Error testing connection with","\"%s\""%testCommand
 print "    Error message:"
 print "   ","\"%s\""%e.output
 exit()
else:
 print "#  connection test passed"

# 1. Generate tile extract jobs
print "# Generating tile extract jobs for tile %d"%tNo,"iteration count, %d, and iteration range = %d-%d"%(len(itList),itLo,itHi)
# Create blocks extract commands that each execute 3 extracts.
clist=[]
for it1,it2 in [ (itList[i], itList[i+2]) for i in range(0,len(itList)-2,3) ]:
 crec="%s %s %d,%d,%d"%("python","someCommand",it1,it2,itStride)
 clist.append(crec)
# Group thesse in sets of 16 per job file
nc=0
nj=0
for c in clist:
 if nc == 0:
  cblock=[]
 crec="%s &"%(c)
 cblock.append(crec)
 if (nc+1)%16 == 0:
  print "%s%s-%5.5d%s"%("######",jobFilePref,nj,".pbs")
  for jh in jobHeader: print jh
  print "export LLC_TEXTRACT_TNO=%d"%tNo
  for cb in cblock:
   print "%s"%cb
  print "wait"
  nc=0
  nj=nj+1
 else:
  nc=nc+1
if nc > 0:
 print "%s%s-%5.5d%s"%("######",jobFilePref,nj,".pbs")
 for jh in jobHeader: print jh
 print "export LLC_TEXTRACT_TNO=%d"%tNo
 for cb in cblock:
  print "%s"%cb
 print "wait"
