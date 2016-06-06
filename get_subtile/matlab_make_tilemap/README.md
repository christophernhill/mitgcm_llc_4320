Matlab that produces a bathymetry map with tile numbers marked

* plot_bathy.m -- main driver (reads ```bathy4320_g5_r4``` as input). Input file is read from directory given in
  environment variable ```INPUT_DIR```.

* The program writes a file ```subtile_coords.jpeg``` that shows
  subpanel numbers overlaid on a global bathymetry map and arranged in raw LLC
  orientation. File is written to directory given by environment variable ```OUTPUT_DIR```.
