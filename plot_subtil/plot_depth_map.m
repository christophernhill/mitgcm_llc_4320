pNo=372;
nx=1080;
ny-540;

dName=sprintf('Depth.p_%4.4d.data',pNo);
xcName=sprintf('XC.p_%4.4d.data',pNo);
ycName=sprintf('YC.p_%4.4d.data',pNo);

fid=fopen(dName,'r','ieee-be');
dVals=fread(fid,[nx ny],'float32');
fclose(fid);
dVals(find(dVals==0))=NaN;

fid=fopen(xcName,'r','ieee-be');
xcVals=fread(fid,[nx ny],'float32');
fclose(fid);

fid=fopen(ycName,'r','ieee-be');
ycVals=fread(fid,[nx ny],'float32');
fclose(fid);

pcolor(xcVals,ycVals,-dVals);axis ij;axis equal;shading flat;axis xy
xlabel('Longitude');
ylabel('Latitude');
title('Depth');
colorbar
