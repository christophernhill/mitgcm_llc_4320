#!/bin/bash

nx=4320;

cd ${odir}

echo "<table>"
echo "<tr>"
echo "<td width=\"22%\">"

echo "<table>"

n0=93;
for j in $(seq 0 15); do
 echo "<tr>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
 echo "</tr>"
done
for j in $(seq 0 23); do
 echo "<tr>"
 for i in $(seq 0  3); do
  fsuf=`printf "%3.3d" $(( ${i} + ${n0} ))`
  fnum=`echo ${fsuf} | sed s'/[0]*\(.*\)/\1/'`
  tijvals=( `${t2ijcmd} ${fnum} | sed s/'\(.*\)#.*/\1/'  | grep '[0-9]' `)
  # ./make_tilemap_webpage/llcfijtoxcyc.sh ../../../grid 4320 1 4320 8640
  ilo=${tijvals[0]}
  ihi=${tijvals[1]}
  jlo=${tijvals[2]}
  jhi=${tijvals[3]}
  fno=${tijvals[4]}
  c_tl=`${llgetcmd} ${gdir} ${nx} ${fno} ${ilo} ${jhi} | tail -1`
  c_tr=`${llgetcmd} ${gdir} ${nx} ${fno} ${ihi} ${jhi} | tail -1`
  c_br=`${llgetcmd} ${gdir} ${nx} ${fno} ${ihi} ${jlo} | tail -1`
  c_bl=`${llgetcmd} ${gdir} ${nx} ${fno} ${ilo} ${jlo} | tail -1`
  echo "<td> <a href=\"${wptilepage}?tnum=${fsuf}&c_tl=${c_tl}&c_tr=${c_tr}&c_br=${c_br}&c_bl=${c_bl}&ilof=${tijvals[0]}&ihif=${tijvals[1]}&jlof=${tijvals[2]}&jhif=${tijvals[3]}\"><img class=\"cell_image\" src=\"${wpimgdir}subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
 done
 echo "</tr>"
 n0=$(($n0-4))
done

echo "</table>"

echo "</td>"

echo "<td width=\"22%\">"
echo "<table>"

n0=221;
for j in $(seq 0 7); do
 echo "<tr>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
 echo "</tr>"
done
for j in $(seq 0 31); do
 echo "<tr>"
 for i in $(seq 0  3); do
  fsuf=`printf "%3.3d" $(( ${i} + ${n0} ))`
  fnum=`echo ${fsuf} | sed s'/[0]*\(.*\)/\1/'`
  tijvals=( `${t2ijcmd} ${fnum} | sed s/'\(.*\)#.*/\1/'  | grep '[0-9]' `)
  ilo=${tijvals[0]}
  ihi=${tijvals[1]}
  jlo=${tijvals[2]}
  jhi=${tijvals[3]}
  fno=${tijvals[4]}
  c_tl=`${llgetcmd} ${gdir} ${nx} ${fno} ${ilo} ${jhi} | tail -1`
  c_tr=`${llgetcmd} ${gdir} ${nx} ${fno} ${ihi} ${jhi} | tail -1`
  c_br=`${llgetcmd} ${gdir} ${nx} ${fno} ${ihi} ${jlo} | tail -1`
  c_bl=`${llgetcmd} ${gdir} ${nx} ${fno} ${ilo} ${jlo} | tail -1`
  echo "<td> <a href=\"${wptilepage}?tnum=${fsuf}&c_tl=${c_tl}&c_tr=${c_tr}&c_br=${c_br}&c_bl=${c_bl}&ilof=${tijvals[0]}&ihif=${tijvals[1]}&jlof=${tijvals[2]}&jhif=${tijvals[3]}\"><img class=\"cell_image\" src=\"${wpimgdir}subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
 done
 echo "</tr>"
 n0=$(($n0-4))
done

echo "</table>"
echo "</td>"

echo "<td width=\"66%\">"
echo "<table>"

n0=405;
for j in $(seq 0 15); do
 echo "<tr>"
 for i in $(seq 0  11); do
  fsuf=`printf "%3.3d" $(( ${i} + ${n0} ))`
  fnum=`echo ${fsuf} | sed s'/[0]*\(.*\)/\1/'`
  tijvals=( `${t2ijcmd} ${fnum} | sed s/'\(.*\)#.*/\1/'  | grep '[0-9]' `)
  ilo=${tijvals[0]}
  ihi=${tijvals[1]}
  jlo=${tijvals[2]}
  jhi=${tijvals[3]}
  fno=${tijvals[4]}
  c_tl=`${llgetcmd} ${gdir} ${nx} ${fno} ${ilo} ${jhi} | tail -1`
  c_tr=`${llgetcmd} ${gdir} ${nx} ${fno} ${ihi} ${jhi} | tail -1`
  c_br=`${llgetcmd} ${gdir} ${nx} ${fno} ${ihi} ${jlo} | tail -1`
  c_bl=`${llgetcmd} ${gdir} ${nx} ${fno} ${ilo} ${jlo} | tail -1`
  echo "<td> <a href=\"${wptilepage}?tnum=${fsuf}&c_tl=${c_tl}&c_tr=${c_tr}&c_br=${c_br}&c_bl=${c_bl}&ilof=${tijvals[0]}&ihif=${tijvals[1]}&jlof=${tijvals[2]}&jhif=${tijvals[3]}\"><img class=\"cell_image\" src=\"${wpimgdir}subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
 done
 echo "</tr>"
 n0=$(($n0-12))
done
for j in $(seq 0 23); do
 echo "<tr>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
  echo "<td> <img class=\"cell_image\" src=\"${wpimgdir}white_pad.jpeg\"> </td>"
 echo "</tr>"
done
# </tr>

echo "</table>"
echo "</td>"

echo "</tr>"
echo "</table>"

