import fitz
import glob
 
def rightinput(desc):
  flag=True
  while(flag):
    instr = input(desc)
    try:
      intnum = eval(instr)
      if type(intnum)==int:
        flag = False
    except:
      print('请输入正整数！')
      pass
  return intnum
 
pdffile = glob.glob("*.pdf")[0]
doc = fitz.open(pdffile)
 
flag = rightinput("输入：1：全部页面；2：选择页面\t")
if flag == 1:
  strat = 0
  totaling = doc.pageCount
else:
  strat = rightinput('输入起始页面：') - 1
  totaling = rightinput('输入结束页面：')
 
for pg in range(strat, totaling):
  page = doc[pg]
  zoom = int(100)
  rotate = int(0)
  trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
  pm = page.getPixmap(matrix=trans, alpha=False)
  pm.writePNG('pdf2png/%s.png' % str(pg+1))


  # ***********************************************************************
import glob
import fitz
import os
 
def pic2pdf():
  doc = fitz.open()
  for img in sorted(glob.glob(r"E:\设计卷册\美标\ACI350.4R/*")): # 读取图片，确保按文件名排序
    print(img)
    imgdoc = fitz.open(img)         # 打开图片
    pdfbytes = imgdoc.convertToPDF()    # 使用图片创建单页的 PDF
    imgpdf = fitz.open("pdf", pdfbytes)
    doc.insertPDF(imgpdf)          # 将当前页插入文档
  if os.path.exists("allimages.pdf"):
    os.remove("allimages.pdf")
  doc.save("allimages.pdf")          # 保存pdf文件
  doc.close()
 
if __name__ == '__main__':
  pic2pdf()