"""
本程序结合鸿业道路软件，快速绘制截洪沟纵剖面
----------------------------------------
输入文件说明：
（1）.bgs是设计标高文件，需要将其后缀名改为.txt，方便Numpy读入，每行有3个数据，（默认）以空格为分割，分别为距离，高程，0
(2).bgz是自然标高文件，需要将其后缀名改为.txt，方便Numpy读入，每行有2个数据，（默认）以空格为分割，分别为距离，高程
（3）.icd是平曲线积木格式数据，需要将其后缀名改为.txt，且仅含表示距离的数据,（默认）以','为分割
ICD文件格式：

| 格式                   | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| StartZH                | 起点桩号                                                     |
| X,Y,Angle              | 起点坐标和方位角                                             |
| 1、Length,[EndAngle]   | 1:直线标示符，长度，后续单元起始方位角（可选）               |
| 2，R,Length,1/-1       | 2:圆曲线标示符，半径，长度，转向（1：右转；-1：左转）        |
| 3，A,EndR,1/-1         | 3:完整缓和曲线（R在无穷大~R0时）标识符，回旋参数，终点半径，转向（1：右转；-1：左转） |
| 4，A,StartR,1/-1       | 4:完整缓和曲线（R在R0~无穷大时）标识符，回旋参数，起点半径，转向（1：右转；-1：左转） |
| 5，A,StartR EndR,1/-1  | 5：不完整缓和曲线（R在(R大-R 小)时）标识符，回旋参数起点半径，终点半径，转向（1：右转；-1：左转） |
| 6，A ,StartR EndR,1/-1 | 6：不完整缓和曲线（R在(R大-R 小)时）标识符，回旋参数起点半径，终点半径，转向（1：右转；-1：左转） |
| 0 0 0                  | 结束符                                                       |

"""
import sys
import math
import numpy as np
import pandas as pd
sys.path.append(r'E:\programming\pycomcad\PycomCAD')
from pycomcad import * 

def drawElevationRuler(acad,x,y,scale,maxH,minH,wordHeight,intern=1):
    """
    绘制标高尺
    x,y:标尺最低点的坐标
    scale:标尺比例
    intern:m,标尺间隔
    maxH:最高,m
    """
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

def addColumn(acad,pnt,row,Height,Length,text,stylename,column=1,wordHeight=3):
    """
    绘制下方表格的表头
    pnt:表头的左上角的坐标点
    row:表格的行数
    Height:单元格高度
    Length:单元格长度
    text:列表，表格中每个单元格的内容
    stylename:表头字体的字体样式名称
    column:表格的列数，默认为1
    wordHeight:字体高度
    """
    x,y,z=pnt
    acad.AddTable(Apoint(*pnt),row,column,Height,Length)
    
    for t in text:
        word=acad.AddText(t,Apoint(x,y-10*(text.index(t)+1)),wordHeight)
        word.StyleName=stylename

