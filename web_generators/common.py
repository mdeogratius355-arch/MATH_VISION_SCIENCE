import html, math
W,H=760,500

def esc(x): return html.escape(str(x),quote=True)
def svg(content,title='Math Vision diagram',desc=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {W} {H}" width="100%" height="auto"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc><rect width="100%" height="100%" fill="white"/>{content}</svg>'
def text(x,y,t,size=16,anchor='middle',weight='normal'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="#172b4d">{esc(t)}</text>'
def line(x1,y1,x2,y2,stroke='#17365d',width=2,dash=''):
    extra=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"{extra}/>'
def num(v,label='value'):
    try: x=float(v)
    except: raise ValueError(f'Enter a valid number for {label}.')
    if not math.isfinite(x): raise ValueError(f'{label} must be a finite number.')
    return x
def esc_text(x,y,t,size=14): return text(x,y,t,size)
def axes(content,xlabel='X',ylabel='Y',xmin=0,xmax=10,ymin=0,ymax=10):
    left,bottom,top,right=80,420,55,710
    content += line(left,top,left,bottom)+line(left,bottom,right,bottom)
    for i in range(6):
        x=left+(right-left)*i/5; val=xmin+(xmax-xmin)*i/5
        content+=line(x,bottom,x,bottom+5)+text(x,bottom+24,f'{val:g}',11)
        y=bottom-(bottom-top)*i/5; v=ymin+(ymax-ymin)*i/5
        content+=line(left-5,y,left,y)+text(left-12,y+4,f'{v:g}',11,'end')
        if i: content+=line(left,y,right,y,'#e2e8f0',1)
    content+=text((left+right)/2,475,xlabel,14)+text(22,(top+bottom)/2,ylabel,14)
    return content
