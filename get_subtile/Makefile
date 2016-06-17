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

MATLAB_CMD=/Applications/MATLAB_R2015b.app/bin/matlab -nodisplay -nodesktop
GRID_INPUT_DIR=~/projects/llc_extract/grid
OUTPUT_DIR=~/projects/llc_extract/output
SRC_DIR=~/projects/llc_extract/git/mitgcm_llc_4320
PLOT_BATHY_CMD_PATH=/get_subtile/matlab_make_tilemap/plot_bathy.m
MAKE_TILE_JPEG_CMD_PATH=/get_subtile/make_tilemap_webpage/mk_panel_jpegs.sh
MAKE_THUMBS_CMD_PATH=/get_subtile/make_tilemap_webpage/mk_thumbs.sh
MAKE_HTML_CMD_PATH=/get_subtile/make_tilemap_webpage/mk_html.sh
MAKE_WPTABLE_CMD=/get_subtile/make_tilemap_webpage/mk_wp_table.sh
GET_LL_CMD_PATH=/get_subtile/make_tilemap_webpage/llcfijtoxcyc.sh
HTML_OUT=$(OUTPUT_DIR)/x.html
WPTABLE_OUT=$(OUTPUT_DIR)/wptable.html
WP_IMG_DIR=/wp-content/uploads/2016/06/
WP_TILE_PAGE=/index.php/home/fetch-output/single-tile-fetch/

default: 
	@ echo "Generate tiled .html file"
	@ echo "MATLAB command = "$(MATLAB_CMD)
	@ echo "Input directory = "$(GRID_INPUT_DIR)
	@ echo "Output directory = "$(OUTPUT_DIR)
	@ echo "Targets"
	@ echo "make subtile_coords.jpeg - Run matlab to write master jpeg to output directory."
	@ echo "make tile_jpegs          - Run Netpbm commands to create individual tile jpeg images."
	@ echo "make thumbs              - Run Netpbm commands to create thumbnail tile jpeg images."
	@ echo "make html                - Run commands to create html table layout with hyperlinks."
	@ echo "make all                 - Run all commands in sqeuence."
	@ echo "Note - To copy WP table to server scp ../../../output/wptable.html  llc4320mitgcm@llc4320.mitgcm.org:php_includes/master_tile_layout.php"

all: 
	make subtile_coords.jpeg
	make tile_jpegs
	make thumbs
	make html

subtile_coords.jpeg:
	INPUT_DIR=$(GRID_INPUT_DIR) OUTPUT_DIR=$(OUTPUT_DIR) $(MATLAB_CMD) -r "run $(SRC_DIR)$(PLOT_BATHY_CMD_PATH)"
	cd $(OUTPUT_DIR); cat subtile_coords.jpeg | jpegtopnm > subtile_coords.pnm

tile_jpegs:
	idir=$(OUTPUT_DIR) odir=$(OUTPUT_DIR) $(SRC_DIR)$(MAKE_TILE_JPEG_CMD_PATH) | bash -e

thumbs:
	idir=$(OUTPUT_DIR) odir=$(OUTPUT_DIR) $(SRC_DIR)$(MAKE_THUMBS_CMD_PATH)

html: html_files wp_files
html_files:
	llgetcmd=$(SRC_DIR)$(GET_LL_CMD_PATH) \
        gdir=$(GRID_INPUT_DIR)                \
        idir=$(OUTPUT_DIR)                    \
        odir=$(OUTPUT_DIR)                    \
        $(SRC_DIR)$(MAKE_HTML_CMD_PATH) > $(HTML_OUT)
wp_files:
	llgetcmd=$(SRC_DIR)$(GET_LL_CMD_PATH) \
        gdir=$(GRID_INPUT_DIR)                \
        idir=$(OUTPUT_DIR)                    \
        odir=$(OUTPUT_DIR)                    \
        wpimgdir=$(WP_IMG_DIR)                \
        wptilepage=$(WP_TILE_PAGE)            \
        $(SRC_DIR)$(MAKE_WPTABLE_CMD) > $(WPTABLE_OUT)
