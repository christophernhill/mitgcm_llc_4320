# Python program to generate and submit jobs to extract all iterations and fields
# for a given standard tile.
#
#
import subprocess
import errno
import sys
import os
import select

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
itHi=10368+144*4
itStride=144
itList=range(itLo,itHi+1,itStride)

# Config settings
# Edit this to use relevant ids, key and host
remoteLoginCmd="ssh -T -A -l cnh -i  ~/.ssh/id_rsa.pub eofe7.mit.edu ssh -T -A -p 20002 cnhill1@localhost"
remoteStoreDirRoot="/nobackupp8/cnhill1/llc_4320_tiles/tiled_output"
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


jobHeader=[]
jobHeader.append('#PBS -S /bin/bash')
jobHeader.append('#PBS -l select=1:ncpus=16:model=san')
jobHeader.append('#PBS -l walltime=00:60:00')
jobHeader.append('#PBS -q normal')
jobHeader.append('#PBS -j oe')
jobHeader.append('#PBS -m abe')
jobHeader.append('#PBS -M cnh@mit.edu')

ni=len(itList)
print '# ',ni,' iterations requested to be tar archived for transfer'
print '# start=',itList[0]
print '#   end=',itList[-1]

print '# Checking to see if expected directories exist'
dl=[]
for i in itList:
 dl.append("i_%15.15d"%i);

dlr=[]
rdFull="%s/p_%3.3d"%(remoteStoreDirRoot,tNo)
print "# Reading remote directory ",rdFull
rc=remoteLoginCmd.split()
p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
pr=1
while pr != []:
 pr,pw,px=select.select([p.stdout],[],[],tmout)
 if pr != []:
  l=pr[0].readline()
  sys.stdout.write(l)
  sys.stdout.flush()
p.stdin.write("cd %s\n"%rdFull)
p.stdin.write("/bin/ls -1 %s | grep i_ | sort\n"%rdFull)
pr,pw,px=select.select([p.stdout],[],[],tmout)
if pr == []:
 print "# remote connect test timed out"
 exit()
else:
 pr=1
 nl=0
 while pr != []:
  pr,pw,px=select.select([p.stdout],[],[],tmout)
  if pr != []:
   l=pr[0].readline()
   if len(l) != 0:
    nl=nl+1
    dlr.append(l.rstrip())
    sys.stdout.write("\r%s"%l.rstrip())
    sys.stdout.flush()
   else:
    pr=[]
print ""
p.stdin.close()

dlrem=set(dlr)
dlreq=set(dl)

if dlreq <= dlrem:
 print "# Directory names that will be requested are in the set of directory names listed remotely."
 print "#",dl[0],dlr[0]
 print "#","        :        "
 print "#","        :        "
 print "#","        :        "
 print "#",dl[-1],dlr[-1]
else:
 print "# ERROR: Some directories to be requested are not in the set of directories found."

# Now check if directories contain expected numbers of files - to make sure the extract stage has completed.

# First create working directory for temporary files on remote host
# Example commands that run
# mkdir -p job_staging/ ; mktemp -d job_staging/llc_tar_XXXXXX
# cd job_staging/llc_extract_GpkaZE; gcc ~/src/fs_tools/src/threaded_dtree_scan/rd2.c -lpthread
# cd job_staging/llc_extract_GpkaZE; ./a.out /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_299/ | grep 000  | awk 'BEGIN{n=0}{if (n%1000==0){printf("%-50s%10d\n", $0,n)};n=n+1}END{printf("%-50s%10d\n",$0,n)}
# sys.stdout.write(tcOut)
# sys.stdout.flush()
# exit()
print '# Setting up working directory on remote host.'
rc=remoteLoginCmd.split()
p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0)
p.stdin.write("mkdir -p %s/\n"%remJobFileDir)
pr = 1
while pr != []:
 pr,pw,px=select.select([p.stdout],[],[],tmout)
 if pr != []:
  l=pr[0].readline()
  sys.stdout.write("%s\n"%l.rstrip())
  sys.stdout.flush()
