#!/bin/bash
#
# bbscp -p 8 -X 88000 -V -l /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_278/tar00304.tar cnh@eofe7.mit.edu:/nfs/cnhlab002/cnh | tee bbscp.log
#
#
echo "cd /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_278"

cd /nobackupp8/cnhill1/llc_4320_tiles/tiled_output/p_278

for f in tar*.tar  ; do
 echo ${f} | awk '{print "bbscp -p 8 -X 88000 -V -l "$1" cnh@eofe7.mit.edu:/nfs/cnhlab002/cnh | tee bbscp"$1".log"}'
done

cd -
echo "cd -"
