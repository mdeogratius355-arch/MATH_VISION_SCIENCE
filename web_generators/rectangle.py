from common import *
NAME='Rectangle'; DESCRIPTION='Draw a rectangle using the supplied length and width.'
FIELDS=[{'name':'length','label':'Length','type':'number','default':'8','required':True},{'name':'width','label':'Width','type':'number','default':'5','required':True}]
def generate(v):
 a=num(v['length'],'length'); b=num(v['width'],'width')
 if a<=0 or b<=0:raise ValueError('Length and width must be greater than zero.')
 scale=min(420/a,250/b); w=a*scale; h=b*scale; c=f'<rect x="{380-w/2:.1f}" y="{230-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#e8f1ff" stroke="#174ea6" stroke-width="3"/>'+text(380,230-h/2-15,'Length = '+v['length'])+text(380+w/2+18,230,'Width = '+v['width'],14,'start')
 d=f'Rectangle with length {v["length"]} and width {v["width"]}. Area and perimeter are not calculated.'
 return svg(c,NAME,d),d
