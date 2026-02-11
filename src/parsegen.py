#!/usr/bin/env python3
from struct import *


def matfile(filename,*,dimx=4096,dimy=4096):
	'''
	Matrix file format .spn, .spn2, .sec 
	C. Wibisono
	02/14 '24
	Usage:
	To parse the matrix file.
	'''
	p=Struct("@i")
	with open(filename,mode='rb') as f:
		for i in range(0,dimy,1):
			for j in range(0,dimx,1):
				buff=f.read(4)
				temp,=p.unpack(buff)
				if temp != 0:
					print("i: ",i,"j: ",j,"val: ",temp)


def matwrite(filename,*,dimy,dimx,arr,overwrite):
	'''
	Matrix writer
	C. Wibisono
	02/18 '24
	Usage:
	To write and or update a matrix into a file.
	Function Arguments
	Filename : file to write/update
	dimy: int, y dimension
	dimx: int, x dimension
	arr: int[dimy][dimx], two dimensional array
	overwrite: int : 1 (to overwrite) or 0 (to append)
	'''
	p=Struct("@i")
	if overwrite == 1:
		with open(filename,mode='wb') as f:
			for i in range(0,dimy,1):
				for j in range(0,dimx,1):
					temp=arr[i][j]
					f.write(p.pack(temp))

			print("Completed\n")
	else:
		with open(filename,mode='rb') as f:
			for i in range(0,dimy,1):
				for j in range(0,dimx,1):
					buff=f.read(4)
					temp,=p.unpack(buff)
					arr[i][j]=arr[i][j]+temp
			print("Complete updating the matrix")
			print("Writing updated matrix")
		with open(filename,mode='wb') as f:
			for i in range(0,dimy,1):
				for j in range(0,dimx,1):
					temp=arr[i][j]
					f.write(p.pack(temp))

			print("Completed\n")
			

