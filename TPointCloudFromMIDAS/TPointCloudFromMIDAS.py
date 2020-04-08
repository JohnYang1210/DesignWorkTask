"""
This script extracts node position(x,y,z) in MIDAS software through .mgt file
"""
import re
import numpy as np 
with open('practical.mgt','r') as f:
	content=f.read()
pattern=re.compile(r'(\*NODE)(.*)(\*ELEMENT)',re.S)
extra=pattern.search(content).group(2)
with open('test.txt','w') as p:
	p.write(extra)
data=np.loadtxt('test.txt',delimiter=',',comments=';',skiprows=1)
datac=data[:,1:]
np.savetxt('testc.txt',datac,delimiter=',')