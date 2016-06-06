#!/bin/bash
#
#
# cat subpanel1080x540_llc4320_map.pnm | pamcut -left=0 -right=1079 -bottom=21599 -top=-539  | pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_p001.jpeg
#
#
npsy=540;
npsx=1080;
npy=8;npym1=$((${npy}-1));
npx=4;npxm1=$((${npx}-1));
itile=0;
for np in $(seq 0 12); do
 for ny in $(seq 0 ${npym1}); do
  for nx in $(seq 0 ${npxm1}); do
   itilestr=`printf "%3.3d" $(($itile+1))`

   if [ ${np} -lt 3 ]; then
    lval=$((0 + ${nx}*${npsx}))
    bval=$((21599 - ${npsy}*${ny} - ${npsy}*${npy}*${np}))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -gt 2 ] && [ ${np} -lt 7 ]; then
    lval=$((4320 + ${nx}*${npsx}))
    bval=$((21599 - ${npsy}*${ny} - ${npsy}*${npy}*$((${np}-3))))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -eq 7 ]; then
    lval=$((     0 + 2*${npx}*${npsx} + ${nx}*${npsx} ))
    bval=$(( 21599 - 3*${npsy}*${npy} - ${ny}*${npsy} ))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -eq 8 ]; then
    lval=$((     0 + 3*${npx}*${npsx} + ${nx}*${npsx} ))
    bval=$(( 21599 - 3*${npsy}*${npy} - ${ny}*${npsy} ))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -eq 9 ]; then
    lval=$((     0 + 4*${npx}*${npsx} + ${nx}*${npsx} ))
    bval=$(( 21599 - 3*${npsy}*${npy} - ${ny}*${npsy} ))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -eq 10 ]; then
    lval=$((     0 + 2*${npx}*${npsx} + ${nx}*${npsx} ))
    bval=$(( 21599 - 4*${npsy}*${npy} - ${ny}*${npsy} ))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -eq 11 ]; then
    lval=$((     0 + 3*${npx}*${npsx} + ${nx}*${npsx} ))
    bval=$(( 21599 - 4*${npsy}*${npy} - ${ny}*${npsy} ))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   if [ ${np} -eq 12 ]; then
    lval=$((     0 + 4*${npx}*${npsx} + ${nx}*${npsx} ))
    bval=$(( 21599 - 4*${npsy}*${npy} - ${ny}*${npsy} ))
    echo 'cat subpanel1080x540_llc4320_map.pnm |' \
         "pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
         '|' 'pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
   fi

   itile=$(($itile+1))
  done
 done
done
