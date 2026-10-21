import os
os.environ['MPLCONFIGDIR']='/tmp/astro-mpl'
import gzip,struct,pathlib,math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=pathlib.Path(__file__).parent
raw=gzip.decompress((P/'Astro-Inspired-Spaceport-300.schematic').read_bytes())
def arr(name):
 needle=b'\x07'+struct.pack('>H',len(name))+name.encode();i=raw.index(needle)+len(needle);n=struct.unpack('>i',raw[i:i+4])[0];return np.frombuffer(raw[i+4:i+4+n],dtype=np.uint8).reshape(96,300,300)
b=arr('Blocks');d=arr('Data'); filled=b!=0
pal={1:(115,118,125),3:(121,85,58),5:(160,133,86),18:(61,108,69),43:(165,167,167),44:(164,165,165),89:(237,207,122),95:(70,144,143),98:(114,120,128),101:(115,127,139),155:(224,224,214),159:(58,68,76),160:(132,208,67),172:(148,108,82)}
# Merge coplanar visible faces into row strips, retaining each block ID and data.
verts=[];cols=[];norms=[]
for axis in range(3):
 for sign in (-1,1):
  neighbor=np.zeros_like(filled)
  dest=[slice(None)]*3;src=dest.copy()
  dest[axis]=slice(None,-1) if sign==1 else slice(1,None)
  src[axis]=slice(1,None) if sign==1 else slice(None,-1)
  neighbor[tuple(dest)]=filled[tuple(src)]
  visible=filled & ~neighbor
  oth=[a for a in range(3) if a!=axis]
  codes=np.where(visible,b.astype(np.int32)*16+d,0).transpose(axis,*oth)
  for plane in range(codes.shape[0]):
   grid=codes[plane]
   for row in range(grid.shape[0]):
    line=grid[row];changes=np.r_[0,np.flatnonzero(line[1:]!=line[:-1])+1,len(line)]
    for start,end in zip(changes[:-1],changes[1:]):
     val=int(line[start])
     if not val:continue
     q=[]
     for aa,bb in [(row,start),(row+1,start),(row+1,end),(row,end)]:
      xyz=[0.,0.,0.];xyz[axis]=plane+(sign==1);xyz[oth[0]]=aa;xyz[oth[1]]=bb
      # source y,z,x => render x,y,z
      q.append([xyz[2]-150,xyz[0],xyz[1]-150])
     col=pal.get(val//16,(160,160,160))
     if val//16==159 and val%16==5:col=(126,183,45)
     shade={0:1 if sign==1 else .42,1:.66 if sign==1 else .8,2:.77 if sign==1 else .58}[axis]
     verts.append(q);cols.append(tuple(int(c*shade) for c in col))
     norm=[0,0,0];norm[{0:1,1:2,2:0}[axis]]=sign;norms.append(norm)
V=np.array(verts);N=np.array(norms);C=np.array(cols,dtype=np.uint8);centers=V.mean(axis=1)
print('Merged faces:',len(V),flush=True)
frames=P/'video-frames';frames.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(font,22);small=ImageFont.truetype(font,15)
for i in range(96):
 a=2*math.pi*i/96+.55; elev=math.radians(31+8*math.sin(i*2*math.pi/96))
 right=np.array([math.cos(a),0,-math.sin(a)])
 view=np.array([math.sin(a)*math.cos(elev),math.sin(elev),math.cos(a)*math.cos(elev)])
 up=np.cross(view,right)
 # Orthographic projection keeps scale comparable throughout orbit.
 flat=V.reshape(-1,3);px=(flat@right).reshape(-1,4)*2.13+640;py=-(flat@up).reshape(-1,4)*2.13+424
 depth=centers@view;inds=np.flatnonzero(N@view>.001);inds=inds[np.argsort(depth[inds])]
 im=Image.new('RGB',(1280,800),(20,27,43));dr=ImageDraw.Draw(im)
 for j in inds:
  points=list(zip(px[j],py[j]));dr.polygon(points,fill=tuple(C[j]))
 dr.rectangle((0,0,1280,67),fill=(13,19,32))
 dr.text((24,14),'ASTRO-INSPIRED FLOATING SPACEPORT',font=f,fill=(235,241,245))
 dr.text((24,43),'300 x 300 blocks | Actual schematic geometry | Minecraft 1.8.8',font=small,fill=(156,198,164))
 dr.rectangle((0,757,1280,800),fill=(13,19,32))
 dr.text((24,770),'Rendered block preview — not captured in Minecraft. Sky, lighting and glass differ in-game.',font=small,fill=(188,199,215))
 im.save(frames/f'{i:04d}.png')
 if i%24==0:print('Rendered',i+1,'/ 96',flush=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','8','-i',str(frames/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(P.parent/'Astro-Spaceport-Overview.mp4')],check=True)
# Compact animation for viewing without a video player.
images=[Image.open(frames/f'{i:04d}.png').resize((768,480)) for i in range(0,96,2)]
images[0].save(P.parent/'Astro-Spaceport-Overview.gif',save_all=True,append_images=images[1:],duration=250,loop=0)
print('MP4 and GIF complete',flush=True)
