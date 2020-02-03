from tkinter import *
import matplotlib.pyplot as plt
from tkinter.filedialog import *
from tkinter import messagebox
import operator
from tkinter.ttk import Progressbar


def brows():
    fileName.delete(0,END)
    #output.delete(0.0,END)
    filename=askopenfilename(filetypes=(("Index files",".txt"),("All files",".*")))
    fileName.insert(END,filename)

def saveTxt():
    global sf
    saveFile.delete(0,END)
    files = [("Text files",".txt"),("Comma separated",".csv")]
    sf=asksaveasfile(mode="w" ,filetypes = files, defaultextension=files)
    saveFile.insert(END,sf.name)
    return sf


def exit():
	window.destroy()

def upperLeftConner(xlist,ylist):
	xUpperLeftConner = min(xlist)
	yUpperLeftConner = max(ylist)
	return [xUpperLeftConner, yUpperLeftConner]

def lowerRightConner(xlist,ylist):
	xlowerRightConner = max(xlist)
	ylowerRightConner = min(ylist)
	return [xlowerRightConner, ylowerRightConner]

def box(ulc,lrc):
	plt.plot([ulc[0],lrc[0],lrc[0],lrc[0],ulc[0],ulc[0]],[ulc[1],ulc[1],lrc[1],lrc[1],lrc[1],ulc[1]])
	#plt.show()

def sampleBox(ulc,dist):
	x = ulc[0]+dist[0]
	y = ulc[1]-dist[1]

	if var3.get()==1:
		plt.plot([ulc[0],x,x,x,ulc[0],ulc[0]],[ulc[1],ulc[1],y,y,y,ulc[1]], color='black')
	#plt.show()
	return[x,y,dist]

def process():

	if var3.get()==1:
		plt.ion()

	try:
		fil = fileName.get()

		with open(fil, "r") as file:
			file = file.readlines()

		ln = float(length.get())
		w = float(width.get())

	except:
		messagebox.showinfo("Error", "The file path is not valid, Enter a valid file path or check the parameters in entry")

	x=[]
	y=[]
	z=[]
	for i in file:
		x.append(float(i.split()[0]))
		y.append(float(i.split()[1]))
		z.append(float(i.split()[2]))

	ulc = upperLeftConner(x,y)
	lrc = lowerRightConner(x,y)
	bb  = sampleBox(ulc,[ln,w])

	if var3.get()==1:
		plt.scatter(x,y, marker='x', color='r')
		plt.xlabel("East/Longitude (m)")
		plt.xlabel("Nord/Latitude  (m)")
		plt.title("Point Clouds")

	i = (((lrc[0]-ulc[0])>0) & ((lrc[1]-ulc[1])<0))

	#print(i)

	varProg.set(10)
	window.update_idletasks()

	rslt3 = []
	rslt1 = []
	k= 0
	l= 0
	
	while i:

		
		for j in zip(x,y,z):
			if (j[0]>=ulc[0]) & (j[1]<=ulc[1]):
				if (j[0]<=bb[0]) & (j[1]>=bb[1]):
					rslt1.append(j)

		#print(rslt1)
		if len(rslt1)>0:
			rslt1.sort(key=operator.itemgetter(2))
			rslt3.append(rslt1[0])
			rslt3.append(rslt1[-1])
		jx = [k[0] for k in rslt3]
		jy = [k[1] for k in rslt3]

		rslt1[:] = []

		plt.pause(0.0001)

		if (lrc[0]-bb[0])>0:
			bb  = sampleBox((bb[0],ulc[1]),(ln,w)) 
			dst = bb[2]
			ulc[0] = ulc[0]+dst[0]
			k += 1
		
		elif (lrc[1]-ulc[1])<0:
			l += 1
			bb = []
			ulc[1] = ulc[1] - dst[0]
			ulc[0] = ulc[0] - k*dst[0]
			bb  = sampleBox((ulc[0],ulc[1]),(ln,w))
			k=0
			
			i = (((lrc[0]-ulc[0])>0) & ((lrc[1]-ulc[1])<0))
			

	varProg.set(80)
	window.update_idletasks()

	# print(rslt1)
	print(i)
	print(rslt3)
	ix = [k[0] for k in rslt1]
	iy = [k[1] for k in rslt1]
	jx = [l[0] for l in rslt3]
	jy = [l[1] for l in rslt3]
	jz = [l[2] for l in rslt3]

	#data = [jx,jy,jz]
	#print(data)

	with open(saveFile.get(), "w") as ff:
		ff.write("x"+","+"y"+","+"z"+"\n")
		j=0
		for i in rslt3:
			j+=1
			if (var1.get()==1) & (var2.get()==1):
				ff.write(str(i[0])+","+str(i[1])+","+str(i[2])+"\n")
				#print(1)
			elif (var1.get()==1) & (var2.get()==0):
				if j%2 ==1:
					ff.write(str(i[0])+","+str(i[1])+","+str(i[2])+"\n")
					#print(2)
			elif (var1.get()==0) & (var2.get()==1):
				if j%2==0:
					ff.write(str(i[0])+","+str(i[1])+","+str(i[2])+"\n")
					#print(3)
			else:
				pass
				#print(4)
				#print(var2,var1)
	varProg.set(100)
	window.update_idletasks()

	if var3.get():
		plt.pause(0.0001)
		plt.scatter(ix,iy, color="blue", marker="x")
		plt.pause(0.0001)
		plt.scatter(jx,jy, color="green", marker="o", s=100, alpha=0.3)
		plt.pause(1)

	messagebox.showinfo("Processing", "Processing completed sucessfully!")
	varProg.set(0)


