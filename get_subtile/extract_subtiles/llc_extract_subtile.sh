#!/bin/bash
#
# Script to extract subtile from LLC global tile
#
nLLC=4320;
nTx=1080;
nTy=540;
bs=4;
#
#         VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM
# ./a.out U   4    3241 4320 2701 3240 1    34590
# e.g.
# ./llc_extract_subtile.sh  Eta   4    3241 4320 2701 3240 1 484560
#

var=$1
if [ "x${var}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# var = "$var

face=$2
if [ "x${face}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# face = "$face

ilo=$3
if [ "x${ilo}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# ilo = "$ilo

ihi=$4
if [ "x${ihi}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# ihi = "$ihi

jlo=$5
if [ "x${jlo}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# jlo = "$jlo

jhi=$6
if [ "x${jhi}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# jhi = "$jhi

klev=$7
if [ "x${klev}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# klev = "$klev

tnum=$8
if [ "x${tnum}" == "x" ]; then
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# tnum = "$tnum

obase=-1;
tstep=-1;
elperlev=$((${nLLC}*${nLLC}*3+${nLLC}*${nLLC}*3+${nLLC}*${nLLC}+${nLLC}*${nLLC}*3${nLLC}*${nLLC}*3))
if [ ${face} -eq 1 ]; then
 obase=0;
 tstepj=$nLLC;
fi
if [ ${face} -eq 2 ]; then
 obase=$((${nLLC}*${nLLC}*3))
 tstepj=$nLLC;
fi
if [ ${face} -eq 3 ]; then
 obase=$((${nLLC}*${nLLC}*3+${nLLC}*${nLLC}*3))
 tstepj=$nLLC;
fi
if [ ${face} -eq 4 ]; then
 obase=$((${nLLC}*${nLLC}*3+${nLLC}*${nLLC}*3+${nLLC}*${nLLC}))
 tstepj=$(($nLLC*3));
fi
if [ ${face} -eq 5 ]; then
 obase=$((${nLLC}*${nLLC}*3+${nLLC}*${nLLC}*3+${nLLC}*${nLLC}+${nLLC}*${nLLC}*3))
 tstepj=$(($nLLC*3));
fi

if [ ${obase} -lt 0 ]; then
 echo "Error: FACE must be in range 1-5"
 echo "Usage: "$0" VAR FACE ILO  IHI  JLO  JHI  KLEV TNUM"
 exit
fi
echo "# obase = "${obase}

fname=`printf '%s.%10.10d.data' ${var} ${tnum}`
echo "# fname = "${fname}
 
efname=`printf '%s.%10.10d-f%d-ilo%4.4d-ihi%4.4d-jlo%4.4d-jhi%4.4d-k%3.3d.data.extract' ${var} ${tnum} ${face} ${ilo} ${ihi} ${jlo} ${jhi} ${klev}`
echo > ${efname}
\rm ${efname}
touch ${efname}
for j in $( seq ${jlo} ${jhi} ); do
 sk=$(((${klev}-1)*${elperlev}+$obase+(${j}-1)*${tstepj}+${ilo}-1))
 nel=$((${ihi}-${ilo}+1))
 dd if=${fname} bs=${bs} skip=${sk} count=${nel} 2>/dev/null >> ${efname}
done

