function draw_numbered_subtiles(nt1,np)

% Calculate face-number and offsets
if np < 13 & np >= 10
 fn=5;
 ntb=10;
 nst=8;
 nt0=10*8*4;
 nt1=nt0+(np-10)*4+1;
end
if np < 10 & np >= 7
 fn=4;
 ntb=7;
 nst=8;
 nt0=7*8*4;
 nt1=nt0+(np-7)*4+1;
end
if np < 7
 fn=3;
 ntb=nt1;
 nst=0;
end
if np < 6
 fn=2;
 ntb=nt1;
 nst=0;
end
if np < 3
 fn=1;
 ntb=nt1;
 nst=0;
end

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
nt=nt+nst;
end

end