def doit(acad,pnt,bgsPath,bgzPath,pqxPath,xScale,yScale,row=7,cellHeight=11,cellLength=35,wordHeight=2.5,digit=2,ZH=False):
    """
    绘制截洪沟剖面图
    pnt:插入点的坐标（该插入点实际是表格最左上角的坐标点）
    bgsPath:设计标高文件路径，.txt
    bgzPath:自然地面标高文件路径，.txt
    pqxPath:平曲线文件路径，.txt
    xScale:水平向比例，如200
    yScale:竖直向比例，如200
    row:表头行数
    cellHeight:表头单元格高度
    cellLength:表头单元格长度
    wordHeight:文字高度
    digit:表格中数字小数的位数，默认为2位小数
    ZH:是否计算/绘制各桩号处的地面标高，设计标高等，默认为False
    """
    ####数据准备-----------------------------------------------------
    x,y,z=pnt #插入点的坐标
    bgs=np.loadtxt(bgsPath) #读入设计标高文件
    if bgs.shape[-1]==3:
        bgs=bgs[:,:2] #只要x,height信息
    bgz=np.loadtxt(bgzPath) #读入自然地面标高
    if bgz.shape[-1]==3:
        bgz=bgz[:,:2]
    yMin=np.vstack((bgs,bgz)).min(axis=0)[1] #插入点所代表的高程，即设计标高与自然地面标高中的最小值
    yMax=np.vstack((bgs,bgz)).max(axis=0)[1]# 标尺需要标注的最大标高
    pqx=np.loadtxt(pqxPath,delimiter=',') #读入平曲线文件
    if pqx.ndim==2:
        pqx=pqx[:,1]       #得到平曲线的原始分段长度值
    pqxData=np.cumsum(pqx) #得到平曲线的累计值

    scaleArray=np.array([1000/xScale,1000/yScale]) #缩放比例数组

    ####绘制表头---------------------------------------------------------
    tableText=['转点编号/桩号','平面距离（m）','自然地面标高',
         '沟顶标高(m)','设计沟内底标高（m）','坡度（%）','沟道型式及尺寸']
    addColumn(acad,pnt,row,cellHeight,cellLength,tableText,'WLZ')

    ####绘制设计线，地面线---------------------------------------------------
    bgsL=np.array([x+cellLength,y])+(bgs-np.array([0,yMin]))*scaleArray #设计线各点的cad坐标
    acad.AddLwpline(*bgsL.flatten().tolist()) #绘制设计线
    bgzL=np.array([x+cellLength,y])+(bgz-np.array([0,yMin]))*scaleArray
    acad.AddLwpline(*bgzL.flatten().tolist()) # 绘制地面线

    ####绘制表格水平线
    firstHorizonLine=acad.AddLine(Apoint(x+cellLength,y),Apoint(x+cellLength+bgs.max(axis=0)[0]*scaleArray[0],y))
    for i in range(row):
        firstHorizonLine.Offset(-cellHeight*(i+1))

    ##### 计算各个特征点（平曲线转折点，竖向线转折点，桩号点）--------------------
    distance=bgs[:,0].tolist()+pqxData.tolist()
    if ZH:
        distance+=bgz[:,0].tolist()
    df=pd.DataFrame({'Distance':distance,
    'BGZ':np.interp(distance,bgz[:,0],bgz[:,1]),
    'BGS':np.interp(distance,bgs[:,0],bgs[:,1])})  #df是记录各个特征点处的桩号，地面标高，设计标高信息的DataFrame

    #### 绘制各个特征点处的竖直线，以及填写相应的高程-----------------------------
    firstVerticalLine=acad.AddLine(Apoint(x+cellLength,y),Apoint(x+cellLength,y-row*cellHeight)) #第一根竖直线，即从桩号K0+000开始的竖直线
    for i in range(df.index.argmax()+1):
        dis,BGZ,BGS=df.iloc[i].values
        firstVerticalLine.Offset(dis*scaleArray[0])
        zhuanghao=acad.AddText('+'+str(round(dis,digit)),Apoint(x+cellLength+dis*scaleArray[0],y-cellHeight/2),wordHeight)
        ziranbiaogao=acad.AddText(str(round(BGZ,digit)),Apoint(x+cellLength+dis*scaleArray[0],y-cellHeight*3),wordHeight)
        shejibiaogao=acad.AddText(str(round(BGS,digit)),Apoint(x+cellLength+dis*scaleArray[0],y-5*cellHeight),wordHeight)
        zhuanghao.Rotation=math.radians(90)
        ziranbiaogao.Rotation=math.radians(90)
        shejibiaogao.Rotation=math.radians(90)
    
    #### 绘制标尺
    floatYmin=yMin-int(yMin)
    drawElevationRuler(acad,x-5,y-floatYmin*scaleArray[-1],yScale,int(yMax)+1,int(yMin),wordHeight)

    #### 绘制比例示意图
    startPnt=Apoint(x+cellLength,y+cellLength)
    endPnt=Apoint(x+2*cellLength,y+cellLength)
    L1=acad.AddLine(startPnt,endPnt)
    L2=acad.AddLine(endPnt,Apoint(x+2*cellLength-0.5*3**0.5*wordHeight,y+cellLength-0.5*wordHeight))
    L3=L2.Mirror(startPnt,endPnt)
    L1.Copy()
    L2.Copy()
    L3.Copy()
    L1.Rotate(startPnt,math.radians(90))
    L2.Rotate(startPnt,math.radians(90))
    L3.Rotate(startPnt,math.radians(90))
    hText=acad.AddText(str(xScale),Apoint(x+1.5*cellLength,y+cellLength),wordHeight)
    vText=acad.AddText(str(yScale),Apoint(x+cellLength,y+1.5*cellLength),wordHeight)
    vText.Rotation=math.radians(90)
if __name__=='__main__':
    acad=Autocad()
    pnt=acad.GetPoint()
    doit(acad,pnt,r'E:\programming\pyprogram\jhgDraw\bgs.txt',r'E:\programming\pyprogram\jhgDraw\bgz.txt',
    r'E:\programming\pyprogram\jhgDraw\pm.txt',300,300,ZH=True)









