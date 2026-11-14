from common import *
NAME='Frequency Polygon'; DESCRIPTION='Plot and connect the class midpoints and frequencies entered by the learner.'
FIELDS=[{'name':'points','label':'Midpoint and frequency pairs, one per line: midpoint, frequency','type':'textarea','default':'5, 2\n15, 6\n25, 9\n35, 5\n45, 2','required':True}]
def generate(v):
 pts=[]
 for row in v['points'].splitlines():
  if not row.strip(): continue
  p=[x.strip() for x in row.split(',')]
  if len(p)!=2: raise ValueError('Each row must contain midpoint, frequency.')
  pts.append((num(p[0],'midpoint'),num(p[1],'frequency')))
 if len(pts)<2: raise ValueError('Enter at least two midpoint and frequency pairs.')
 if any(y<0 for x,y in pts): raise ValueError('Frequencies cannot be negative.')
 xmin=min(0,min(x for x,y in pts)); xmax=max(1,max(x for x,y in pts)); ymax=max(1,max(y for x,y in pts))
 if xmin==xmax:xmax+=1
 c=axes('','Class midpoint','Frequency',xmin,xmax,0,ymax)
 coords=[]
 for x,y in pts: coords.append((80+(x-xmin)/(xmax-xmin)*630,420-y/ymax*365))
 c+=''.join(line(*coords[i],*coords[i+1],'#1764a5',3) for i in range(len(coords)-1))
 for i,((x,y),(px,py)) in enumerate(zip(pts,coords)): c+=f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#c0392b"/>'+text(px,py-12,f'{x:g}, {y:g}',12)
 d='Class midpoint and frequency pairs plotted in the order entered: '+'; '.join(f'{x:g}: {y:g}' for x,y in pts)+'. Midpoints and missing frequencies are not calculated.'
 return svg(c,NAME,d),d
