from common import *
NAME='Quadratic Graph'; DESCRIPTION='Plot the quadratic expression using the coefficients entered.'
FIELDS=[{'name':'a','label':'Coefficient a','type':'number','default':'1','required':True},{'name':'b','label':'Coefficient b','type':'number','default':'0','required':True},{'name':'c','label':'Constant c','type':'number','default':'0','required':True}]
def generate(v):
 a,b,cc=[num(v[k],k) for k in ('a','b','c')]
 if a==0:raise ValueError('Coefficient a must not be zero for a quadratic graph.')
 xs=[-5+i*.2 for i in range(51)]; ys=[a*x*x+b*x+cc for x in xs]; ymin=min(0,min(ys)); ymax=max(1,max(ys))
 if ymin==ymax:ymax+=1
 c=axes('','x','y',-5,5,ymin,ymax); coords=[(80+(x+5)/10*630,420-(y-ymin)/(ymax-ymin)*365) for x,y in zip(xs,ys)]
 c+=''.join(line(*coords[i],*coords[i+1],'#1764a5',2) for i in range(len(coords)-1))
 d=f'Quadratic graph of y = {a:g}x squared + {b:g}x + {cc:g}. The coefficients entered are a={a:g}, b={b:g}, c={cc:g}. The curve is plotted; roots, turning point and other answers are not reported.'
 return svg(c,NAME,d),d
