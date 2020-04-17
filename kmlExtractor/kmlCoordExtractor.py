""""
This script is used to extract coordinates
from kml file
"""
import numpy
import numpy as np 
import pandas as pd 

import re 
import os
from io import StringIO
import sys
class KceError(Exception):
	def __init__(self,info):
		print(info)
class Kce:
	def __init__(self,file):
		self.path=os.path.split(file)[0]
		with open(file,'r',encoding='utf-8') as f:
			self.content=f.read()
			content=self.content
		self.names=[]
		while content:
			try:
				ni=re.search(r'<name>(.*)</name>\s+<Style>',content)
				self.names.append(ni.groups()[0])
				content=content[ni.end():]
			except AttributeError:
				break

		self.coordinates=re.findall(r'(?s)<coordinates>(.*?)</coordinates>',self.content)

		self.extract()
	def extract(self):
		for i in range(len(self.names)):
			co=self.coordinates[i]
			co=co.replace(' ','\n')[:-1]
			t0=np.loadtxt(StringIO(co),delimiter=',')
			df=pd.DataFrame(t0,columns=['longitude','latitude','altitude'])
			filename=os.path.join(self.path,self.names[i]+'.csv')
			df.to_csv(filename)
	def getnames(self):
		content=self.content




if __name__=='__main__':
	print('****欢迎使用kmlExtractor***')
	if len(sys.argv)==2:
		file=sys.argv[1]
	else:
		# print(sys.argv)
		file=input('输入kml文件路径及文件名:')
	Kce(file)
