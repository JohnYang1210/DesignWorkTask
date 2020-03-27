"""
This script is used to auto-draw designed ditch onto cross section of terrain created through 
鸿业道路.exe
"""
import sys
sys.path.append(r'F:\PycharmProject\PycomCAD')
from pycomcad import *
acad=Autocad()
print('Current File is %s'% acad.CurrentFilename)
slt=acad.GetSelectionSets('slt4')
ft=[8]
fd=['SZ-HDM-LMX']
ft=VtInt(ft)
fd=VtVariant(fd)
slt.SelectOnScreen(ft,fd)
try:
	for i in range(slt.Count):
		obj=slt.Item(i)
		if obj.EntityName=='AcDbPolyline':
			# print(obj.Coordinate(0),obj.Coordinate(1))
			c1=obj.Coordinate(0)
			c2=obj.Coordinate(1)
			acad.AddLine(Apoint(c1[0],c1[1],0),Apoint(c1[0],c1[1]+25,0))
			acad.AddLine(Apoint(c2[0],c2[1]),Apoint(c2[0],c2[1]+25))
			copyObj=obj.Copy()
			copyObj.Move(Apoint(c1[0],c1[1],0),Apoint(c1[0],c1[1]+25,0))
			
except:
	print('Error,%s,%s,%s'%(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
finally:
	slt.Delete()
