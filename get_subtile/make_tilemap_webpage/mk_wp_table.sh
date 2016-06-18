#!/bin/bash

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
  echo "<td> <a href=\"${wptilepage}?tnum=${fsuf}\"><img class=\"cell_image\" src=\"${wpimgdir}subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
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
  echo "<td> <a href=\"${wptilepage}?tnum=${fsuf}\"><img class=\"cell_image\" src=\"${wpimgdir}subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
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
  echo "<td> <a href=\"${wptilepage}?tnum=${fsuf}\"><img class=\"cell_image\" src=\"${wpimgdir}subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
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

