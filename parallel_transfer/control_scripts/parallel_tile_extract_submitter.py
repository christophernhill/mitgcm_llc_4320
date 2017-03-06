# Python program to generate and submit jobs to extract all iterations and fields
# for a given standard LLC tile.
#
#
import subprocess
import errno
import sys
import os
import select

#
# Script generated batches of N-way parallel jobs submitted to a queue and running 
# python extraction script. It can interact with a remote machine via ssh to
# submit jobs, provided remote system is configured to accept authentication
# via simple ssh key. For Pleiades this is possible by going over a pre-existing tunnel
# that was set up using multi factor auth.
#

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
# itHi=itLo+itStride*16*3*2
itList=range(itLo,itHi+1,itStride)

# Config settings
# Edit this to use relevant ids, key and host
# Note - turn off tty otherwise handshaking with remote shell falls apart
remoteLoginCmd="ssh -T -A -l cnh -i  ~/.ssh/id_rsa.pub eofe7.mit.edu ssh -T -A -p 20002 cnhill1@localhost /bin/bash -s"
tmout=10;
# remoteLoginCmd="/bin/bash -s"
# tmout=1;

# Set local directory for writing job files that will be transferred to submission system.
jobFilePref="tile_extract_job"
jobFileDir="jobs"
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

# Set job header lines
jobHeader=[]
jobHeader.append('#PBS -S /bin/bash')
jobHeader.append('#PBS -l select=1:ncpus=16:model=san')
jobHeader.append('#PBS -l walltime=00:60:00')
jobHeader.append('#PBS -q normal')
jobHeader.append('#PBS -j oe')
jobHeader.append('#PBS -m abe')
jobHeader.append('#PBS -M cnh@mit.edu')
jobHeader.append('module load python/2.7.10')
jobHeader.append('cd /home4/cnhill1/projects/get_alll_llc/python/mitgcm_llc_4320/get_subtil_py')

# Check to see if connecting to remote login command system works.
print "# Testing remote connection"
rc=remoteLoginCmd.split()
p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
p.stdin.write("pwd\n")
pr,pw,px=select.select([p.stdout],[],[],tmout)
if pr == []:
 print "# remote connect test timed out"
 exit()
else:
 pr=1
 while pr != []:
  pr,pw,px=select.select([p.stdout],[],[],tmout)
  if pr != []:
   l=pr[0].readline()
   if len(l) != 0:
    print "stdout ",l
   else:
    pr=[]
print '#stdout drained'
p.stdin.close()
print "#  connection test passed"

#
# 1. Generate tile extract jobs
print "# Generating tile extract jobs for tile %d"%tNo,"iteration count, %d, and iteration range = %d-%d"%(len(itList),itLo,itHi)
# Create blocks extract commands that each execute 3 extracts.
clist=[]
for it1,it2 in [ (itList[i], itList[i+2]) for i in range(0,len(itList)-2,3) ]:
 crec="%s %s %d,%d,%d"%("python","simple_extract_looping_driver.py",it1,it2+1,itStride)
 clist.append(crec)
# Group these in sets of 16 per job file
nc=0
nj=0
f=sys.stdout
jflist=[]

for c in clist:
 if nc == 0:
  cblock=[]
 crec="%s &"%(c)
 cblock.append(crec)
 if (nc+1)%16 == 0:
  fnj="%s/%s-%5.5d.pbs"%(jobFileDir,jobFilePref,nj)
  f=open(fnj,'w')
  print >> f, "%s%s-%5.5d%s"%("######",jobFilePref,nj,".pbs")
  for jh in jobHeader: print >> f, jh
  print >> f, "export LLC_TEXTRACT_TNO=%d"%tNo
  for cb in cblock:
   print >> f, "%s"%cb
  print >> f, "wait"
  nc=0
  nj=nj+1
  f.close()
  jflist.append(fnj)
  f=sys.stdout
 else:
  nc=nc+1

if nc > 0:
 fnj="%s/%s-%5.5d.pbs"%(jobFileDir,jobFilePref,nj)
 f=open(fnj,'w')
 print >> f, "%s%s-%5.5d%s"%("######",jobFilePref,nj,".pbs")
 for jh in jobHeader: print >> f, jh
 print >> f, "export LLC_TEXTRACT_TNO=%d"%tNo
 for cb in cblock:
  print >> f, "%s"%cb
 print >> f, "wait"
 f.close()
 jflist.append(fnj)
 f=sys.stdout
 nj=nj+1
# 
print "#",nj,"job scripts created."

#
#
#
# ================================================
# ==== Now tar job scripts and then transfer =====
# ================================================
#
#
# == Tar into memory buffer ==
tc="tar -cf - "
for jf in jflist:
 tc="%s %s"%(tc,jf)
tcOut=subprocess.check_output(tc,stderr=subprocess.STDOUT,shell=True)
# Check tar matches expected list of files
p=subprocess.Popen(['tar','-tf','-'],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
soutArr=p.communicate(input=tcOut)
sout=soutArr[0]
tl=sout.split('\n')[0:-1]
if jflist!=tl:
 print 'Error: tar contents does not match expected list of jobs'
 exit()
else:
 print '# tar archive of job files to transfer is ready, beginning transfer.'

#
# == Unpack tar file on job system ==
#
# Example commands that run
# mkdir -p job_staging/ ; mktemp -d job_staging/llc_extract_XXXXXX
# cd job_staging/llc_extract_GpkaZE; tar -xf -
# cd job_staging/llc_extract_GpkaZE; qsub ....
# sys.stdout.write(tcOut)
# sys.stdout.flush()
# exit()
rc=remoteLoginCmd.split()
p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0)
p.stdin.write("mkdir -p %s/\n"%remJobFileDir)
pr = 1
while pr != []:
 pr,pw,px=select.select([p.stdout],[],[],tmout)
 if pr != []:
  pr[0].readline()
print '# connected and root staging directory created.'
p.stdin.write("mktemp -d %s/llc_extract_XXXXXX\n"%remJobFileDir)
tpath=p.stdout.readline()
tpath=tpath[0:-1]
print "%s \"%s\"%s"%('# transfer sub-directory',tpath,' created.')
p.stdin.write("cd %s\n"%tpath)
p.stdin.write("pwd\n")
p.stdin.write("tar -xf -\n")
p.stdin.write("%s"%tcOut)
# p.stdin.write("boo")
p.stdin.close()
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
print "# reading stderr"
pr=1
while pr != []:
 pr,pw,px=select.select([p.stderr],[],[],tmout)
 if pr != []:
  l=pr[0].readline()
  if len(l) != 0:
   print "stderr ",l
  else:
   pr=[]

#
# == Submit the jobs ===
#
print '# submiting jobs.'
rc=remoteLoginCmd.split()
p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0)
p.stdin.write("cd %s\n"%tpath)
for jf in jflist:
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
