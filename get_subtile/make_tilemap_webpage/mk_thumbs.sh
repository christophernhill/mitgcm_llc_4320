#!/bin/bash
#
#
cd ${odir}
fl=`ls -1 subpanel1080x540_llc4320_map_[0-9][0-9][0-9].jpeg`
# cat subpanel1080x540_llc4320_map_415.jpeg | jpegtopnm | pnmscale 0.2 | pnmtojpeg -q 30 > subpanel1080x540_llc4320_map_415_thumb.jpeg
for f in ${fl} ; do
 tname=${f%*.*}"_thumb.jpeg"
 cat ${f} | jpegtopnm | pnmscale 0.2 | pnmtojpeg -q 30 > ${tname}
done
cp  subpanel1080x540_llc4320_map_001_thumb.jpeg subpanel1080x540_llc4320_map_pad_thumb.jpeg 
#
# RGBDEF pathname on Mac. May need chaging for different platform
#
RGBDEF=/opt/X11/share/X11/rgb.txt
export RGBDEF
cat subpanel1080x540_llc4320_map_pad_thumb.jpeg | jpegtopnm | ppmchange -closeness=100 white white  | pnmtojpeg -q 100 > white_pad.jpeg
