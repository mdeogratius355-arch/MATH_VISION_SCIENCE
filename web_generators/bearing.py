from common import *
NAME='Bearing Diagram'; DESCRIPTION='Show destinations at bearings measured clockwise from north.'
FIELDS=[{'name':'origin','label':'Starting point','type':'text','default':'O'},{'name':'destinations','label':'Destinations and bearings, one per line: Name, degrees','type':'textarea','default':'Town A, 45\nTown B, 135\nTown C, 270','required':True}]
def generate(v):
 rows=[]
 for line0 in v['destinations'].splitlines():
  if not line0.strip(): continue
  p=[x.strip() for x in line0.split(',')]
  if len(p)!=2: raise ValueError('Each destination line must contain a name, a comma and a bearing.')
  a=num(p[1],'bearing')
  if not 0<=a<=360: raise ValueError('Bearings must be between 0 and 360 degrees.')
  rows.append((p[0],a,p[1]))
 if not rows: raise ValueError('Enter at least one destination.')
 c=line(380,440,380,65)+text(380,48,'N',18,weight='bold')+text(380,265,v['origin'] or 'O',16,weight='bold')
 for name,a,raw in rows:
  r=175; rad=math.radians(a); x=380+r*math.sin(rad); y=265-r*math.cos(rad)
  c+=line(380,265,x,y,'#1764a5',3)+text(x,y-10,name+' '+raw+'°',13)
 d='Starting point '+(v['origin'] or 'O')+'. North is upwards and bearings are measured clockwise from north. '+ ' '.join(f'{n} is shown at {raw} degrees.' for n,a,raw in rows)+' No reverse bearings or distances are calculated.'
 return svg(c,NAME,d),d
