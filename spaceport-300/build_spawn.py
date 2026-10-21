"""Deterministic original Minecraft 1.8.8 floating spaceport schematic."""
import gzip, struct, pathlib, random, zipfile, hashlib
import numpy as np
from PIL import Image, ImageDraw
P=pathlib.Path(__file__).parent
W=L=300; H=96
b=np.zeros((H,L,W),dtype=np.uint8); d=np.zeros_like(b)
def box(x0,y0,z0,x1,y1,z1,block,meta=0):
 x0,x1=max(0,x0),min(W-1,x1); z0,z1=max(0,z0),min(L-1,z1); y0,y1=max(0,y0),min(H-1,y1)
 if x1<x0 or y1<y0 or z1<z0:return
 b[y0:y1+1,z0:z1+1,x0:x1+1]=block; d[y0:y1+1,z0:z1+1,x0:x1+1]=meta
# Broad flat octagonal deck, with a layered underside and lit edge.
for z in range(300):
 for x in range(300):
  if abs(x-149.5)+abs(z-149.5)>258:continue
  b[7:10,z,x]=98; b[10,z,x]=43; d[10,z,x]=0
  if x%12==0 or z%12==0:b[10,z,x]=98
  if x<3 or x>296 or z<3 or z>296 or abs(x-149.5)+abs(z-149.5)>255:
   b[10,z,x]=155;b[11,z,x]=160;d[11,z,x]=5
# Flat, white central concourse and four broad approaches.
box(132,10,16,167,10,283,155);box(16,10,132,283,10,167,155)
for v in (130,169):
 box(v,10,20,v,10,279,159,9);box(20,10,v,279,10,v,159,9)
for a in range(26,278,12):
 for v in (132,167):box(v,10,a,v,10,a+2,89);box(a,10,v,a+2,10,v,89)
# Landing pad: concentric square/octagonal geometric rings, all at deck height.
for z in range(117,183):
 for x in range(117,183):
  r=max(abs(x-149.5),abs(z-149.5)); q=abs(x-149.5)+abs(z-149.5)
  if q<48:
   b[10,z,x]=155
   if 38<q<42:b[10,z,x]=159;d[10,z,x]=5
   if r<10:b[10,z,x]=98
box(148,10,140,151,10,159,155);box(140,10,148,159,10,151,155)
# Four open public facilities around the plaza: framed hangars with walkable interiors.
def building(cx,cz,sx,sz,height,variant):
 x0=cx-sx//2;x1=cx+sx//2;z0=cz-sz//2;z1=cz+sz//2; roof=11+height
 box(x0,11,z0,x1,roof,z1,159,9)
 box(x0+2,11,z0+2,x1-2,roof-2,z1-2,0)
 box(x0,11,z0,x1,11,z1,155)
 # Horizontal bands and window strips on all four faces.
 for yy in range(16,roof-3,8):
  box(x0,yy,z0,x1,yy+1,z0,155);box(x0,yy,z1,x1,yy+1,z1,155)
  box(x0,yy,z0,x0,yy+1,z1,155);box(x1,yy,z0,x1,yy+1,z1,155)
  box(x0+3,yy+2,z0,x1-3,yy+4,z0,95,9);box(x0+3,yy+2,z1,x1-3,yy+4,z1,95,9)
  box(x0,yy+2,z0+3,x0,yy+4,z1-3,95,9);box(x1,yy+2,z0+3,x1,yy+4,z1-3,95,9)
 for xx in (x0,x1):
  for zz in (z0,z1):box(xx-1,11,zz-1,xx+1,roof+2,zz+1,98)
 # Cross-axis passages allow entry from all sides, without functional plugin content.
 box(cx-3,12,z0,cx+3,17,z1,0);box(x0,12,cz-3,x1,17,cz+3,0)
 box(x0-2,roof,z0-2,x1+2,roof+1,z1+2,155)
 box(x0+3,roof+2,z0+3,x1-3,roof+3,z1-3,159,9)
 box(cx-4,roof+4,cz-4,cx+4,roof+7,cz+4,155)
 box(cx-2,roof+5,cz-5,cx+2,roof+6,cz-5,95,5)
 # Green power modules in prominent white face frames.
 for zz in (z0-1,z1+1):
  box(cx-6,roof-11,zz,cx+6,roof-2,zz,155)
  box(cx-4,roof-9,zz,cx+4,roof-4,zz,159,15)
  box(cx-2,roof-8,zz,cx+2,roof-5,zz,95,5)
 # Ceiling lighting and decorative interior counters.
 for xx in range(x0+5,x1-3,8):
  box(xx,roof-1,cz-1,xx+1,roof-1,cz+1,89)
 for xx in (x0+4,x1-4):
  box(xx,12,z0+5,xx,13,z0+10,5);box(xx,12,z1-10,xx,13,z1-5,5)
for args in [(90,92,40,42,34,0),(210,92,42,40,40,1),(90,210,40,42,28,2),(210,210,42,42,34,3)]:building(*args)
# Tall asymmetric outer pylons, observation windows and ribbed facades.
for cx,cz,ht in [(46,111,49),(253,189,56),(110,254,47),(190,45,54)]:
 box(cx-8,11,cz-8,cx+8,11+ht,cz+8,159,9)
 for yy in range(15,ht+8,7):
  box(cx-10,yy,cz-10,cx+10,yy+1,cz+10,155)
  box(cx-7,yy+2,cz-9,cx+7,yy+4,cz-9,95,9)
 box(cx-4,ht+13,cz-4,cx+4,ht+17,cz+4,155)
 box(cx-2,ht+14,cz-5,cx+2,ht+16,cz-5,95,5)
 box(cx,ht+18,cz,cx,ht+24,cz,101)
