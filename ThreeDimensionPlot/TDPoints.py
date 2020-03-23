import os,sys
os.chdir(r'F:\PycharmProject\PycomCAD')
sys.path.append(r'F:\PycharmProject\PycomCAD')
f=open('3DPointCloud.txt','w')
from pycomcad import *

acad=Autocad()
print('Connected ...')
ft=vtInt([8])
fd=vtVariant(['dxt'])
slt=acad.GetSelectionSets('slt')
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
	else:
		print('Not a polyline...')

slt.Delete()
print('Done!')

