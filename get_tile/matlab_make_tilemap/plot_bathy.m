%
% Make plot of sub patches for experimentally splitting raw output for download
% Plot shows bathymetry in native llc orientation and marks sub patches that are
% 1080 x 540 cells in horizontal size.
% Each cell has a number that indicates a region that is used for breaking up
% output into some manageable pieces.
% A single sub path is about 2.5MB, an hourly series over a year is about 21GB.
% All 90 levels are about 1.9TB.
%
nx=4320;
nsby=8;
nsbx=4;

if isempty(getenv('INPUT_DIR'))
 exit;
else
 idir=getenv('INPUT_DIR');
end

if isempty(getenv('OUTPUT_DIR'))
 exit;
else
 odir=getenv('OUTPUT_DIR');
end

ibfile=sprintf('%s/%s',idir,'bathy4320_g5_r4');

b=read_bathy(ibfile,nx);
eps=0.002;
eps=0.000;
fw=0.2-eps;
fh=0.2-eps;
clf;hold on;
set(gcf,'PaperSize',[36 36]);
set(gcf,'PaperPosition',[0 0 36 36]);
np=13;  gca=subplot('Position',[0.8 0.8 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.6 0.8 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.4 0.8 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.8 0.6 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.6 0.6 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.4 0.6 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.2 0.6 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.2 0.4 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.2 0.2 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.2 0.0 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.0 0.4 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.0 0.2 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

np=np-1;gca=subplot('Position',[0.0 0.0 fw fh]);imagesc(b(:,:,np)');set(gca,'YTick',[],'XTick',[]);caxis([-10000 0]);axis xy;hold on
nt1=(np-1)*nsby*nsbx+1;draw_numbered_subtiles(nt1);

cd(odir)
print('-djpeg100','-r600','subtile_coords.jpeg');
% print('-depsc2','-r2400','subtile_coords.ps')
exit

