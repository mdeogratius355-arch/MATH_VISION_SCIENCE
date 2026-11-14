from common import *
NAME='Bar Graph'; DESCRIPTION='Compare categories using the values entered.'
FIELDS=[{'name':'labels','label':'Category names (comma separated)','type':'text','default':'A, B, C','required':True},{'name':'values','label':'Values (comma separated)','type':'text','default':'4, 7, 5','required':True},{'name':'xlabel','label':'Horizontal axis label','type':'text','default':'Categories'},{'name':'ylabel','label':'Vertical axis label','type':'text','default':'Values'}]
def generate(v):
 labs=[x.strip() for x in v['labels'].split(',') if x.strip()]; vals=[num(x.strip(),'value') for x in v['values'].split(',') if x.strip()]
 if not labs or len(labs)!=len(vals): raise ValueError('Enter the same number of category names and values.')
 if any(x<0 for x in vals): raise ValueError('Bar graph values must not be negative.')
 mx=max(vals+[1]); c=''; n=len(vals); bw=min(65,560/n-10)
 for i,(lab,val) in enumerate(zip(labs,vals)):
  x=105+i*560/n; h=320*val/mx; c+=f'<rect x="{x:.1f}" y="{420-h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="#3977bd"/>'+text(x+bw/2,440,lab,12)+text(x+bw/2,410-h,f'{val:g}',12)
 c=axes(c,v.get('xlabel') or 'Categories',v.get('ylabel') or 'Values',0,max(1,n),0,mx)
 d='Bar graph values: '+'; '.join(f'{a}: {b:g}' for a,b in zip(labs,vals))+'. Values are displayed as entered.'
 return svg(c,NAME,d),d
