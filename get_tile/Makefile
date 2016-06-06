# Create tiled images, thumbnails and .html pages for displaying them.
#
# Steps
#
# 1. matlab reads master bathymetry bindary file and creates
#    high-res .pnm with bathymetry in tiles with 1 pixel
#    per grid cell and laid out in LLC layout.
#    Tiles are numbered sequentially within each of the
#    13 subpanels.
#
#
# 2. netpbm programs split high-res .pnm into one full res jpeg
#    per file and one thumbnail jpeg per file
#
#
# 3. shell script generates .html file with table that displays
#    individual thumbnail images in LLC layout. Each thumbnail is
#    hyperlinked to page displaying full resolution tile,
#    its information and a form to request data extract.
#

default: 
	@ echo "Generate tiled .html file"
