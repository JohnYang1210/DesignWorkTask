"""
This script is used to check differences between 2 dwg files
"""
import sys
sys.path.append(r'G:\PycharmProject\PycomCAD\PycomCAD')
from pycomcad import *
import win32com
def CollectEntity(blk):
	"""
	collect the information of entities in blk into a dictionary locally called collectDict.
	The data structure of collectDict is as the following:
	collectDict={
	'AcDbText':{(InsertionPoint,TextString)},
	'AcDbMText':{(InsertionPoint,TextString)},
	'AcDbCircle':{(Center,Radius)},
	'AcDbArc':{(Center,Radius,StartAngle,EndAngle)},
	'AcDbPoint':{Coordinates},
	'AcDb2dPolyline':{Coordinates},
	'AcDbPolyline':{Coordinates},
	'AcDbLine':{(StartPoint,EndPoint)},
	'AcDbRotatedDimension':{(TextPosition,Measurement)},
	'AcDbAlignedDimension':{(ExtLine1Point,ExtLine2Point,TextPosition,Measurement)},
	'AcDbRadialDimension':{(TextPosition,Measurement)},
	'AcDb2LineAngularDimension':{(TextPosition,Measurement)},
	'AcDbDiametricDimension':{(TextPosition,Measurement)},
	'AcDbBlockReference':{(InsertionPoint,Name)},
	'AcDbRasterImage':{(Origin,Name,Height,Width)}
	}
	"""
	collectDict={}
	for i in range(blk.Count):
		obj=blk.Item(i)
		obj=obj.Copy()
		objName=obj.EntityName
		if objName in collectDict:
			AddObject(collectDict,obj)
			obj.Delete()
		else:
			collectDict[objName]=set()
			print(collectDict)
			AddObject(collectDict,obj)
			obj.Delete()
	return collectDict
def AddObject(collectDict,obj):
	if obj.EntityName in('AcDbText','AcDbMText'):
		data=(obj.InsertionPoint,obj.TextString)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName=='AcDbCircle':
		data=(obj.Center,obj.Radius)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName=='AcDbArc':
		data=(obj.Center,obj.Radius,obj.StartAngle,obj.EndAngle)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName in ('AcDbPoint','AcDbPolyline','AcDb2dPolyline'):
		data=obj.Coordinates
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName=='AcDbLine':
		data=(obj.StartPoint,obj.EndPoint)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName in ('AcDbRotatedDimension','AcDbRadialDimension','AcDb2LineAngularDimension','AcDbDiametricDimension'):
		if obj.TextOverride:
			measure=obj.TextOverride
		else:
			measure=obj.Measurement
		data=(obj.TextPosition,measure)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName=='AcDbAlignedDimension':
		data=(obj.ExtLine1Point,obj.ExtLine2Point,obj.TextPosition,obj.Measurement)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName=='AcDbBlockReference':
		data=(obj.InsertionPoint,obj.Name)
		collectDict[obj.EntityName].add(data)
	elif obj.EntityName=='AcDbRasterImage':
		data=(obj.Origin,obj.Name,obj.Height,obj.Width)
		collectDict[obj.EntityName].add(data)
	else:
		pass

def FindDiff(dict1,dict2):
	"""
	dict1-dict2
	"""
	diff={}
	for i in dict1:
		if i in dict2.keys():
			diff[i]=dict1[i]-dict2[i]
		else:
			diff[i]=dict1[i]
	return diff 
def AddAnnotation(acad,diff,layername,anno_prefix,radius,height):
	if layername in acad.LayerNames:
		acad.GetLayer(layername).Delete
	layer=acad.CreateLayer(layername)
	layer.color=win32com.client.constants.acRed 
	acad.ActivateLayer(layername)
	for i in diff:
		eleSet=diff[i]
		for ele in eleSet:
			if i not in ('AcDbPoint','AcDb2dPolyline','AcDbPolyline'):
				coord=ele[0]
			else:
				coord=(ele[0],ele[1],0)
			acad.AddCircle(Apoint(*coord),radius)
			acad.AddText(anno_prefix+i[4:],Apoint(*coord),height)



if __name__=='__main__':

	acad=Autocad()
	acad.ActivateFile('test1.dwg')
	blk1=acad.acad.ActiveDocument.ModelSpace
	test1=CollectEntity(blk1)
	print('test1 done')
	acad.ActivateFile('test2.dwg')
	blk2=acad.acad.ActiveDocument.ModelSpace
	test2=CollectEntity(blk2)
	print('test2 done')
	diff1=FindDiff(test2,test1)
	AddAnnotation(acad,diff1,'pycom_layer_addChange','+',10,3)
	diff2=FindDiff(test1,test2)
	AddAnnotation(acad,diff2,'pycom_layer_delete','-',10,3)
