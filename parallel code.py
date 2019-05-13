#!/usr/bin/env python

#rank==0 means master node


from mpi4py import MPI
from inp1000 import inputMatrix
from random import uniform
from random import randint 
import math
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

distanceMatrix = inputMatrix

def levyFlight(u):
	return math.pow(u,-1.0/3.0)#returns u^(-0.333)

def randF():
	return uniform(0.0001,0.9999)

def calculateDistance(path):
	index = path[0]
#	distanceMatrix[index][0]=rank #?
#supposed to do something here to make sure the values dont repeat accross nodes right now its 6 in all nodes
	distance = 0
	for nextIndex in path[1:]:
		distance += distanceMatrix[index][nextIndex]
		index = nextIndex
	return distance+distanceMatrix[path[-1]][path[0]];

def swap(sequence,i,j):
        temp = sequence[i]
        sequence[i]=sequence[j]
        sequence[j]=temp

def twoOptMove(nest,a,c):
	nest = nest[0][:]
	swap(nest,a,c)
	return (nest,calculateDistance(nest))
	

def doubleBridgeMove(nest,a,b,c,d):
	nest = nest[0][:]
	swap(nest,a,b)
	swap(nest,b,d)
	return (nest , calculateDistance(nest))

numNests = 10
pa = int(0.2*numNests)
pc = int(0.6*numNests)


maxGen = 50

n = len(inputMatrix)

nests = []
nest1 = []  #list()
fin=list()
initPath=list(range(0,n))
index = 0
swap(initPath,1,rank*40)
#print(initPath)
for i in range(numNests):
	if index == n-1:
		index = 0
	swap(initPath,index,index+1)
	index+=1
	nests.append((initPath[:],calculateDistance(initPath)))
#print(initPath)
#print(nests)


nests.sort(key=lambda tup: tup[1])
#print(nests)

for t in range(maxGen):
	cuckooNest = nests[randint(0,pc)]
	if(levyFlight(randF())>2):
		cuckooNest = doubleBridgeMove(cuckooNest,randint(0,n-1),randint(0,n-1),randint(0,n-1),randint(0,n-1))
	else:
		cuckooNest = twoOptMove(cuckooNest,randint(0,n-1),randint(0,n-1))
	randomNestIndex = randint(0,numNests-1)
	if(nests[randomNestIndex][1]>cuckooNest[1]):
		nests[randomNestIndex] = cuckooNest
	for i in range(numNests-pa,numNests):
		nests[i] = twoOptMove(nests[i],randint(0,n-1),randint(0,n-1))
	nests.sort(key=lambda tup: tup[1])	
if(rank==0):
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
	print("CUCKOO SOLUTION from Master:")
	print(nests[0])
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
if(rank==1):
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
	print("CUCKOO SOLUTION from Slave - 1:")
	print(nests[0])
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
if(rank==2):
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
	print("CUCKOO SOLUTION from Slave - 2:")
	print(nests[0])
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
#PPF_Print(MPI_COMM_WORLD,"hello")
#print(rank)
#print(nests)
nest1=comm.gather(nests[0],0)

if(rank==0):
	nest1.sort(key=lambda tup: tup[1])#prints sorted values, didnt work earlier cause you used gather and the other nodes didnt have any value for nest1[] 
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")	
	print("FINAL SOLUTION:(Best of the three solutions) : ") #It does wait for the other process
	print(nest1[0])
	fin=nest1[0]
	comm.bcast(nest1,root=0)
	print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")


'''isnt working for some reason '''
	
#if(rank!=0):
	#print(nest1)
	#fin=comm.Recv()

