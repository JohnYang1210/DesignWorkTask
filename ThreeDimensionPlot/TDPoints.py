import os,sys
os.chdir(r'F:\PycharmProject\PycomCAD')
sys.path.append(r'F:\PycharmProject\PycomCAD')
f=open('3DPointCloudYueNan.txt','w')
from pycomcad import *

acad=Autocad()
print('Connected ...')
ft=vtInt([8])
fd=vtVariant(['SRTM_Terrain_data_shp'])
slt=acad.GetSelectionSets('slt3')
slt.SelectOnScreen(ft,fd)
for i in range(slt.Count):
	if slt.Item(i).EntityName=='AcDbPolyline':
		cache=slt.Item(i).Copy()
		ele=str(cache.Elevation)
		num=len(cache.Coordinates)/2
		for j in range(int(num)):
			data=str(cache.Coordinate(j)[0])+','+str(cache.Coordinate(j)[1])+','+ele+'\n'
			f.write(data)
		cache.Delete()
	elif slt.Item(i).EntityName=='AcDb3dPolyline':
		obj=slt.Item(i)
		j=0
		while True:
			try:
				data=str(obj.Coordinate(j)[0])+','+str(obj.Coordinate(j)[1])+','+str(obj.Coordinate(j)[2])+'\n'
				f.write(data)
				j=j+1
			except:
				break
	else:
		print('Not a polyline...')

slt.Delete()
print('Done!')

