from common import *
NAME='Triangle'; DESCRIPTION='Draw a triangle using three entered side labels as a schematic diagram.'
FIELDS=[{'name':'a','label':'Side A label','type':'text','default':'5'},{'name':'b','label':'Side B label','type':'text','default':'6'},{'name':'c','label':'Side C label','type':'text','default':'7'}]
def generate(v):
 c='<polygon points="180,390 580,390 390,100" fill="#e8f1ff" stroke="#174ea6" stroke-width="3"/>'+text(380,420,'Side A: '+v['a'])+text(150,245,'Side B: '+v['b'])+text(510,245,'Side C: '+v['c'])
 d=f'Triangle diagram with side labels A {v["a"]}, B {v["b"]}, and C {v["c"]}. The drawing is schematic and does not calculate angles, area or missing sides.'
 return svg(c,NAME,d),d
