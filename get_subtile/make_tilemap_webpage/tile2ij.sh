#!/bin/bash
#
# For given tile number figure out face and i,j for each corner (bl, br, tr, tl)
#
#
tno=1;
if [ "x${1}" != "x" ]; then
 tno=$1
fi
tx=1080;
ty=540;
nllc=4320;

xm=$(( ${nllc}*${nllc}/(${tx}*${ty}) ))
# echo $xm

# Get panel number
pno=$(( (${tno}-1)/${xm}+1 ));
echo "# pno = "$pno

# Get face number, face dimensions and tile rank within
# face.
fno=0
if [ ${pno} -ge  1 ] && [ ${pno} -le  3 ]; then
 fno=1
 fx=${nllc}
 fy=$(( ${nllc}*3 ))
 ntx=$(( ${fx}/${tx} ))
 nty=$(( ${fy}/${ty} ))
 t0=1
fi
if [ ${pno} -ge  4 ] && [ ${pno} -le  6 ]; then
 fno=2
 fx=${nllc}
 fy=$(( ${nllc}*3 ))
 ntx=$(( ${fx}/${tx} ))
 nty=$(( ${fy}/${ty} ))
 t0=$(( 3*${nllc}*${nllc}/(${tx}*${ty}) + 1 ))
fi
if [ ${pno} -ge  7 ] && [ ${pno} -le  7 ]; then
 fno=3
 fx=${nllc}
 fy=${nllc}
 ntx=$(( ${fx}/${tx} ))
 nty=$(( ${fy}/${ty} ))
 t0=$(( 6*${nllc}*${nllc}/(${tx}*${ty}) + 1 ))
fi
if [ ${pno} -ge  8 ] && [ ${pno} -le 10 ]; then
 fno=4
 fx=$(( ${nllc}*3 ))
 fy=${nllc}
 ntx=$(( ${fx}/${tx} ))
 nty=$(( ${fy}/${ty} ))
 t0=$(( 7*${nllc}*${nllc}/(${tx}*${ty}) + 1 ))
fi
if [ ${pno} -ge 11 ] && [ ${pno} -le 13 ]; then
 fno=5
 fx=$(( ${nllc}*3 ))
 fy=${nllc}
 ntx=$(( ${fx}/${tx} ))
 nty=$(( ${fy}/${ty} ))
 t0=$(( 10*${nllc}*${nllc}/(${tx}*${ty}) + 1 ))
fi
if [ ${fno} -eq 0 ]; then
 exit
fi

echo "# t0  = "${t0}

ftnoy=$(( (${tno}-${t0})/${ntx} + 1 ))
echo "# ftnoy  = "${ftnoy}
ftnox=$(( ${tno}-${t0}-(${ftnoy}-1)*${ntx} + 1 ))
echo "# ftnox  = "${ftnox}

ilo=$(( (${ftnox}-1)*${tx}+1 ))
ihi=$(( (${ftnox}-0)*${tx}   ))
jlo=$(( (${ftnoy}-1)*${ty}+1 ))
jhi=$(( (${ftnoy}-0)*${ty}   ))

echo "# fno = "${fno}
echo "# ilo = "${ilo}
echo "# ihi = "${ihi}
echo "# jlo = "${jlo}
echo "# jhi = "${jhi}

echo $ilo, $jlo " # bl "
echo $ihi, $jlo " # br "
echo $ihi, $jhi " # tr "
echo $ilo, $jhi " # tl "

# tnox=$(( ${tno}/


