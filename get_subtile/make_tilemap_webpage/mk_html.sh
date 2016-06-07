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
  echo "<td> <a href=\"subpanel1080x540_llc4320_map_${fsuf}.jpeg\"><img src=\"subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
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
  echo "<td> <a href=\"subpanel1080x540_llc4320_map_${fsuf}.jpeg\"><img src=\"subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
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
  echo "<td> <a href=\"subpanel1080x540_llc4320_map_${fsuf}.jpeg\"><img src=\"subpanel1080x540_llc4320_map_${fsuf}_thumb.jpeg\"></a> </td>"
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
echo "</body>"
echo "</html>"