print '# connected and root staging directory created.'
print '# creating work directory and checking that expected files are present.'
p.stdin.write("mktemp -d %s/llc_tar_XXXXXX\n"%remJobFileDir)
tpath=p.stdout.readline()
tpath=tpath[0:-1]
cmd="cd %s; gcc ~/src/fs_tools/src/threaded_dtree_scan/rd2.c -lpthread\n"%tpath
p.stdin.write(cmd);
pr = 1
while pr != []:
 pr,pw,px=select.select([p.stdout],[],[],tmout)
 if pr != []:
  l=pr[0].readline()
  sys.stdout.write("%s\n"%l.rstrip())
  sys.stdout.flush()
cmd="cd ~/%s; ./a.out %s | grep 000 | awk 'BEGIN{n=0}{if(n%%1000==0){printf(\"%%-50s%%10d\\n\",$0,n)};n=n+1}END{printf(\"%%-50s%%10d\\n\",$0,n)}'\n"%(tpath,rdFull)
p.stdin.write(cmd)
pr = 1
l  = "EMPTY"
while pr != []:
 pr,pw,px=select.select([p.stdout],[],[],tmout)
 if pr != []:
  l=pr[0].readline()
  sys.stdout.write("\r%s"%l.rstrip())
  sys.stdout.flush()
p.stdin.close()
sys.stdout.write("\n")
sys.stdout.flush()
lspl=l.split()
nfExpect=459
if int(lspl[1])%nfExpect != 0:
 print "ERROR: Number of files in remote directories is not a multiple of %d!"%(nfExpect)
 exit()

# Create tar jobs

# exit()

### #PBS -S /bin/bash
### #PBS -l select=1:ncpus=16:model=san
### #PBS -l walltime=00:60:00
### #PBS -q normal
### #PBS -j oe
### #PBS -m abe
### #PBS -M cnh@mit.edu
### 
### module load python/2.7.10
### # cd /home4/cnhill1/projects/get_alll_llc/python/mitgcm_llc_4320/get_subtil_py
### cd /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_278
### tar -cvf tar00195.tar \
### i_000000001358208 \
### i_000000001358352 \
### i_000000001358640 \
### i_000000001358784 \
### i_000000001359072 \
### i_000000001359216 \
### i_000000001359504 \
### i_000000001359648 \
### i_000000001359936 \
### i_000000001360080 \
### i_000000001360368 \
### i_000000001360512 \
### i_000000001360800 \
### i_000000001360944 \
### i_000000001361232 \
### i_000000001361376 \
### i_000000001361664 \
### i_000000001361808 \
### i_000000001362096 \
### i_000000001362240 \
### i_000000001362528 \
### i_000000001362672 \
### i_000000001362960 \
### i_000000001363104 \
### i_000000001363392 \
### i_000000001363536 \
### i_000000001363824 \
### i_000000001363968 \
### i_000000001364256 \
### i_000000001364400 \
### i_000000001364688 \
### i_000000001364832 \
### ;


#
# 1. Generate tile extract jobs
print "# Generating tile extract jobs for tile %d"%tNo,"iteration count, %d, and iteration range = %d-%d"%(len(itList),itLo,itHi)
# Create blocks tar commands that each archive 32 directories
jw=0 
ni=0
nj=0
# Open first job file
jfName="%s/%s-%4.4d.pbs"%(jobDir,jobPref,nj)
print jfName
exit()
for i in itlist:
 ni=ni+1
 if jw == 0:
  # Write header
  jw=1
 if ni%32 == 0:
  # Write close
  # Open next file
  nj=nj+1
  jfName="%s/%s-%4.4d.pbs"%(jobDir,jobPref,nj)

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


# Now do file check
## nfExpect=459
## rc=remoteLoginCmd.split()
## p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
## pr=1
## while pr != []:
##  pr,pw,px=select.select([p.stdout],[],[],tmout)
##  if pr != []:
##   l=pr[0].readline()
##   sys.stdout.write(l)
##   sys.stdout.flush()
## "/u/cnhill1/src/fs_tools/src/threaded_dtree_scan"
## CHANGE a.out to CORRECT PATH
## p.stdin.write("./a.out /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_299/ | grep 000  | awk 'BEGIN{n=0}{if (n%1000==0){printf("%-50s%10d\n", $0,n)};n=n+1}END{printf("%-50s%10d\n",$0,n)}' %s\n"%rdFull)
## pr,pw,px=select.select([p.stdout],[],[],tmout)
## if pr == []:
##  print "# remote connect test timed out"
##  exit()
## else:
##  pr=1
##  nl=0
##  while pr != []:
##   pr,pw,px=select.select([p.stdout],[],[],tmout)
##   if pr != []:
##    l=pr[0].readline()
##    if len(l) != 0:
##     nl=nl+1
##     dlr.append(l.rstrip())
##     sys.stdout.write("\r%s"%l.rstrip())
##     sys.stdout.flush()
##    else:
##     pr=[]
## print ""
## p.stdin.close()

