from common import *
NAME='Histogram'; DESCRIPTION='Draw adjacent bars from the class intervals and frequencies entered.'
FIELDS=[{'name':'classes','label':'Class interval and frequency, one per line: lower, upper, frequency','type':'textarea','default':'0, 10, 4\n10, 20, 8\n20, 30, 6','required':True}]
def generate(v):
 rows=[]
 for row in v['classes'].splitlines():
  if not row.strip():continue
  p=[x.strip() for x in row.split(',')]
  if len(p)!=3: raise ValueError('Each row must contain lower boundary, upper boundary, frequency.')
  a,b,f=[num(x,'class value') for x in p]
  if b<=a or f<0: raise ValueError('Upper boundary must exceed lower boundary; frequency cannot be negative.')
  rows.append((a,b,f))
 if not rows:raise ValueError('Enter at least one class interval.')
 lo=min(a for a,b,f in rows); hi=max(b for a,b,f in rows); mf=max(1,max(f for a,b,f in rows)); c=axes('','Class interval','Frequency',lo,hi,0,mf)
 for a,b,f in rows:
  x=80+(a-lo)/(hi-lo)*630; w=(b-a)/(hi-lo)*630; h=f/mf*365
  c+=f'<rect x="{x:.1f}" y="{420-h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#75a9d8" stroke="#17365d" stroke-width="2"/>'+text(x+w/2,440,f'{a:g}-{b:g}',11)+text(x+w/2,410-h,f'{f:g}',12)
 d='Histogram classes: '+'; '.join(f'{a:g} to {b:g}: frequency {f:g}' for a,b,f in rows)+'. The entered frequencies are displayed; no missing frequency or statistical measure is calculated.'
 return svg(c,NAME,d),d
