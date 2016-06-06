function [bathy]=read_bathy(fnam,nx)
% Read in llc SSH and reshape to latlon "belt" and polar cap.
% nx = 4320 for llc_4320
 bathy=[];
 fid=fopen(fnam,'r','ieee-be');
 if fid <= 0
  return
 end
 bathyIn=reshape(fread(fid,(nx)*(nx)*13,'float32'),[nx nx 13]);
 fclose(fid);
 bathy=bathyIn;
 phi=cat(2,bathyIn(:,:, 8), bathyIn(:,:, 9), bathyIn(:,:,10));
 bathy(:,:, 8)=phi(:,1:3:end-2);
 bathy(:,:, 9)=phi(:,2:3:end-1);
 bathy(:,:,10)=phi(:,3:3:end  );

 % Face 5 - Eastern Pac (and GoM)
 phi=cat(2,bathyIn(:,:,11), bathyIn(:,:,12), bathyIn(:,:,13));
 bathy(:,:,11)=phi(:,1:3:end-2);
 bathy(:,:,12)=phi(:,2:3:end-1);
 bathy(:,:,13)=phi(:,3:3:end  );

 bathy(find(bathy==0))=NaN;
end
