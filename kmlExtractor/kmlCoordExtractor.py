""""
This script is used to extract coordinates
from kml file
"""
import pandas as pd 
import numpy as np 
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
		self.names=re.findall(r'<name>(.*?)</name>',self.content)[1:]
		self.coordinates=re.findall(r'<coordinates>(.*?)</coordinates>',self.content)
		if len(self.names) !=len(self.coordinates):
			raise KceError('number of <name> is not equal to <coordinates> in file %s' % file)
		self.extract()
	def extract(self):
		for i in range(len(self.names)):
			co=self.coordinates[i]
			co=co.replace(' ','\n')[:-1]
			t0=np.loadtxt(StringIO(co),delimiter=',')
			df=pd.DataFrame(t0,columns=['longitude','latitude','altitude'])
			filename=os.path.join(self.path,self.names[i]+'.csv')
			df.to_csv(filename)

if __name__=='__main__':
	if len(sys.argv)==2:
		file=sys.argv[1]
	else:
		print(sys.argv)
		file=input('输入kml文件路径及文件名')
	Kce(file)
