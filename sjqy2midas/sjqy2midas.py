"""
This script can be used to convert 世纪旗云's .s2k file to '.mgt' file of Midas software.
"""
import re
import os
import pandas as pd 
import io
MEDIATEFILENAME_Element='elementRawSet.csv'
MEDIATEFILENAME_Node='nodeRawSet.csv'
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
	def gen(self):
		content='*NODE\n'+self.nodeSet+'*ELEMENT\n'+self.elemSet
		with open(self.filename,'w')  as f:
			f.write(content)
		


if __name__=='__main__':
	inputs=input('input the .s2k file path')
	Model(inputs,dele=True).gen()




		



