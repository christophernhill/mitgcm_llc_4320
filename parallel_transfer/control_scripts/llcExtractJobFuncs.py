#
#  Functions and tools used to run jobs automatically
#
import subprocess
import errno
import sys
import os
import select


class llcExtractJobFuncs:

 ###
 ### Begin __init__
 ###
 def __init__(this,tmout,tNo, itList, remoteStoreDirRoot, remoteLoginCmd, remJobFileDir,jobFileDir,jobFilePref):
  this.tmout=tmout
  this.tNo=tNo
  this.itList=itList
  this.remoteStoreDirRoot=remoteStoreDirRoot
  this.remoteLoginCmd=remoteLoginCmd
  this.rdFull="%s/p_%3.3d"%(remoteStoreDirRoot,tNo)
  this.remJobFileDir=remJobFileDir
  this.jobFileDir=jobFileDir
  this.jobFilePref=jobFilePref
 ###
 ### End __init__
 ###

 ###
 ### Begin checkRemTileDirPresent
 ###
 def checkRemTileDirPresent( this ):

  remoteStoreDirRoot=this.remoteStoreDirRoot
  tNo=this.tNo
  itList=this.itList
  remoteLoginCmd=this.remoteLoginCmd
  rdFull=this.rdFull

  print '# Checking to see if expected directories exist'
  dl=[]
  for i in itList:
   dl.append("i_%15.15d"%i);
  
  dlr=[]
  print "# Reading remote directory ",rdFull
  rc=remoteLoginCmd.split()
  p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  pr=1
  while pr != []:
   pr,pw,px=select.select([p.stdout],[],[],this.tmout)
   if pr != []:
    l=pr[0].readline()
    sys.stdout.write(l)
    sys.stdout.flush()
  p.stdin.write("cd %s\n"%rdFull)
  p.stdin.write("/bin/ls -1 %s | grep i_ | sort\n"%rdFull)
  pr,pw,px=select.select([p.stdout],[],[],this.tmout)
  if pr == []:
   print "# remote connect test timed out"
   exit()
  else:
   pr=1
   nl=0
  while pr != []:
   pr,pw,px=select.select([p.stdout],[],[],this.tmout)
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
   return 0
  else:
   print "# ERROR: Some directories to be requested are not in the set of directories found."
   return -1
 ###
 ### End checkRemTileDirPresent
 ###

 ###
 ### Beging checkRemFileCount
 ###
 def checkRemFileCount( this ):
  # First create working directory for temporary files on remote host
  # Example commands that run
  # mkdir -p job_staging/ ; mktemp -d job_staging/llc_tar_XXXXXX
  # cd job_staging/llc_extract_GpkaZE; gcc ~/src/fs_tools/src/threaded_dtree_scan/rd2.c -lpthread
  # cd job_staging/llc_extract_GpkaZE; ./a.out /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_299/ | grep 000  | awk 'BEGIN{n=0}{if (n%1000==0){printf("%-50s%10d\n", $0,n)};n=n+1}END{printf("%-50s%10d\n",$0,n)}
  # sys.stdout.write(tcOut)
  # sys.stdout.flush()
  # exit()

  remoteLoginCmd=this.remoteLoginCmd
  tmout=this.tmout
  remJobFileDir=this.remJobFileDir
  rdFull=this.rdFull

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
   return -1
  else:
   return 0
 ###
 ### End checkRemFileCount
 ###

 ###
 ### Begin standardJobHeader
 ###
 def standardJobHeader(this):
  sHead=["#PBS -S /bin/bash",
         "#PBS -l select=1:ncpus=16:model=san",
         "#PBS -l walltime=00:60:00",
         "#PBS -q normal",
         "#PBS -j oe",
         "#PBS -m abe",
         "#PBS -M cnh@mit.edu",
         "",
         "module load python/2.7.10"]
  return sHead
 ###
 ### End standardJobHeader
 ###

 ###
 ### Begin writeTarJob
 ###
 def writeTarJob(this,tNo,itList):

   remoteLoginCmd=this.remoteLoginCmd
   tmout=this.tmout
   remJobFileDir=this.remJobFileDir
   rdFull=this.rdFull
   jobFileDir=this.jobFileDir
   jobFilePref=this.jobFilePref
   remoteStoreDirRoot=this.remoteStoreDirRoot

   jfList=[]
   sh=this.standardJobHeader()
   jw=0
   ni=0
   nj=0
   # Open first job file
   jfName="%s/%s-%4.4d.pbs"%(jobFileDir,jobFilePref,nj)
   jfList.append(jfName)
   f=open(jfName,'w')
   for s in sh: print >> f, s
   print >> f, "cd %s/p_%3.3d"%(remoteStoreDirRoot,tNo)
   print >> f, "tar -cvf tar%6.6d.tar \\"%nj
   for i in itList:
    ni=ni+1
    if jw == 0:
     # Write header
     jw=1
    if ni%64 == 0:
     # Write close
     print >> f, ';'
     f.close()
     # Open next file
     nj=nj+1
     jfName="%s/%s-%4.4d.pbs"%(jobFileDir,jobFilePref,nj)
     jfList.append(jfName)
     f=open(jfName,'w')
     for s in sh: print >> f, s
     print >> f, "cd %s/p_%3.3d"%(remoteStoreDirRoot,tNo)
     print >> f, "tar -cvf tar%6.6d.tar \\"%nj
     print >> f, "i_%15.15d"%i, "\\"
    else:
     print >> f, "i_%15.15d"%i, "\\"
   print >> f, ';'
   f.close()
   return jfList
 ###
 ### End writeTarJob
 ###

 ###
 ### Begin writeTarInMem
 ###
 def writeTarInMem(this,jflist):
   # Create in memory tar file
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
   return tcOut
 ###
 ### End writeTarInMem
 ###


 ###
 ### Begin unTarOnRemote
 ###
 def unTarOnRemote(this,tcOut):
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
    remoteLoginCmd=this.remoteLoginCmd
    tmout=this.tmout
    remJobFileDir=this.remJobFileDir
    rdFull=this.rdFull
    jobFileDir=this.jobFileDir
    jobFilePref=this.jobFilePref
    remoteStoreDirRoot=this.remoteStoreDirRoot

    rc=remoteLoginCmd.split()
    p=subprocess.Popen(rc,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0)
    p.stdin.write("mkdir -p %s/\n"%remJobFileDir)
    pr = 1
    while pr != []:
     pr,pw,px=select.select([p.stdout],[],[],tmout)
     if pr != []:
      pr[0].readline()
    print '# connected and root staging directory created.'
    p.stdin.write("mktemp -d %s/%s_XXXXXX\n"%(remJobFileDir,jobFilePref))
    tpath=p.stdout.readline()
    tpath=tpath[0:-1]
    print "%s \"%s\"%s"%('# transfer sub-directory',tpath,' created.')
    p.stdin.write("cd %s\n"%tpath)
    p.stdin.write("pwd\n")
    p.stdin.write("tar -xf -\n")
    p.stdin.write("%s"%tcOut)
    p.stdin.close()
    print "# reading stdout"
    pr=1
    while pr != []:
     pr,pw,px=select.select([p.stdout],[],[],tmout)
     if pr != []:
      l=pr[0].readline()
      if len(l) != 0:
       print "stdout ",l.strip()
      else:
       pr=[]
    print "# reading stderr"
    pr=1
    while pr != []:
     pr,pw,px=select.select([p.stderr],[],[],tmout)
     if pr != []:
      l=pr[0].readline()
      if len(l) != 0:
       print "stderr ",l.strip()
      else:
       pr=[]
    return tpath
 ###
 ### End unTarOnRemote
 ###
