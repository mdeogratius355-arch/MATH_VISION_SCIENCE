from common import *
NAME='Set Theory Venn Diagram'; DESCRIPTION='Display a two-set Venn diagram with supplied region labels. No set operations are calculated.'
FIELDS=[{'name':'universal','label':'Universal set label','type':'text','default':'U'},{'name':'set_a','label':'First set label','type':'text','default':'A'},{'name':'set_b','label':'Second set label','type':'text','default':'B'},{'name':'a_only','label':'First set only (enter supplied value or elements)','type':'text','default':'A only'},{'name':'intersection','label':'Intersection (supplied value or elements)','type':'text','default':'A intersection B'},{'name':'b_only','label':'Second set only (supplied value or elements)','type':'text','default':'B only'},{'name':'outside','label':'Outside both sets','type':'text','default':'Outside'}]
def generate(v):
 c='<rect x="90" y="65" width="580" height="370" rx="18" fill="#f8fbff" stroke="#17365d" stroke-width="3"/>'+text(115,95,'Universal set '+(v['universal'] or 'U'),15,'start', 'bold')
 c+='<circle cx="315" cy="250" r="125" fill="#9cc7f0" fill-opacity=".55" stroke="#174ea6" stroke-width="3"/><circle cx="445" cy="250" r="125" fill="#f4bd78" fill-opacity=".55" stroke="#b45f06" stroke-width="3"/>'
 c+=text(265,160,v['set_a'] or 'A',18,weight='bold')+text(495,160,v['set_b'] or 'B',18,weight='bold')+text(255,260,v['a_only'],14)+text(380,260,v['intersection'],13)+text(510,260,v['b_only'],14)+text(590,390,v['outside'],13)
 d=f"Two-set Venn diagram in universal set {v['universal']}. {v['set_a']} only: {v['a_only']}. Intersection: {v['intersection']}. {v['set_b']} only: {v['b_only']}. Outside: {v['outside']}. These are displayed exactly as supplied; no union, intersection or complement is calculated."
 return svg(c,NAME,d),d
