#!/bin/bash
# 
# llcijtoxcyc.sh gridfiledir llcsize facenumber iface jface
#
# e.g.
# llcijtoxcyc.sh ../grid 4320 5 3000 4000
# 30.657W, 2.453S
#
# example
# ./make_tilemap_webpage/llcijtoxcyc.sh ../../../grid 4032 1 10 1 2> /dev/null | tail -2 | head -1 | awk '{print $2}'
#
usage=" gridfiledir llcsize facenumber iface jface"

#
gd=$1   # Should be an existing directory
if [ "x${gd}" = "x" ]; then
 echo "Usage: "$0" "${usage}
 exit
fi
echo "# gd="${gd}
if [ ! -d ${gd} ]; then
 echo "Directory \"${gd}\" not found."
 exit
fi

#
nrgb=$2  # Should be a positive integer
if [ "x${nrgb}" = "x" ]; then
 echo "Usage: "$0" "${usage}
 exit
fi
echo "# nrgb="${nrgb}
if [[ $nrgb =~ ^[+]?[1-9][0-9]*$ ]]; then
 true
else
 echo "nrgb value "${nrgb}" is not a positive integer."
 exit
fi

#
nfac=$3  # Should be in range 1-5
if [ "x${nfac}" = "x" ]; then
 echo "Usage: "$0" "${usage}
 exit
fi
echo "# nfac="${nfac}
if [[ $nfac =~ ^[+]?[1-9][0-9]*$ ]]; then
 true
else
 echo "nfac value "${nfac}" is not a positive integer."
 exit
fi
if [ $nfac -lt 1 ] || [ $nfac -gt 5 ]; then
 echo "nfac value "${nfac}" is not in range 1-5."
 exit
fi

#
iface=$4 # Should be positive integer and less than ${nrgb}*3+1
if [ "x${iface}" = "x" ]; then
 echo "Usage: "$0" "${usage}
 exit
fi
echo "# iface="${iface}
if [[ $iface =~ ^[+]?[1-9][0-9]*$ ]]; then
 true
else
 echo "iface value "${iface}" is not a positive integer."
 exit
fi
if [ $iface -gt $((${nrgb}*3)) ]; then
 echo "iface value "${iface}" is not in range 1-$((${nrgb}*3))."
 exit
fi

#
jface=$5 # Should be positive integer and less than ${nrgb}*3+1
if [ "x${jface}" = "x" ]; then
 echo "Usage: "$0" "${usage}
 exit
fi
echo "# jface="${jface}
if [[ $jface =~ ^[+]?[1-9][0-9]*$ ]]; then
 true
else
 echo "jface value "${jface}" is not a positive integer."
 exit
fi
if [ $jface -gt $((${nrgb}*3)) ]; then
 echo "jface value "${jface}" is not in range 1-$((${nrgb}*3))."
 exit
fi

#
if [ ! -d ${gd} ]; then
 echo "Error: Directory \"${gd}\" not found."
 exit
fi

if [ $nfac -eq 1 ]; then
 nskipLon=$(( ($jface-1)*($nrgb+1)+$iface-1                          ))
 nskipLat=$(( ($jface-1)*($nrgb+1)+$iface-1 +($nrgb+1)*(($nrgb*3)+1) ))
fi
if [ $nfac -eq 2 ]; then
 nskipLon=$(( ($jface-1)*($nrgb+1)+$iface-1                          ))
 nskipLat=$(( ($jface-1)*($nrgb+1)+$iface-1 +($nrgb+1)*(($nrgb*3)+1) ))
fi
if [ $nfac -eq 3 ]; then
 nskipLon=$(( ($jface-1)*($nrgb+1)+$iface-1                          ))
 nskipLat=$(( ($jface-1)*($nrgb+1)+$iface-1 +($nrgb+1)*($nrgb+1)     ))
fi
if [ $nfac -eq 4 ]; then
 nskipLon=$(( ($jface-1)*(($nrgb*3)+1)+$iface-1                           ))
 nskipLat=$(( ($jface-1)*(($nrgb*3)+1)+$iface-1 + ($nrgb+1)*(($nrgb*3)+1) ))
fi
if [ $nfac -eq 5 ]; then
 nskipLon=$(( ($jface-1)*(($nrgb*3)+1)+$iface-1                           ))
 nskipLat=$(( ($jface-1)*(($nrgb*3)+1)+$iface-1 + ($nrgb+1)*(($nrgb*3)+1) ))
fi

# echo $nskipLon
# echo $nskipLat
tfnam="tile"`printf '%3.3d' $nfac`".mitgrid"
# echo ${tfnam}

degLon=`( dd if=${gd}/${tfnam} skip=${nskipLon} bs=8 count=1 ) 2> /dev/null |  \
          LC_ALL=C sed s'/\(.\)\(.\)\(.\)\(.\)\(.\)\(.\)\(.\)\(.\)/\8\7\6\5\4\3\2\1/' | ( dd bs=8 count=1 ) 2> /dev/null | od -t fD | tail -2 | head -1 | awk '{print $2}'`
degLon=`printf '%4.2f' ${degLon}`
degLat=`( dd if=${gd}/${tfnam} skip=${nskipLat} bs=8 count=1 ) 2> /dev/null |  \
          LC_ALL=C sed s'/\(.\)\(.\)\(.\)\(.\)\(.\)\(.\)\(.\)\(.\)/\8\7\6\5\4\3\2\1/' | ( dd bs=8 count=1 ) 2> /dev/null | od -t fD | tail -2 | head -1 | awk '{print $2}'`
degLat=`printf '%4.2f' ${degLat}`
echo $degLon","$degLat
