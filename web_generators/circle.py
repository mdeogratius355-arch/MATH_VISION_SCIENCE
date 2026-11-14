from common import *
NAME='Circle'; DESCRIPTION='Draw a circle using the radius supplied by the learner.'
FIELDS=[{'name':'radius','label':'Radius','type':'number','default':'7','required':True},{'name':'label','label':'Circle label','type':'text','default':'Circle'}]
def generate(v):
 r=num(v['radius'],'radius')
 if r<=0: raise ValueError('Radius must be greater than zero.')
 rr=min(175, r*12); c=f'<circle cx="380" cy="245" r="{rr}" fill="#e8f1ff" stroke="#174ea6" stroke-width="3"/>'+line(380,245,380+rr,245,'#c62828',3)+text(380+rr/2,232,'r = '+v['radius'],15)
 c+=text(380,45,v.get('label') or 'Circle',22,weight='bold')
 d=f"A circle labelled {v.get('label') or 'Circle'}. The radius entered is {v['radius']}. No diameter, circumference or area is calculated."
 return svg(c,NAME,d),d
