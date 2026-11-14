from common import *
NAME='3D Shapes and Nets'; DESCRIPTION='Display a simple schematic net for selected common solids.'
FIELDS=[{'name':'shape','label':'Shape','type':'select','options':['Cube','Cuboid','Triangular Prism','Cylinder','Square Pyramid'],'default':'Cube'},{'name':'size','label':'Side or length label','type':'text','default':'5'},{'name':'height','label':'Height label (where relevant)','type':'text','default':'8'}]
def generate(v):
 shape=v['shape']; s=v['size']; h=v['height']; c=''
 if shape=='Cube':
  for x,y in [(300,170),(380,170),(220,170),(300,90),(300,250),(300,330)]:c+=f'<rect x="{x}" y="{y}" width="80" height="80" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/>'
 elif shape=='Cuboid':
  for x,y,w,hh in [(270,180,120,70),(390,180,70,70),(150,180,120,70),(270,110,120,70),(270,250,120,70),(270,320,120,70)]:c+=f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/>'
 elif shape=='Cylinder':
  c+='<rect x="260" y="170" width="240" height="120" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><circle cx="380" cy="115" r="55" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><circle cx="380" cy="345" r="55" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/>'
 elif shape=='Triangular Prism':
  c+='<polygon points="300,150 220,290 380,290" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><rect x="300" y="150" width="180" height="140" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><polygon points="480,150 560,290 400,290" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/>'
 else:
  c+='<rect x="300" y="260" width="160" height="120" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><polygon points="300,260 380,120 460,260" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><polygon points="300,260 160,320 300,380" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><polygon points="460,260 600,320 460,380" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/><polygon points="300,380 380,490 460,380" fill="#e8f1ff" stroke="#174ea6" stroke-width="2"/>'
 c+=text(380,45,shape+' net',22,weight='bold')+text(380,475,'Entered label: '+s+'; height: '+h,14)
 d=f'Schematic net for {shape}. Supplied labels: {s} and {h}. The drawing is illustrative and does not calculate surface area, volume or missing dimensions.'
 return svg(c,NAME,d),d
