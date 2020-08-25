import sys 
sys.path.append(r'F:\PycharmProject\PycomCAD')
from pycomcad import *
# import pythoncom,win32com
acad=Autocad()
print('当前CAD：',acad.CurrentFilename)
# print(acad.IsEarlyBind)

# acad.TurnOnEarlyBind()
digits=acad.GetReal('输入保留小数位数')
digits=int(digits)
data=[('Num','Area','Length')]
f=open('polylineInfo.txt','w')
i=1
while True:
	acad.InitializeUserInput(0,'q')
	flag=acad.GetKeyword('选择多段线:停止按q/任意键继续')
	print(flag)
	if flag=='q':
		for i in data:
			f.write('	'.join(i)+'\n')
		f.close()
		break
	try:
		entity=acad.GetEntity()
		entity=acad.Handle2Object(entity[0].Handle)
		if not entity.EntityName=='AcDbPolyline':
			acad.GetKeyword('不是多段线,按任意键忽略!')
			pass
		else:
			data.append((str(i),str(round(entity.Area,digits)),str(round(entity.Length,digits))))
			i+=1
	except:
		pass 
		
