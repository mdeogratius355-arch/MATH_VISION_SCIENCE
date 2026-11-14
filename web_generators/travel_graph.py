from common import *
NAME='Travel Graph'; DESCRIPTION='Plot supplied time and distance coordinates.'
FIELDS=[{'name':'points','label':'Time and distance pairs, one per line: time, distance','type':'textarea','default':'0, 0\n1, 10\n2, 10\n3, 25','required':True}]
def generate(v):
 pts=[]
 for row in v['points'].splitlines():
  if not row.strip():continue
  p=[x.strip() for x in row.split(',')]
  if len(p)!=2:raise ValueError('Each row must contain time, distance.')
  pts.append((num(p[0],'time'),num(p[1],'distance')))
 if len(pts)<2:raise ValueError('Enter at least two time-distance pairs.')
 xmin=min(0,min(x for x,y in pts)); xmax=max(1,max(x for x,y in pts)); ymin=min(0,min(y for x,y in pts)); ymax=max(1,max(y for x,y in pts))
 if xmin==xmax:xmax+=1
 if ymin==ymax:ymax+=1
 c=axes('','Time','Distance',xmin,xmax,ymin,ymax); coords=[(80+(x-xmin)/(xmax-xmin)*630,420-(y-ymin)/(ymax-ymin)*365) for x,y in pts]
 c+=''.join(line(*coords[i],*coords[i+1],'#1764a5',3) for i in range(len(coords)-1))
 for i,((x,y),(px,py)) in enumerate(zip(pts,coords)):c+=f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#c0392b"/>'+text(px+7,py-9,f'({x:g},{y:g})',11,'start')
 d='Travel graph coordinates in entered order: '+'; '.join(f'time {x:g}, distance {y:g}' for x,y in pts)+'. Math Vision does not calculate speed or interpret journey answers.'
 return svg(c,NAME,d),d