# Plaza stalls / crates display pedestals, wood accents like the reference.
for cx,cz in [(117,117),(182,117),(117,182),(182,182)]:
 for off in (-5,5):
  box(cx+off-2,11,cz-2,cx+off+2,11,cz+2,155)
  box(cx+off-1,12,cz-1,cx+off+1,12,cz+1,5)
  box(cx+off,13,cz,cx+off,13,cz,89)
# Seating, planters, lamp posts along the concourse.
for a in (32,58,84,216,242,268):
 for side in (121,178):
  box(a-3,11,side-1,a+3,11,side+1,5)
  box(a-3,12,side+1,a+3,12,side+1,5)
  box(side-1,11,a-3,side+1,11,a+3,5)
  box(side+1,12,a-3,side+1,12,a+3,5)
for x,z in [(120,46),(179,46),(120,254),(179,254),(46,120),(46,179),(254,120),(254,179)]:
 box(x-2,11,z-2,x+2,12,z+2,155);box(x-1,13,z-1,x+1,13,z+1,18)
 box(x,14,z,x,21,z,101);box(x-1,22,z-1,x+1,22,z+1,89);box(x-2,23,z-2,x+2,23,z+2,44)
# Spacecraft landing strips.
for cx,cz in [(65,45),(235,255)]:
 box(cx-22,11,cz-10,cx+22,11,cz+10,159,15)
 for xx in range(cx-20,cx+21,8):box(xx,11,cz-9,xx+3,11,cz-9,159,5);box(xx,11,cz+9,xx+3,11,cz+9,159,5)
 # Small block-built parked shuttle.
 box(cx-12,12,cz-2,cx+12,14,cz+2,155);box(cx-4,14,cz-4,cx+5,17,cz+4,155)
 box(cx+6,15,cz-2,cx+9,16,cz+2,95,9)
 box(cx-7,13,cz-10,cx+2,13,cz+10,159,9)
 for zz in (cz-4,cz+4):box(cx-14,12,zz,cx-10,14,zz,98);box(cx-15,13,zz,cx-15,13,zz,89)
# Suspended asteroid clusters, away from walkways.
rng=random.Random(731)
for cx,cz,cy,r in [(25,30,50,12),(276,28,59,13),(28,275,54,13),(274,274,64,11),(21,70,71,6),(278,82,78,7),(72,281,70,7),(240,19,78,6)]:
 for yy in range(cy-r,cy+r+1):
  for zz in range(cz-r,cz+r+1):
   for xx in range(cx-r,cx+r+1):
    dist=((xx-cx)/r)**2+((yy-cy)/(r*1.15))**2+((zz-cz)/r)**2
    if dist<.78+rng.random()*.28:
     block=rng.choice([1,1,1,3,172]);box(xx,yy,zz,xx,yy,zz,block)
# Export classic MCEdit/WorldEdit Alpha schematic (1.8 block IDs).
def utf(s):
 q=s.encode();return struct.pack('>H',len(q))+q
def tag(t,n,p):return bytes([t])+utf(n)+p
def short(n,v):return tag(2,n,struct.pack('>h',v))
def integer(n,v):return tag(3,n,struct.pack('>i',v))
root=short('Width',W)+short('Height',H)+short('Length',L)+tag(8,'Materials',utf('Alpha'))
for name,a in [('Blocks',b),('Data',d)]:
 raw=a.tobytes();root+=tag(7,name,struct.pack('>i',len(raw))+raw)
for n in ('Entities','TileEntities'):root+=tag(9,n,b'\x0a'+struct.pack('>i',0))
for n,v in [('WEOriginX',0),('WEOriginY',0),('WEOriginZ',0),('WEOffsetX',-150),('WEOffsetY',-11),('WEOffsetZ',-150)]:root+=integer(n,v)
path=P/'Astro-Inspired-Spaceport-300.schematic'
with gzip.open(path,'wb') as f:f.write(b'\x0a'+utf('Schematic')+root+b'\0')
# Actual block-derived top-down preview, not a gameplay screenshot.
colors={0:(17,23,36),1:(115,118,125),3:(121,85,58),5:(160,133,86),18:(61,108,69),43:(165,167,167),44:(164,165,165),89:(237,207,122),95:(70,144,143),98:(114,120,128),101:(115,127,139),155:(224,224,214),159:(58,68,76),160:(132,208,67),172:(148,108,82)}
rgb=np.zeros((L,W,3),dtype=np.uint8)
for z in range(L):
 for x in range(W):
  ys=np.flatnonzero(b[:,z,x]); y=int(ys[-1]) if len(ys) else 0; bid=int(b[y,z,x]);c=colors.get(bid,(160,160,160))
  if bid==159 and d[y,z,x]==5:c=(126,183,45)
  light=.72+.28*y/80
  rgb[z,x]=tuple(min(255,int(v*light)) for v in c)
im=Image.fromarray(rgb).resize((1200,1200),Image.Resampling.NEAREST)
canvas=Image.new('RGB',(1280,1320),(17,23,36));canvas.paste(im,(40,70));dr=ImageDraw.Draw(canvas)
dr.text((40,23),'ASTRO-INSPIRED SPACEPORT | 300 x 300 | MINECRAFT 1.8.8',(235,240,245))
dr.text((40,1280),'Actual schematic top view | central landing pad / hangars / towers / shuttles / asteroids',(205,215,225))
canvas.save(P/'Top-Down-Preview.png')
print('Blocks:',int(np.count_nonzero(b)),'dimensions:',(W,H,L),'schematic bytes:',path.stat().st_size)
assert b.shape==(96,300,300) and b.max()<=197
assert np.all(b[11:14,148:152,148:152]==0),'Spawn must be clear'
assert b[10,150,150]!=0
