import random
f=open("inp1000",'w')
f.write("inputMatrix =")
f.write("[")
for i in range(0,1000):
	f.write("[ ")
	for j in range(0,1000):
		if(i==j):
			f.write(" 0 ,")
		else:
			f.write(str(random.randint(1,100)))
			if(j!=999):
				f.write(" ,")
	if(i!=999):
		f.write("],")
	else:
		f.write("]")
f.write("]")
f.close

