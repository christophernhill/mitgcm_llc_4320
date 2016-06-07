#!/bin/bash
#
#
# cat subpanel1080x540_llc4320_map.pnm | pamcut -left=0 -right=1079 -bottom=21599 -top=-539  | pnmtojpeg -quality=100 > subpanel1080x540_llc4320_map_p001.jpeg
#
#
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
 if [ ${fn} -eq 1 ]; then
  bval0=$((${nx}*5-1))
  lval0=0;
 fi
 if [ ${fn} -eq 2 ]; then
  bval0=$((${nx}*5-1))
  lval0=$((${nx}));
 fi
 if [ ${fn} -eq 3 ]; then
  bval0=$((${nx}*2-1))
  lval0=$((${nx}));
 fi
 if [ ${fn} -eq 4 ]; then
  bval0=$((${nx}*2-1))
  lval0=$((${nx}*2));
 fi
 if [ ${fn} -eq 5 ]; then
  bval0=$((${nx}-1))
  lval0=$((${nx}*2));
 fi
 npx=$((${nxf}/${npsx}))
 npy=$((${nyf}/${npsy}))
 # echo "Face "${fn}" npx="${npx}" npy="${npy}" lval0="${lval0}" bval0="${bval0}
 
 for nty in $(seq 0 $((npy-1))); do
  for ntx in $(seq 0 $((npx-1))); do
   itile=$(($itile+1))
   lval=$(($lval0 + ${ntx}*${npsx}))
   bval=$(($bval0 - ${nty}*${npsy}))
   # echo "tile ="${itile}" lval="${lval}" bval="${bval}
   itilestr=`printf "%3.3d" $(($itile))`
   echo "cat ${idir}/subtile_coords.pnm " \
        "| pamcut -left="${lval} "-bottom="${bval} "-width="${npsx} "-height="${npsy} \
        '|' 'pnmtojpeg -quality=100 > '${odir}'/subpanel1080x540_llc4320_map_'${itilestr}".jpeg"
  done
 done
done
