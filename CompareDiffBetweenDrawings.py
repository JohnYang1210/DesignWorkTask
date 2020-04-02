"""
This script is used to check differences between 2 dwg files
"""
import sys
sys.path.append(r'F:\PycharmProject\PycomCAD')
from pycomcad import *
def CollectEntity(blk):
	"""
	collect the information of entities in blk into a dictionary locally called collectDict.
	The data structure of collectDict is as the following:
	collectDict={
	'AcDbText':[(InsertionPoint,TextString)],
	'AcDbMText':[(InsertionPoint,TextString)],
	'AcDbCircle':[(Center,Radius)],
	'AcDbArc':[(Center,Radius,StartAngle,EndAngle)],
	'AcDbPoint':[Coordinates],
	'AcDb2dPolyline':[Coordinates],
	'AcDbPolyline':[Coordinates],
	'AcDbLine':[(StartPoint,EndPoint)],
	'AcDbRotatedDimension':[(TextPosition,Measurement)],
	'AcDbAlignedDimension':[(ExtLine1Point,ExtLine2Point,TextPosition,Measurement)],
	'AcDbRadialDimension':[(TextPosition,Measurement)],
	'AcDb2LineAngularDimension':[(TextPosition,Measurement)],
	'AcDbDiametricDimension':[(TextPosition,Measurement)],
	'AcDbBlockReference':[(InsertionPoint,Name)],
	'AcDbRasterImage':[(Origin,Name,Height,Width)]


	}
	"""
	collectDict={}
	for i in range(blk.Count):
		obj=blk.Item(i)
		objName=obj.EntityName
		if objName in collectDict:
			AddObject(collectDict,obj)
		else:
			collectDict[objName]=[]
			AddObject(collectDict,obj)
	return collectDict
def AddObject(collectDict,obj):
	if obj.EntityName in('AcDbText','AcDbMText'):
		data=(obj.InsertionPoint,obj.TextString)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName=='AcDbCircle':
		data=(obj.Center,obj.Radius)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName=='AcDbArc':
		data=(obj.Center,obj.Radius,obj.StartAngle,obj.EndAngle)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName in ('AcDbPoint','AcDbPolyline','AcDb2dPolyline'):
		data=obj.Coordinates
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName=='AcDbLine':
		data=(obj.StartPoint,obj.EndPoint)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName in ('AcDbRotatedDimension','AcDbRadialDimension','AcDb2LineAngularDimension','AcDbDiametricDimension'):
		data=(obj.TextPosition,obj.Measurement)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName=='AcDbAlignedDimension':
		data=(obj.ExtLine1Point,obj.ExtLine2Point,obj.TextPosition,obj.Measurement)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName=='AcDbBlockReference':
		data=(obj.InsertionPoint,obj.Name)
		collectDict[obj.EntityName].append(data)
	elif obj.EntityName=='AcDbRasterImage':
		data=(obj.Origin,obj.Name,obj.Height,obj.Width)
		collectDict[obj.EntityName].append(data)
	else:
		pass
def AddAnnotation(acad,dict1,dict2,radius):
	for ele in dict1:
		a=set(dict1[ele])-set(dict2[ele])
		print(a,'')
		print(ele)
		if a:
			if ele not in ('AcDbPoint','AcDb2dPolyline','AcDbPolyline') :
				for data in a:
					coord=data[0]
					acad.AddCircle(Apoint(*coord),radius)
			else:
				for data in a:
					acad.AddCircle(Apoint(data[0],data[1],0),radius)



if __name__=='__main__':
	acad=Autocad()
	acad.OpenFile(r'C:\Users\QQ\Desktop\Drawing2.dwg')
	print(acad.CurrentFilename)
	blk=acad.acad.ActiveDocument.ModelSpace
	test1=CollectEntity(blk)
	print('test1 done!')
	# print(test1['AcDbPolyline'])
	acad.OpenFile(r'C:\Users\QQ\Desktop\Drawing2 - 副本.dwg')
	blk1=acad.acad.ActiveDocument.ModelSpace
	
	test2=CollectEntity(blk1)
	# print(test2['AcDbPolyline'])
	# for i in test1:
	# 	a=set(test1[i])-set(test2[i])
	# 	if a:
	# 		print(i)
	# 		print(a)
	# 		for k in a:
	# 			acad.AddCircle(Apoint(*k[0]),10)
	print('test2 done!')
	AddAnnotation(acad,test1,test2,5)