## exit()

########################################

###   ###   #PBS -S /bin/bash
###   #PBS -l select=1:ncpus=16:model=san
###   #PBS -l walltime=00:60:00
###   #PBS -q normal
###   #PBS -j oe
###   #PBS -m abe
###   #PBS -M cnh@mit.edu
###   
###   module load python/2.7.10
###   # cd /home4/cnhill1/projects/get_alll_llc/python/mitgcm_llc_4320/get_subtil_py
###   cd /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_278
###   tar -cvf tar00090.tar \
###   i_000000000632448 \
###   i_000000000632592 \
###   i_000000000632880 \
###   i_000000000633024 \
###   i_000000000633312 \
###   i_000000000633456 \
###   i_000000000633744 \
###   i_000000000633888 \
###   i_000000000634176 \
###   i_000000000634320 \
###   i_000000000634608 \
###   i_000000000634752 \
###   i_000000000635040 \
###   i_000000000635184 \
###   i_000000000635472 \
###   i_000000000635616 \
###   i_000000000635904 \
###   i_000000000636048 \
###   i_000000000636336 \
###   i_000000000636480 \
###   i_000000000636768 \
###   i_000000000636912 \
###   i_000000000637200 \
###   i_000000000637344 \
###   i_000000000637632 \
###   i_000000000637776 \
###   i_000000000638064 \
###   i_000000000638208 \
###   i_000000000638496 \
###   i_000000000638640 \
###   i_000000000638928 \
###   i_000000000639072 \
###   ;
###   
###   
###   jobHeader.append('module load python/2.7.10')
###   jobHeader.append('cd /home4/cnhill1/projects/get_alll_llc/python/mitgcm_llc_4320/get_subtil_py')
###   # python  simple_extract_looping_driver.py   17280,17568,144 & </dev/null
###   
###   # Check connectivity
###   print "# Testing remote connection"
###   testCommand="%s %s"%(remoteLoginCmd,"pwd")
###   try:
###    tcOut=subprocess.check_output(testCommand,stderr=subprocess.STDOUT,shell=True)
###   except subprocess.CalledProcessError, e:
###    print "    Error testing connection with","\"%s\""%testCommand
###    print "    Error message:"
###    print "   ","\"%s\""%e.output
###    exit()
###   else:
###    print "#  connection test passed"
###   
###   # 1. Generate tile extract jobs
###   print "# Generating tile extract jobs for tile %d"%tNo,"iteration count, %d, and iteration range = %d-%d"%(len(itList),itLo,itHi)
###   # Create blocks extract commands that each execute 3 extracts.
###   clist=[]
###   for it1,it2 in [ (itList[i], itList[i+2]) for i in range(0,len(itList)-2,3) ]:
###    crec="%s %s %d,%d,%d"%("python","someCommand",it1,it2,itStride)
###    clist.append(crec)
###   # Group thesse in sets of 16 per job file
###   nc=0
###   nj=0
###   for c in clist:
###    if nc == 0:
###     cblock=[]
###    crec="%s &"%(c)
###    cblock.append(crec)
###    if (nc+1)%16 == 0:
###     print "%s%s-%5.5d%s"%("######",jobFilePref,nj,".pbs")
###     for jh in jobHeader: print jh
###     print "export LLC_TEXTRACT_TNO=%d"%tNo
###     for cb in cblock:
###      print "%s"%cb
###     print "wait"
###     nc=0
###     nj=nj+1
###    else:
###     nc=nc+1
###   if nc > 0:
###    print "%s%s-%5.5d%s"%("######",jobFilePref,nj,".pbs")
###    for jh in jobHeader: print jh
###    print "export LLC_TEXTRACT_TNO=%d"%tNo
###    for cb in cblock:
###     print "%s"%cb
###    print "wait"
