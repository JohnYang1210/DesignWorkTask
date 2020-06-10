"""
This script can be used to convert 世纪旗云's .s2k file to '.mgt' file of Midas software.
"""
import re
import os
import pandas as pd 
import io
MEDIATEFILENAME_Element='elementRawSet.csv'
MEDIATEFILENAME_Node='nodeRawSet.csv'
class MidasErr(Exception):
	def __init__(self,info):
		print(info)
class Model:
	def __init__(self,file,dele=False):
		"""
		By default,dele=False,if set True,related mediate file will be deleted.
		
		"""
		filePath=os.path.split(file)
		self.path=filePath[0]
		self.filename=os.path.join(self.path,filePath[1].split('.')[0]+'.mgt')
		with open(file) as f:
			self.content=f.read()
		self.nodeSet=self.GetNodeSet()
		self.elemSet=self.GetEleSet()
		if dele:
			os.remove(self.mediateFilenameElem)
			os.remove(self.mediateFilenameNode)
		self.fullEle=self.GetFullEle()
		
	def GetNodeSet(self):
		nodeStr=re.findall(r'(?s)JOINT\s+(.*)SPRING',self.content)[0]
		pattr=re.compile(r'(?s)[X=|Y=|Z=]')
		nodeSet=re.sub(pattr,'',nodeStr)
		nodeSet=nodeSet.replace(' ',',')
		self.mediateFilenameNode=os.path.join(self.path,MEDIATEFILENAME_Node)
		with open(self.mediateFilenameNode,'w') as f:
			f.write(nodeSet)
		self.nodeDf=pd.read_csv(self.mediateFilenameNode,engine='python',names=['node num','x','y','z'])
		self.nodeDf.set_index('node num',inplace=True)
		return nodeSet

	def GetEleSet(self):
		eleStr=re.findall(r'(?s)SHELL SECTION\s+(.*)SHELL\s+(.*)LOAD',self.content)[0][1]
		pattr=re.compile(r'(?s)[J=|(SEC=SSEC)]')
		rawEleSet=re.sub(pattr,'',eleStr).replace(' ',',')
		self.mediateFilenameElem=os.path.join(self.path,MEDIATEFILENAME_Element)
		with open(self.mediateFilenameElem,'w') as f:
			f.write(rawEleSet)
		elemDf=pd.read_csv(self.mediateFilenameElem,engine='python',names=['element number','Node1','Node2','Node4','Node3','section num'])
		elemDf=elemDf
		elemDf['type']='PLATE'
		elemDf['imat']=1
		elemDf['ipro']=1
		elemDf['isub']=3
		elemDf['iwid']=0
		order=['element number','type','imat','ipro','Node1','Node2','Node3','Node4']
		elemDf=elemDf[order]
		self.elemDf=elemDf
		elemDf.set_index('element number',inplace=True) # attention here,set_index returns a new object unless inplace=True.
		elemOutputs=io.StringIO()
		elemOutputs.write(elemDf.to_csv(header=False))
		elemSet=elemOutputs.getvalue()
		elemOutputs.close()
		return elemSet
	def Gen(self):
		content='*NODE\n'+self.nodeSet+'*ELEMENT\n'+self.elemSet
		with open(self.filename,'w')  as f:
			f.write(content)
	def GetFullEle(self):
		elemDf=self.elemDf
		nodeDf=self.nodeDf
		FullEle=pd.merge(elemDf,nodeDf,left_on='Node1',right_index=True).rename(columns={'x':'x1','y':'y1','z':'z1'})
		FullEle=pd.merge(FullEle,nodeDf,left_on='Node2',right_index=True).rename(columns={'x':'x2','y':'y2','z':'z2'})
		FullEle=pd.merge(FullEle,nodeDf,left_on='Node3',right_index=True).rename(columns={'x':'x3','y':'y3','z':'z3'})
		FullEle=pd.merge(FullEle,nodeDf,left_on='Node4',right_index=True).rename(columns={'x':'x4','y':'y4','z':'z4'})
		return FullEle
	def SelectEle(self,x=None,y=None,z=None,otherCond=None):
		"""
		x=[None,4] means x<4,x=[2,4] means 2<x<4,x=[4] means x==4.only these structures above are allowed.
		and that means 'x=None,y=None,z=None' can only select rectangle-shape zone of element.
		*args is the arguments in f.
		otherCond,for example can be got through user-defined function,
		cond=np.square(self.fullEle['x1'])+np.square(self.fullEle['z1'])<16
		otherCond:list,containing all other conditions.
		for example:
			>>>model=sjqy2midas.Model(r'well.s2k',dele=True)
			>>>fullEle=model.fullEle
			>>>def distance(y,z):
    			return z**2+(y-4)**2
    		>>>cond2a1=distance(fullEle['y1'],fullEle['z1'])<9
			>>>cond2a2=distance(fullEle['y2'],fullEle['z2'])<9
			>>>cond2a3=distance(fullEle['y3'],fullEle['z3'])<9
			>>>cond2a4=distance(fullEle['y4'],fullEle['z4'])<9
			>>>cond2a=[cond2a1,cond2a2,cond2a3,cond2a4]
			>>>a=model.SelectEle(x=[0],otherCond=cond2a)
			>>>model.Press(a,-10,42,'hydropress.csv')
		"""
		cond=[]
		cond=self.DealXYZ(x,'x',cond)
		cond=self.DealXYZ(y,'y',cond)
		cond=self.DealXYZ(z,'z',cond)
		if otherCond:
			cond.extend(otherCond)
		# print(len(cond))
		if len(cond)>1:
			condSet=pd.concat(cond,axis=1)
		elif len(cond)==1:
			condSet=cond[0]
		
		return self.fullEle[condSet.all(1)]
	def DealXYZ(self,cond,alpha,collector):
		inte=[alpha+'1',alpha+'2',alpha+'3',alpha+'4']
		if cond:
			if isinstance(cond,list):
				if len(cond)==1:
					collector.append(self.fullEle[inte]==cond[0])
					print(len(collector))
				elif len(cond)==2:
					if cond[0]:                                      
						collector.append(self.fullEle[inte]>cond[0])
					if cond[1]:
						collector.append(self.fullEle[inte]<cond[1])
				# else:
				# 	raise MidasErr('Input type is wrong')
			else:
				raise MidasErr('Input type is wrong')
		return collector

	def Press(self,elemSet,f,dire,filename):
		"""
		elemSet: the selected element set,normally returned value of instance method:self.SelectEle
		f:function
		dire:荷载作用方向,'LX','LY','LZ','GX','GY','GZ'
		"""
		dic={'CMD':'HYDRO',
		'ETYP':'PLATE',
		'iFACE':'FACE',
		'DIR':dire,
		'VX':0,
		'VY':0,
		'VZ':0,
		'bPro':'NO',
		'PU':0,
		'P1':elemSet['z1'].apply(lambda x:f(x)),
		'P2':elemSet['z2'].apply(lambda x:f(x)),
		'P3':elemSet['z3'].apply(lambda x:f(x)),
		'P4':elemSet['z4'].apply(lambda x:f(x)),
		'group':' '
		}
		pressDf=pd.DataFrame(dic,index=elemSet.index)
		order=['CMD','ETYP','iFACE','DIR','VX','VY','VZ','bPro','PU','P1','P2','P3','P4','group']
		pressDf[order].to_csv(os.path.join(self.path,filename),sep=',')

if __name__=='__main__':
	inputs=input('input the .s2k file path')
	Model(inputs,dele=True).Gen()
	



		



