#This program helps filter a file of x,y,z points into min and max values of a defined square.
import matplotlib.pyplot as plt
import operator
import matplotlib as mpl

plt.ion()

#open txt file
with open("semi.txt") as file:
	file = file.readlines()

	x=[]
	y=[]
	z=[]
	for i in file:
		x.append(float(i.split()[0]))
		y.append(float(i.split()[1]))
		z.append(float(i.split()[2]))
	
#	plt.scatter(x,y, marker='x', color='r')
#	plt.xlabel("Longitude (m)")
#	plt.ylabel("Latitude (m)")
#	plt.title("Scatter plot of cloud points")
#	plt.show()

#find the upper left conner and the lower right conner.
#Takes as input two list of x, y coordinates and outputs a tuple of x,y conners.
def upperLeftConner(xlist,ylist):
	xUpperLeftConner = min(xlist)
	yUpperLeftConner = max(ylist)
	return [xUpperLeftConner, yUpperLeftConner]

def lowerRightConner(xlist,ylist):
	xlowerRightConner = max(xlist)
	ylowerRightConner = min(ylist)
	return [xlowerRightConner, ylowerRightConner]

#defines the bounding box of the points
#takes as input two tuples representing the upper left conner and the lower right conner.
def box(ulc,lrc):
	plt.plot([ulc[0],lrc[0],lrc[0],lrc[0],ulc[0],ulc[0]],[ulc[1],ulc[1],lrc[1],lrc[1],lrc[1],ulc[1]])
	#plt.show()

#define the sampling box
#takes the upper left conner and the sampling distance in tuples

def sampleBox(ulc,dist):
	x = ulc[0]+dist[0]
	y = ulc[1]-dist[1]

	plt.plot([ulc[0],x,x,x,ulc[0],ulc[0]],[ulc[1],ulc[1],y,y,y,ulc[1]], color='black')
	#plt.show()
	return[x,y,dist]

ulc = upperLeftConner(x,y)
lrc = lowerRightConner(x,y)
bb  = sampleBox(ulc,[50,50])

plt.scatter(x,y, marker='x', color='r')
# box(luc,lrc)
# sampleBox(luc,(100,100))
# plt.xlabel("Longitude (m)")
# plt.ylabel("Latitude (m)")
# plt.title("Scatter plot of cloud points")
# plt.show()

i = (((lrc[0]-ulc[0])>0) & ((lrc[1]-ulc[1])<0))

print(i)
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

	rslt1[:] = []

	plt.pause(0.0001)

	if (lrc[0]-bb[0])>0:
		bb  = sampleBox((bb[0],ulc[1]),(50,50)) 
		dst = bb[2]
		ulc[0] = ulc[0]+dst[0]
		k += 1
	
	elif (lrc[1]-ulc[1])<0:
		l += 1
		bb = []
		ulc[1] = ulc[1] - dst[0]
		ulc[0] = ulc[0] - k*dst[0]
		bb  = sampleBox((ulc[0],ulc[1]),(50,50))
		k=0
		
		i = (((lrc[0]-ulc[0])>0) & ((lrc[1]-ulc[1])<0))

# print(rslt1)
print(i)
print(rslt3)
ix = [k[0] for k in rslt1]
iy = [k[1] for k in rslt1]
jx = [l[0] for l in rslt3]
jy = [l[1] for l in rslt3]

plt.pause(0.0001)
plt.scatter(ix,iy, color="blue", marker="x")
plt.pause(0.0001)
plt.scatter(jx,jy, color="green", marker="o", s=100, alpha=0.3)
plt.xlabel("East/Longitude (m)")
plt.xlabel("Nord/Latitude  (m)")
plt.title("Point Clouds")
plt.pause(10000)
#plt.show()