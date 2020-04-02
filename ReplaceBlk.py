"""
This script used to change Blocks in batch
"""
import sys
sys.path.append(r'F:\PycharmProject\PycomCAD')
from pycomcad import *
acad=Autocad()

print('点击源图块')
blk=acad.GetEntity()
coordOrigin=blk[0].InsertionPoint
print('点击其中一个需要修改的图块')
blkRe=acad.GetEntity()
layer=blkRe[0].Layer 
# ft=[0,8]
# fd=['AcDbBlockReference',layer]
ft=[8]
fd=[layer]
ft=VtInt(ft)
fd=VtVariant(fd)
try:
	slt=acad.GetSelectionSets('slt')
	print('选择修改区域')
	slt.SelectOnScreen(ft,fd)
	# slt.Highlight(True)
	for i in range(slt.Count):
		obj=slt.Item(i)
		coord=obj.InsertionPoint
		objNew=blk[0].Copy()
		objNew.Move(Apoint(*coordOrigin),Apoint(*coord))
		obj.Delete()
	
except:
	# print('Failed...')
	print(sys.exc_info())
finally:
	slt.Delete()