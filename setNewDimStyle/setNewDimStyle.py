import sys
sys.path.append(r'F:\PycharmProject\PycomCAD')
from pycomcad import *
def setDimStyle(acad,name,factor):
	table={'dimclrd':62,'dimdlI':0,'dimclre':62,
	   'dimexe':2,'dimexo':3,
	   'dimfxlon':1,
	   'dimfxl':3,'dimblk1':'_archtick',
	   'dimldrblk':'_dot',
	   'dimcen':2.5,'dimclrt':62,'dimtxt':3,'dimtix':1,
	   'dimdsep':'.','dimlfac':50}
	table['dimlfac']=int(factor)
	for i in table:
		acad.SetVariable(i,table[i])
	dim=acad.CreateDimStyle(name)
	dim.CopyFrom(acad.DimStyle0)
	acad.ActivateDimStyle(name)
acad=Autocad()
if acad.IsEarlyBind:
	print('Mode is early bind')
else:
	print('Mode is not early bind')
	acad.TurnOnEarlyBind()
print('Current file:%s'% acad.CurrentFilename)
name=input('input dim style name')
factor=input('input dim style factor')
setDimStyle(acad,name,factor)
print('Done!')