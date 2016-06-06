Code related to displaying and extracting standard output size tiles

* ```Makefile``` has commands to execute the codes in this directory. Starting from a binary
   bathymetry file the codes generate a hyperlinked file of sub-tile thumbnail images that are linked
   to full resolution images that show the coordinate extents for the each sub-tile. LLC output can
   then be selected, extracted and downloaded by sub-tile.

   *  ```matlab_make_tilemap/``` has matlab code to read a binary bathymetry file and produce a master
   jpeg file that shows the bathymetry split into numbered sub-tiles plotted on the default LLC
   layout.

   * ```make_tilemap_webpage/``` has shell scripts that take the jpeg produced by the matlab code in 
   ```matlab_make_tilemap/``` and create a set of per sub-tile images and thumbnails, and then generate
   html that shows the images in the default LLC layout.

To execute matlab step
```
make subtile_coords.jpeg
```
