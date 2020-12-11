"""
本程序结合鸿业道路软件，快速绘制截洪沟纵剖面
"""
def drawElvationRuler(acad,scale,maxH,minH,wordHeight,intern=1):
    """
    绘制标高尺
    scale:标尺比例
    intern:m,标尺间隔
    maxH:最高,m
    """
    x,y,z=acad.GetPoint()
    n=math.floor((maxH-minH)/intern)+1
    acad.AddLwpline(x,y,x+1,y,x+1,y+n*intern*1000/scale,x,y+n*intern*1000/scale,x,y)
    texts=[str(minH+intern*i) for i in range(n)]
    for i in range(n):
        textPnt=Apoint(x-10,y+i*intern*1000/scale)  #字体距离标尺左边距离
        text=acad.AddText(texts[i],textPnt,wordHeight)
        ys=y+i*intern*1000/scale
        ye=y+(i+1)*intern*1000/scale
        if i%2==0:
            xx=x+0.75
        else:
            xx=x+0.25
        pl=acad.AddLwpline(xx,ys,xx,ye)
        pl.ConstantWidth=0.5

def sliceGroup(seq):
    """
    对list或者tuple切片为相邻端点的list集，
    如[3,5,7,8]-->[[3,5],[5,7],[7,8]]
    """
    a=[]
    count=len(seq)-1
    for i in range(count):
        j,*seq=seq
        a.append([j,seq[0]])
    return a

def doit(bgzPath,bgsPath,icdPath,)