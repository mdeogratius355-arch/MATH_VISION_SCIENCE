from common import *
NAME='Scatter Graph'; DESCRIPTION='Plot separate coordinate points without joining them or calculating a trend.'
FIELDS=[{'name':'points','label':'Coordinate pairs, one per line: x, y','type':'textarea','default':'1, 2\n2, 4\n3, 3\n4, 6','required':True},{'name':'xlabel','label':'Horizontal axis label','type':'text','default':'X'},{'name':'ylabel','label':'Vertical axis label','type':'text','default':'Y'}]
def generate(v):
 pts=[]
 for row in v['points'].splitlines():
  if not row.strip(): continue
  p=[x.strip() for x in row.split(',')]
  if len(p)!=2: raise ValueError('Each point must be entered as x, y.')
  pts.append((num(p[0],'x'),num(p[1],'y')))
 if not pts: raise ValueError('Enter at least one coordinate pair.')
 xmin=min(0,min(x for x,y in pts)); xmax=max(1,max(x for x,y in pts)); ymin=min(0,min(y for x,y in pts)); ymax=max(1,max(y for x,y in pts))
 if xmin==xmax:xmax+=1
 if ymin==ymax:ymax+=1
 c=axes('',v.get('xlabel') or 'X',v.get('ylabel') or 'Y',xmin,xmax,ymin,ymax)
 for i,(x,y) in enumerate(pts):
  px=80+(x-xmin)/(xmax-xmin)*630; py=420-(y-ymin)/(ymax-ymin)*365
  c+=f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#c0392b"/>'+text(px+12,py-10,f'P{i+1} ({x:g}, {y:g})',12,'start')
 d='Points plotted separately: '+'; '.join(f'({x:g}, {y:g})' for x,y in pts)+'. Points are not joined and no line of best fit or correlation is calculated.'
 return svg(c,NAME,d),d
