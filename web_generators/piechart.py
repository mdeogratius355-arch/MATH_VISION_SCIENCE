from common import *
NAME='Pie Chart'; DESCRIPTION='Display categories and their supplied values as labelled sectors.'
FIELDS=[{'name':'labels','label':'Category names (comma separated)','type':'text','default':'Science, Mathematics, English','required':True},{'name':'values','label':'Corresponding values (comma separated)','type':'text','default':'40, 35, 25','required':True}]
def generate(v):
 labels=[x.strip() for x in v['labels'].split(',') if x.strip()]; vals=[num(x.strip(),'category value') for x in v['values'].split(',') if x.strip()]
 if len(labels)<2 or len(labels)!=len(vals): raise ValueError('Enter at least two category names and the same number of values.')
 if any(x<0 for x in vals) or sum(vals)<=0: raise ValueError('Values must be zero or greater, with at least one positive value.')
 total=sum(vals); angle=-90; c=''; colors=['#2457a7','#e07a24','#2e8b57','#9b59b6','#c0392b','#16a085']
 for i,(lab,val) in enumerate(zip(labels,vals)):
  if val==0: continue
  end=angle+360*val/total; rad=math.pi/180
  x1=380+150*math.cos(angle*rad); y1=250+150*math.sin(angle*rad); x2=380+150*math.cos(end*rad); y2=250+150*math.sin(end*rad)
  large=1 if end-angle>180 else 0
  c+=f'<path d="M 380 250 L {x1:.2f} {y1:.2f} A 150 150 0 {large} 1 {x2:.2f} {y2:.2f} Z" fill="{colors[i%len(colors)]}" stroke="white" stroke-width="2"/>'
  mid=(angle+end)/2*rad; lx=380+190*math.cos(mid); ly=250+190*math.sin(mid)
  c+=text(lx,ly,f'{lab}: {val:g}',13)
  angle=end
 d='Pie chart categories and values in the order supplied: '+ '; '.join(f'{a}: {b:g}' for a,b in zip(labels,vals))+'. The chart does not calculate percentages or report mathematical answers.'
 return svg(c,NAME,d),d
