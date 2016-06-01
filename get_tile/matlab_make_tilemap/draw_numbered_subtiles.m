function draw_numbered_subtiles(nt1)
dx=1080;
dy=540;
nt=nt1;
ylo=0;
for nsy=1:8
xlo=0;
for nsx=1:4
xhi=xlo+dx-0.5;
yhi=ylo+dy-0.5;
plot([xlo xhi xhi xlo xlo],[ylo ylo yhi yhi ylo],'k');
tt=sprintf('%3.3d',nt);
h=text(xlo+(xhi-xlo)*0.5,ylo+(yhi-ylo)*0.5,tt);
set(h,'Color',[0.6 0.6 0.6]);
set(h,'HorizontalAlignment','center');
xlo=xlo+dx;
nt=nt+1;
end
ylo=ylo+dy;
end

end