window = Tk()
window.geometry("750x400")
window.title("Cloudy")
window.iconbitmap('logo_Clear_Survey.ico')


window1=Frame(window)
window1.pack()

Label(window1).grid(row=0,column=0,sticky=W)
Label(window1, text="Import file").grid(row=1,column=0,sticky=W)

fileName=Entry(window1, width=90, bg="white")
fileName.grid(row=1,column=1,sticky=W)

Button(window1, text="...",width=12, command=brows, cursor="heart").grid(row=1,column=2,sticky=W)

Label(window1).grid(row=2,column=0,sticky=W)
Label(window1, text="Sampling box ").grid(row=3,column=0,sticky=W)
Label(window1, text="length (m)").grid(row=4,column=0,sticky=W)
Label(window1, text="width (m)").grid(row=5,column=0,sticky=W)

length=Entry(window1, width=10, bg="white")
length.grid(row=4,column=1,sticky=W)

width=Entry(window1, width=10, bg="white")
width.grid(row=5,column=1,sticky=W)

Label(window1, text="Output Points").grid(row=3,column=2,sticky=W)
var1 = IntVar()
Checkbutton(window1, text="Min Alt", variable=var1).grid(row=4, column = 2, sticky=W)
var2 = IntVar()
Checkbutton(window1, text="Max Alt", variable=var2).grid(row=5, column = 2, sticky=W)

Label(window1, text="Plot Processig").grid(row=6,column=0,sticky=W)
var3 = IntVar()
Checkbutton(window1, text="", variable=var3).grid(row=6, column = 1, sticky=W)

Label(window1).grid(row=7,column=0,sticky=W)
Label(window1, text="Save file").grid(row=8,column=0,sticky=W)

saveFile = Entry(window1, width=90, bg="white")
saveFile.grid(row=8,column=1,sticky=W)

Button(window1, text="...",width=12, command=saveTxt, cursor="heart").grid(row=8,column=2,sticky=W)

Label(window1).grid(row=9,column=0,sticky=W)
Button(window1, text="Process",width=12, command=process, cursor="heart").grid(row=10,column=0,sticky=W)
Button(window1, text="Exit",width=12, command=exit, cursor="heart").grid(row=10,column=2,sticky=W)

window3=Frame(window)
window3.pack()
Label(window3).pack()

varProg = DoubleVar()
progress = Progressbar(window3, orient=HORIZONTAL, variable=varProg, length=600, mode = "determinate", maximum=100)
progress.pack()


window2=Frame(window)
window2.pack()
Label(window2).pack()
Label(window2, text= "Contributors: Demeveng Derrick & Tchuisse Micarel").pack()
Label(window2, text= "Contact: (+237) 6959000764 / (+237) 698787902").pack()
Label(window2, text= "Email: demeveng@gmail.com / mtchuis@gmail.com").pack()


# window2=Frame(window)
# window2.pack()
# figure = plt.Figure(figsize=(6,5), dpi=100)
# ax = figure.add_subplot(111)
# chart_type = FigureCanvasTkAgg(figure, window2)
# chart_type.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
# #df = df[['First Column','Second Column']].groupby('First Column').sum()
# #df.plot(kind='Chart Type such as bar', legend=True, ax=ax)
# ax.set_title('The Title for your chart')

window.mainloop()