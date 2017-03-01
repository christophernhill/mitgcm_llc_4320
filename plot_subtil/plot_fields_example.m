pNo=372;
pNo=278;
itNo=685152;
kLev=30;
pRoot='/nfs/cnhlab002/cnh/llc4320/tiled_output/'

dName=sprintf( '%s/p_%3.3d/grid/Depth.p_%4.4d.data',pRoot,pNo,pNo);
xcName=sprintf('%s/p_%3.3d/grid/XC.p_%4.4d.data',pRoot,pNo,pNo);
ycName=sprintf('%s/p_%3.3d/grid/YC.p_%4.4d.data',pRoot,pNo,pNo);
xgName=sprintf( '%s/p_%3.3d/grid/XG.p_%4.4d.data',pRoot,pNo,pNo);
ygName=sprintf( '%s/p_%3.3d/grid/YG.p_%4.4d.data',pRoot,pNo,pNo);
rcName=sprintf( '%s/p_%3.3d/grid/RC.p_%4.4d.data',pRoot,pNo,pNo);

dte=datestr(datenum(2011,9,10)+itNo*25/60/60/24,-1);

subplot(3,4,1)

fid=fopen(dName,'r','ieee-be');
dVals=fread(fid,[1080 540],'float32');
fclose(fid);
dVals(find(dVals==0))=NaN;

fid=fopen(xcName,'r','ieee-be');
xcVals=fread(fid,[1080 540],'float32');
fclose(fid);

fid=fopen(ycName,'r','ieee-be');
ycVals=fread(fid,[1080 540],'float32');
fclose(fid);

fid=fopen(xgName,'r','ieee-be');
xgVals=fread(fid,[1080 540],'float32');
fclose(fid);

fid=fopen(ygName,'r','ieee-be');
ygVals=fread(fid,[1080 540],'float32');
fclose(fid);

fid=fopen(rcName,'r','ieee-be');
rcVals=fread(fid,'float32');
fclose(fid);

subplot(3,4,1)

pcolor(xcVals,ycVals,-dVals);axis ij;axis equal;shading flat;axis xy
xlabel('Longitude');
ylabel('Latitude');
title('Depth','FontSize',6);
colorbar

subplot(3,4,2)

thetaName=sprintf( '%s/p_%3.3d/i_%15.15d/Theta/Theta.%10.10d.p_%4.4d.k_%4.4d.data',pRoot,pNo,itNo,itNo,pNo,kLev);

fid=fopen(thetaName,'r','ieee-be');
thVals=fread(fid,[1080 540],'float32');
fclose(fid);
thVals(find(thVals==0))=NaN;

dep=rcVals(kLev);

pcolor(xcVals,ycVals,thVals);axis ij;axis equal;shading flat;axis xy
xlabel('Longitude');
ylabel('Latitude');
pt1='Potential Temperature';
pt2=sprintf(', %6.2fm',dep);
pt3=sprintf(' %s',dte);
pt={pt1,pt2,pt3};
title(pt,'FontSize',6);
colorbar

subplot(3,4,3)

etaName=sprintf( '%s/p_%3.3d/i_%15.15d/Eta/Eta.%10.10d.p_%4.4d.k_%4.4d.data',pRoot,pNo,itNo,itNo,pNo,1);

fid=fopen(etaName,'r','ieee-be');
etaVals=fread(fid,[1080 540],'float32');
fclose(fid);
etaVals(find(dVals==0))=NaN;

pcolor(xcVals,ycVals,etaVals);axis ij;axis equal;shading flat;axis xy
xlabel('Longitude');
ylabel('Latitude');
pt1='Sea Surface Height';
pt2=sprintf('%s',dte);
pt={pt1,pt2};
title(pt,'FontSize',6);
colorbar

subplot(3,4,4)

uName=sprintf( '%s/p_%3.3d/i_%15.15d/U/U.%10.10d.p_%4.4d.k_%4.4d.data',pRoot,pNo,itNo,itNo,pNo,kLev);

fid=fopen(uName,'r','ieee-be');
uVals=fread(fid,[1080 540],'float32');
fclose(fid);
uVals(find(uVals==0))=NaN;

dep=rcVals(kLev);

pcolor(xgVals,ycVals,uVals);axis ij;axis equal;shading flat;axis xy
xlabel('Longitude');
ylabel('Latitude');
pt1='Local grid U';
pt2=sprintf('%6.2fm',dep);
pt3=sprintf('%s',dte);
pt={pt1,pt2,pt3};
title(pt,'FontSize',6);
colorbar

subplot(3,4,5)

vName=sprintf( '%s/p_%3.3d/i_%15.15d/V/V.%10.10d.p_%4.4d.k_%4.4d.data',pRoot,pNo,itNo,itNo,pNo,kLev);

fid=fopen(vName,'r','ieee-be');
vVals=fread(fid,[1080 540],'float32');
fclose(fid);
vVals(find(vVals==0))=NaN;

dep=rcVals(kLev);

pcolor(xcVals,ygVals,vVals);axis ij;axis equal;shading flat;axis xy
xlabel('Longitude');
ylabel('Latitude');
pt1='Local grid V';
pt2=sprintf('%6.2fm',dep);
pt3=sprintf('%s',dte);
pt={pt1,pt2,pt3};
title(pt,'FontSize',6);
colorbar
