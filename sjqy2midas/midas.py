import re 
import pandas as pd 
import os 
from sjqy2midas import Model,MidasErr
MEDIATEFILENAME_Element='elementRawSet.csv'
MEDIATEFILENAME_Node='nodeRawSet.csv'
DOMAINNAME='domain.csv'
class Mmodel(Model):
    def __init__(self,file,dele=False,interval=0.01,r=1,writeDomainFile=True):
        filePath=os.path.split(file)
        self.path=filePath[0]
        with open(file) as f:
            self.content=f.read()
        self.GetNodeSet()
        self.GetEleSet()
        if dele:
            os.remove(self.mediateFilenameElem)
            os.remove(self.mediateFilenameNode)
        self.fullEle=self.GetFullEle()
        self.GetDomain(dele,interval,r)
        if writeDomainFile:
            with open(os.path.join(self.path,'domainFile.txt'),'w') as f:
                for i in self.domainSet:
                    p=(self.domainSet[i]).copy()        #copy() shall be called, because p.pop will influence self.domainSet[i], specifically here, pop key 'all'.
                    p.pop('all')
                    for j in p:
                        for k in p[j]:
                            f.write(str(k)+',')

    def GetNodeSet(self):
        nodeStr=re.findall(r'(?s)\*NODE    ; Nodes\n; iNO, X, Y, Z(.*)\*ELEMENT',self.content)
        self.mediateFilenameNode=os.path.join(self.path,MEDIATEFILENAME_Node)
        with open(self.mediateFilenameNode,'w') as f:
            f.write(nodeStr[0])
        self.nodeDf=pd.read_csv(self.mediateFilenameNode,engine='python',names=['node number','x','y','z'])
        self.nodeDf.set_index('node number',inplace=True)
    
    def GetEleSet(self):
        #确保赋值了材料Material才可以
       eleStr=re.findall(r'(?s)\*ELEMENT    ; Elements\n; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB,                     ; Frame  Element\n; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB, EXVAL, EXVAL2, bLMT ; Comp/Tens Truss\n; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iSUB, iWID , LCAXIS    ; Planar Element\n; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iN5, iN6, iN7, iN8     ; Solid  Element(.*)\*MATERIAL',self.content)
       self.mediateFilenameElem=os.path.join(self.path,MEDIATEFILENAME_Element)
    #    print(eleStr)
       with open(self.mediateFilenameElem,'w') as f:
            f.write(eleStr[0])
       self.elemDf=pd.read_csv(self.mediateFilenameElem,engine='python',names=['element number','type','imat','ipro','Node1','Node2','Node3','Node4','iSub','iwid'])
       self.elemDf.set_index('element number',inplace=True)
    def GetDomain(self,dele,interval,r):
        """
        获得域
        其中,Mmodel.domainDf获得.mgt文件中有关域的原始数据，整理为DataFrame类型
        Mmodel.domainSet的数据结构为如下：
        {'wallName':{'all':DataFrame.Index,'support_x_large':DataFrame.Index,'support_x_small':DataFrame.Index,'support_y_large':DataFrame.Index,'support_y_small':DataFrame.Index,'midspan':DataFrame.Index}
        ...}
        Mmdoel.domainTotalMS:所有域的支座，跨中单元的集合
        """
        if '*DOMAIN-ELEMENT' not in self.content:
            raise MidasErr('No domain defined!')
        domain=re.findall(r'(?s)\*DOMAIN-ELEMENT  ; Domain Element\n; iKEY, iTYPE, iDOMAIN, MADONAME(.*)\*MAIN-DOMAIN',self.content)
        filename=os.path.join(self.path,'domain.csv')
        with open(filename,'w') as f:
            f.write(domain[0])
        self.domainDf=pd.read_csv(filename,engine='python',names=['ikey','itype','idomain','madoname'])
        self.domainDf=self.domainDf.set_index('ikey')
        if dele:
            os.remove(filename)
        domainKeys=self.domainDf['madoname'].drop_duplicates().values
        self.domainSet={}
        for i in domainKeys:
            self.domainSet[i]={}
            self.domainSet[i]['all']=self.domainDf.loc[self.domainDf['madoname']==i].index 
            self.addMs(self.domainSet[i],interval,r)
    def addMs(self,Set,interval,r):
        """
        给domainset[i]加上支座跨中单元,DataFrame.Index
        r:midspan中板块中心的半径的平方
        """
        xyz=['x','y','z']
        xsets=self.fullEle.loc[Set['all']]['x1'].append(self.fullEle.loc[Set['all']]['x3']).drop_duplicates().sort_values().values     # 'x3' must be appended to 'x1'
        ysets=self.fullEle.loc[Set['all']]['y1'].append(self.fullEle.loc[Set['all']]['y3']).drop_duplicates().sort_values().values
        zsets=self.fullEle.loc[Set['all']]['z1'].append(self.fullEle.loc[Set['all']]['z3']).drop_duplicates().sort_values().values
        xyzSets={'x':xsets,'y':ysets,'z':zsets}
        xyzLen={len(xsets):'x',len(ysets):'y',len(zsets):'z'}
        plane=xyzLen[1]
        xyz.remove(plane)

        kSmall=xyzSets[xyz[0]][0]  # smallest coord
        kSmall2=xyzSets[xyz[0]][1]  # second smallest coord
        kLarge=xyzSets[xyz[0]][-1]  # largest coord
        kLarge2=xyzSets[xyz[0]][-2]  # second largest coord
        pSmall=xyzSets[xyz[1]][0]
        pSmall2=xyzSets[xyz[1]][1]
        pLarge=xyzSets[xyz[1]][-1]
        pLarge2=xyzSets[xyz[1]][-2]
        kChar=xyz[0]
        pChar=xyz[1]
        distance=lambda k,p:(k-(kSmall+kLarge)/2)**2+(p-(pSmall+pLarge)/2)**2
        # print(plane)   #Debug
        # print('plane',xyzSets[plane][0])
        # print(plane+'=[%s]'% xyzSets[plane][0])
        # print(xyzSets)
        # print('ksmall',kSmall)
        # print('ksmall2',kSmall2)
        # print('klarge',kLarge)
        # print('klarge2',kLarge2)

        # print('psmall',pSmall)
        # print('psmall2',pSmall2)
        # print('plarge',pLarge)
        # print('plarge2',pLarge2)
        Set['midspan']=self.SelectEle(**{plane:[xyzSets[plane][0]],'f':distance,'args':[kChar,pChar],'logic':'<','constant':r}).index
        Set['support_'+kChar+'_small']=self.SelectEle(**{plane:[xyzSets[plane][0]],kChar:[kSmall-interval,kSmall2+interval],pChar:[pSmall-interval,pLarge+interval]}).index   
        Set['support_'+kChar+'_large']=self.SelectEle(**{plane:[xyzSets[plane][0]],kChar:[kLarge2-interval,kLarge+interval],pChar:[pSmall-interval,pLarge+interval]}).index
        Set['support_'+pChar+'_small']=self.SelectEle(**{plane:[xyzSets[plane][0]],pChar:[pSmall-interval,pSmall2+interval],kChar:[kSmall-interval,kLarge+interval]}).index 
        Set['support_'+pChar+'_large']=self.SelectEle(**{plane:[xyzSets[plane][0]],pChar:[pLarge2-interval,pLarge+interval],kChar:[kSmall-interval,kLarge+interval]}).index
    



        
        
        

       







        



