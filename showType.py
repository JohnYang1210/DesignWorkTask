"""
This script is used to test the type of  entities in AutoCAD 
"""
import sys
sys.path.append(r'F:\PycharmProject\PycomCAD')
from pycomcad import *
acad=Autocad()
print('The Current File is %s'% acad.CurrentFilename)
while True:
	test=acad.GetEntity()
	print('The type is %s'% test[0].EntityName)
	a=input('Enter anything except q to continue and q to quit...')
	if a =='q':
		break

