#!/bin/bash

cd ${odir}

echo "<html>"
cat <<'EOF'
<head>
<style type="text/css">
  table{
    border-collapse: collapse;
    border: 0px solid black;
    padding: 0;
    margin:  0;
  }
  table td{
    border: 0px solid black;
    padding: 0;
    margin:  0;
  }
</style>
</head>
EOF

echo "<body>"
echo "<table>"
echo "<tr>"

echo "<td>"
echo "<table>"

n0=93;
for j in $(seq 0 15); do
 echo "<tr>"
  echo "<td> <img src=\"white_pad.jpeg\"> </td>"
 echo "</tr>"
done
for j in $(seq 0 23); do
 echo "<tr>"
 for i in $(seq 0  3); do
  fsuf=`printf "%3.3d" $(( ${i} + ${n0} ))`
  echo "<td> <a href=\"subpanel1080x540_llc4320_map_${fsuf}.html\"><img src=\"subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
 done
 echo "</tr>"
 n0=$(($n0-4))
done

echo "</table>"
echo "</td>"

echo "<td>"
echo "<table>"

n0=221;
for j in $(seq 0 7); do
 echo "<tr>"
  echo "<td> <img src=\"white_pad.jpeg\"> </td>"
 echo "</tr>"
done
for j in $(seq 0 31); do
 echo "<tr>"
 for i in $(seq 0  3); do
  fsuf=`printf "%3.3d" $(( ${i} + ${n0} ))`
  echo "<td> <a href=\"subpanel1080x540_llc4320_map_${fsuf}.html\"><img src=\"subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
 done
 echo "</tr>"
 n0=$(($n0-4))
done

echo "</table>"
echo "</td>"

echo "<td>"
echo "<table>"

n0=405;
for j in $(seq 0 15); do
 echo "<tr>"
 for i in $(seq 0  11); do
  fsuf=`printf "%3.3d" $(( ${i} + ${n0} ))`
  echo "<td> <a href=\"subpanel1080x540_llc4320_map_${fsuf}.html\"><img src=\"subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
 done
 echo "</tr>"
 n0=$(($n0-12))
done
for j in $(seq 0 23); do
 echo "<tr>"
  echo "<td> <img src=\"white_pad.jpeg\"> </td>"
 echo "</tr>"
done
# </tr>

echo "</table>"
echo "</td>"

echo "</tr>"
echo "</table>"
echo "</div>"
echo "</body>"
echo "</html>"


npsy=540;
npsx=1080;
nx=4320;


itile=0
for fn in $(seq 1 5); do
 if [ ${fn} -eq 1 ] || [ ${fn} -eq 2 ]; then
  nxf=$((${nx}  ))
  nyf=$((${nx}*3))
 fi
 if [ ${fn} -eq 3 ]; then
  nxf=$((${nx}  ))
  nyf=$((${nx}  ))
 fi
 if [ ${fn} -eq 4 ] || [ ${fn} -eq 5 ]; then
  nxf=$((${nx}*3))
  nyf=$((${nx}  ))
 fi
 npx=$((${nxf}/${npsx}))
 npy=$((${nyf}/${npsy}))
 # echo "Face "${fn}" npx="${npx}" npy="${npy}" lval0="${lval0}" bval0="${bval0}
 
 for nty in $(seq 0 $((npy-1))); do
  for ntx in $(seq 0 $((npx-1))); do
   itile=$(($itile+1))
   itilestr=`printf "%3.3d" $(($itile))`
   (
   echo "<html>"
   echo "<head>"
   echo "</head>"
   echo "<body>"
   echo "<div width=\"100%\">"
   echo "<table width=\"95%\" align=\"center\">"
   ilof=$((${ntx}*${npsx}+1))
   ihif=$((${ilof}+${npsx}-1))
   jlof=$((${nty}*${npsy}+1))
   jhif=$((${jlof}+${npsy}-1))
   # ./make_tilemap_webpage/llcfijtoxcyc.sh ../../../grid 4320 1 4320 8640
   llstr_tl=`${llgetcmd} ${gdir} ${nx} ${fn} ${ilof} ${jhif} | tail -1`
   llstr_bl=`${llgetcmd} ${gdir} ${nx} ${fn} ${ilof} ${jlof} | tail -1`
   llstr_tr=`${llgetcmd} ${gdir} ${nx} ${fn} ${ihif} ${jhif} | tail -1`
   llstr_br=`${llgetcmd} ${gdir} ${nx} ${fn} ${ihif} ${jlof} | tail -1`

   echo "<tr>"
   echo "<td>"
   echo "LLC Face "${fn}"</br>"
   echo "(i<sub>face</sub>,j<sub>face</sub>)=("${ilof}","${jhif}")</br>"
   echo "(Lon<sub>E</sub>,Lat)=("$llstr_tl")"
   echo "</td>"
   echo "<td>"
   echo "&nbsp;"
   echo "</td>"
   echo "<td>"
   echo "LLC Face "${fn}"</br>"
   echo "(i<sub>face</sub>,j<sub>face</sub>)=("${ihif}","${jhif}")</br>"
   echo "(Lon<sub>E</sub>,Lat)=("$llstr_tr")"
   echo "</td>"
   echo "</tr>"

   echo "<tr>"
   echo "<td>"
   echo "&nbsp;"
   echo "</td>"
   echo "<td>"
   echo "<img width=\"100%\" src=subpanel1080x540_llc4320_map_"${itilestr}".jpeg>"
   echo "</td>"
   echo "<td>"
   echo "&nbsp;"
   echo "</td>"
   echo "</tr>"

   echo "<tr>"
   echo "<td>"
   echo "LLC Face "${fn}"</br>"
   echo "(i<sub>face</sub>,j<sub>face</sub>)=("${ilof}","${jlof}")</br>"
   echo "(Lon<sub>E</sub>,Lat)=("$llstr_bl")"
   echo "</td>"
   echo "<td>"
   echo "&nbsp;"
   echo "</td>"
   echo "<td>"
   echo "LLC Face "${fn}"</br>"
   echo "(i<sub>face</sub>,j<sub>face</sub>)=("${ihif}","${jlof}")</br>"
   echo "(Lon<sub>E</sub>,Lat)=("$llstr_br")"
   echo "</td>"
   echo "</tr>"

   echo "</table>"
   echo "</div>"

   echo "</body>"
   echo "</html>"

   ) > "subpanel1080x540_llc4320_map_"${itilestr}".html"
  done
 done
done
