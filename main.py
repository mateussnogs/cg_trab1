#!/usr/bin/env python
# coding: UTF-8
#
## @package _12_tet
#
#  Draws a 3D tetrahedron and allows a user to rotate it
#  (mouse left button and wheel).
#
#  The Tetrahedron is represented by a 3 x 4 matrix. 
#  Each column represents a 3D vertex.
#
#  note: a m x n matrix is represented by a list of lines:
#     [[l_1] [l_2] .. [l_m]].
#  m = len(mat), n = len(mat[0]), mat(i,j) = mat[i][j]
#
#  @author Paulo Roma
#  @since 01/05/2014
#  @see http://www.orimosenzon.com/wiki/index.php/Python_samples
#  @see http://mathworld.wolfram.com/RotationMatrix.html

try:
   from tkinter import *     # python 3
except ImportError:
   from Tkinter import *     # python 2
from math import *

from mapper.mapper import Mapper # map coordinates
import sys # to read parameters from command line
from matrix.ops import *
from mapper.mymapper import AffineMapper
from vector import *

   
def drawTet(tet,col):
	"""Draw a tetrahedron."""
	global tetNormals
	global normalsOn

	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.delete(ALL) # delete all edges
	nv = len(tet[0])   # number of vertices in tet (4)

	face1 = [tet[0][1], tet[1][1], tet[0][2], tet[1][2], tet[0][3], tet[1][3], tet[0][1], tet[1][1]]    
	face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
	tetNormals[0] = polygonNormal([tet[0][1], tet[1][1], tet[2][1], tet[0][2],
		 tet[1][2], tet[2][2], tet[0][3], tet[1][3], tet[2][3]], tet)

	face2 = [tet[0][1], tet[1][1], tet[0][0], tet[1][0], tet[0][2], tet[1][2], tet[0][1], tet[1][1]]
	face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]
	tetNormals[1] = polygonNormal([tet[0][1], tet[1][1], tet[2][1], 
		tet[0][0], tet[1][0], tet[2][0], tet[0][2], tet[1][2], tet[2][2]], tet)

	face3 = [tet[0][3], tet[1][3], tet[0][2], tet[1][2], tet[0][0], tet[1][0], tet[0][3], tet[1][3]]
	face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]
	tetNormals[2] = polygonNormal([tet[0][3], tet[1][3], tet[2][3], tet[0][2],
		 tet[1][2], tet[2][2], tet[0][0], tet[1][0], tet[2][0]], tet)

	face4 = [tet[0][0], tet[1][0], tet[0][1], tet[1][1], tet[0][3], tet[1][3], tet[0][0], tet[1][0]]
	face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]
	tetNormals[3] = polygonNormal([tet[0][0], tet[1][0], tet[2][0], tet[0][1],
		 tet[1][1], tet[2][1], tet[0][3], tet[1][3], tet[2][3]], tet)

	faces = [face1, face2, face3, face4]  

	facesToDraw = backfaceCulling(tetNormals)
	for faceNumber in facesToDraw:
		canvas.create_polygon(faces[faceNumber], outline='red',
	        fill='dark slate gray', width=1)
		if (normalsOn):
			drawNormal(tetNormals[faceNumber], faces[faceNumber])    


def drawCube(cube, col):
	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.delete(ALL) # delete all edges
	nv = len(cube[0])   # number of vertices in cube (8)
	global cubeNormals
	global normalsOn

	# draw the 6 faces of the tetrahedron
	face1 = [
		cube[0][0], cube[1][0], 
	    cube[0][1], cube[1][1],
	    cube[0][3], cube[1][3],
	    cube[0][2], cube[1][2],
	    cube[0][0], cube[1][0]
	   ]
	face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
	cubeNormals[0] = polygonNormal([cube[0][0], cube[1][0], cube[2][0], cube[0][1], cube[1][1],
	 cube[2][1], cube[0][3], cube[1][3], cube[2][3], cube[0][2], cube[1][2], cube[2][2]], cube) 
		
	face2 = [
		cube[0][1], cube[1][1],
	    cube[0][5], cube[1][5], 
	    cube[0][7], cube[1][7],
	    cube[0][3], cube[1][3],
	    cube[0][1], cube[1][1] 
	]    
	face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]
	cubeNormals[1] = polygonNormal([cube[0][1], cube[1][1], cube[2][1], cube[0][5], 
		cube[1][5], cube[2][5], cube[0][7], cube[1][7], cube[2][7], cube[0][3], cube[1][3], cube[2][3]], cube) 

	face3 = [
		cube[0][0], cube[1][0],
	    cube[0][4], cube[1][4], 
	    cube[0][6], cube[1][6],
	    cube[0][2], cube[1][2],
	    cube[0][0], cube[1][0] 
	]
	face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]
	cubeNormals[2] = polygonNormal([cube[0][0], cube[1][0], cube[2][0], cube[0][4], cube[1][4], cube[2][4], cube[0][6],
	 cube[1][6], cube[2][6], cube[0][2], cube[1][2], cube[2][2]], cube)
	face4 = [
		cube[0][0], cube[1][0],
	    cube[0][1], cube[1][1], 
	    cube[0][5], cube[1][5],
	    cube[0][4], cube[1][4],
	    cube[0][0], cube[1][0] 
	]	
	face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]
	cubeNormals[3] = polygonNormal([cube[0][0], cube[1][0], cube[2][0], cube[0][1], cube[1][1], cube[2][1],
	 cube[0][5], cube[1][5], cube[2][5], cube[0][4], cube[1][4], cube[2][4]], cube)
	face5 = [
		cube[0][2], cube[1][2],
	    cube[0][3], cube[1][3], 
	    cube[0][7], cube[1][7],
	    cube[0][6], cube[1][6],
	    cube[0][2], cube[1][2]
	]	
	face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]
	cubeNormals[4] = polygonNormal([cube[0][2], cube[1][2], cube[2][2], cube[0][3], cube[1][3], cube[2][3], cube[0][7], 
		cube[1][7], cube[2][7], cube[0][6], cube[1][6], cube[2][6]], cube)
	face6 = [
		cube[0][4], cube[1][4],
	    cube[0][5], cube[1][5], 
	    cube[0][7], cube[1][7],
	    cube[0][6], cube[1][6],
	    cube[0][4], cube[1][4]
	]	
	face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]
	cubeNormals[5] = polygonNormal([cube[0][4], cube[1][4], cube[2][4], cube[0][5], cube[1][5], cube[2][5], cube[0][7],
	 cube[1][7], cube[2][7], cube[0][6], cube[1][6], cube[2][6]], cube)     
	faces = [face1, face2, face3, face4, face5, face6]
	facesToDraw = backfaceCulling(cubeNormals)
	for faceNumber in facesToDraw:
		canvas.create_polygon(faces[faceNumber], outline='red',
	        fill='blue', width=1)
		if (normalsOn):
			drawNormal(cubeNormals[faceNumber], faces[faceNumber])     


def drawOctahedron(octa, col):
	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.delete(ALL) # delete all edges
	global octaNormals
	global normalsOn

	face1 = [
		octa[0][4], octa[1][4], octa[0][0], octa[1][0], octa[0][1], octa[1][1], octa[0][4], octa[1][4]
	]
	face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
	octaNormals[0] = polygonNormal([
		octa[0][4], octa[1][4], octa[2][4], octa[0][0], octa[1][0], octa[2][0], octa[0][1], octa[1][1], octa[2][1]
	], octa)

	face2 = [
		octa[0][4], octa[1][4], octa[0][1], octa[1][1], octa[0][2], octa[1][2], octa[0][4], octa[1][4]
	]
	face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]
	octaNormals[1] = polygonNormal([
		octa[0][4], octa[1][4], octa[2][4], octa[0][1], octa[1][1], octa[2][1], octa[0][2], octa[1][2], octa[2][2]
	], octa)

	face3 = [
		octa[0][4], octa[1][4], octa[0][2], octa[1][2], octa[0][3], octa[1][3], octa[0][4], octa[1][4]
	]
	face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]
	octaNormals[2] = polygonNormal([
		octa[0][4], octa[1][4], octa[2][4], octa[0][2], octa[1][2], octa[2][2], octa[0][3], octa[1][3], octa[2][3]
	], octa)        

	face4 = [
		octa[0][4], octa[1][4], octa[0][3], octa[1][3], octa[0][0], octa[1][0], octa[0][4], octa[1][4]
	]
	face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]
	octaNormals[3] = polygonNormal([
		octa[0][4], octa[1][4], octa[2][4], octa[0][3], octa[1][3], octa[2][3], octa[0][0], octa[1][0], octa[2][0]
	], octa)        

	face5 = [
		octa[0][5], octa[1][5], octa[0][1], octa[1][1], octa[0][0], octa[1][0], octa[0][5], octa[1][5]
	]
	face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]
	octaNormals[4] = polygonNormal([
		octa[0][5], octa[1][5], octa[2][5], octa[0][1], octa[1][1], octa[2][1], octa[0][0], octa[1][0], octa[2][0]
	], octa)    
	face6 = [
		octa[0][5], octa[1][5], octa[0][2], octa[1][2], octa[0][1], octa[1][1], octa[0][5], octa[1][5]
	]
	face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]  
	octaNormals[5] = polygonNormal([
		octa[0][5], octa[1][5], octa[2][5], octa[0][2], octa[1][2], octa[2][2], octa[0][1], octa[1][1], octa[2][1]
	], octa)          

	face7 = [
		octa[0][5], octa[1][5], octa[0][3], octa[1][3], octa[0][2], octa[1][2], octa[0][5], octa[1][5]
	]
	face7 = [translate(face7[i], face7[i+1], w, h) for i in range(0, len(face7), 2)]
	octaNormals[6] = polygonNormal([
		octa[0][5], octa[1][5], octa[2][5], octa[0][3], octa[1][3], octa[2][3], octa[0][2], octa[1][2], octa[2][2]
	], octa)            
	face8 = [
		octa[0][5], octa[1][5], octa[0][0], octa[1][0], octa[0][3], octa[1][3], octa[0][5], octa[1][5]
	]
	face8 = [translate(face8[i], face8[i+1], w, h) for i in range(0, len(face8), 2)]          
	octaNormals[7] = polygonNormal([
		octa[0][5], octa[1][5], octa[2][5], octa[0][0], octa[1][0], octa[2][0], octa[0][3], octa[1][3], octa[2][3]
	], octa)
	faces = [face1, face2, face3, face4, face5, face6, face7, face8]            

	facesToDraw = backfaceCulling(octaNormals)
	for faceNumber in facesToDraw:
		canvas.create_polygon(faces[faceNumber], outline='red',
            fill='pink', width=1)
		if (normalsOn):
			drawNormal(octaNormals[faceNumber], faces[faceNumber])

def drawDodecahedron(dodec, col):
	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.delete(ALL) # delete all edges
	global dodecNormals
	global normalsOn

	face1 = [
		dodec[0][1], dodec[1][1], dodec[0][2], dodec[1][2], dodec[0][18], dodec[1][18], dodec[0][11], dodec[1][11], dodec[0][14], dodec[1][14], dodec[0][1], dodec[1][1] 
	]        
	face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
	dodecNormals[0] = polygonNormal([
		dodec[0][1], dodec[1][1], dodec[2][1], dodec[0][2], dodec[1][2], dodec[2][2], dodec[0][18], dodec[1][18], dodec[2][18], 
		dodec[0][11], dodec[1][11], dodec[2][11], dodec[0][14], dodec[1][14], dodec[2][14], dodec[0][1], dodec[1][1], dodec[2][1] 
	], dodec)

	face2 = [
		dodec[0][1], dodec[1][1], dodec[0][13], dodec[1][13], dodec[0][7], dodec[1][7], dodec[0][17], dodec[1][17], dodec[0][2], dodec[1][2], dodec[0][1], dodec[1][1] 
	]        
	face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]
	dodecNormals[1] = polygonNormal([
		dodec[0][1], dodec[1][1], dodec[2][1], dodec[0][13], dodec[1][13], dodec[2][13], dodec[0][7], dodec[1][7], dodec[2][7], 
		dodec[0][17], dodec[1][17], dodec[2][17], dodec[0][2], dodec[1][2], dodec[2][2], dodec[0][1], dodec[1][1], dodec[2][1]
	], dodec)
	face3 = [
		dodec[0][3], dodec[1][3], dodec[0][4], dodec[1][4], dodec[0][19], dodec[1][19], dodec[0][8], dodec[1][8], dodec[0][15], dodec[1][15], dodec[0][3], dodec[1][3] 
	]        
	face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]
	dodecNormals[2] = polygonNormal([
		dodec[0][3], dodec[1][3], dodec[2][3], dodec[0][4], dodec[1][4], dodec[2][4], dodec[0][19], dodec[1][19], dodec[2][19], 
		dodec[0][8], dodec[1][8], dodec[2][8], dodec[0][15], dodec[1][15], dodec[2][15], dodec[0][3], dodec[1][3], dodec[2][3]
	], dodec)

	face4 = [
		dodec[0][3], dodec[1][3], dodec[0][16], dodec[1][16], dodec[0][12], dodec[1][12], dodec[0][0], dodec[1][0], dodec[0][4], dodec[1][4], dodec[0][3], dodec[1][3] 
	]        
	face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]
	dodecNormals[3] = polygonNormal([
		dodec[0][3], dodec[1][3], dodec[2][3], dodec[0][16], dodec[1][16], dodec[2][16], dodec[0][12], dodec[1][12], dodec[2][12], 
			dodec[0][0], dodec[1][0], dodec[2][0], dodec[0][4], dodec[1][4], dodec[2][4], dodec[0][3], dodec[1][3], dodec[2][3]
	], dodec)
	face5 = [
		dodec[0][3], dodec[1][3], dodec[0][15], dodec[1][15], dodec[0][6], dodec[1][6], dodec[0][5], dodec[1][5], dodec[0][16], dodec[1][16], dodec[0][3], dodec[1][3] 
	]        
	face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]                   
	dodecNormals[4] = polygonNormal([
		dodec[0][3], dodec[1][3], dodec[2][3], dodec[0][15], dodec[1][15], dodec[2][15], dodec[0][6], dodec[1][6], dodec[2][6], 
		dodec[0][5], dodec[1][5], dodec[2][5], dodec[0][16], dodec[1][16], dodec[2][16], dodec[0][3], dodec[1][3], dodec[2][3]
	], dodec)
	face6 = [
		dodec[0][1], dodec[1][1], dodec[0][14], dodec[1][14], dodec[0][5], dodec[1][5], dodec[0][6], dodec[1][6], dodec[0][13], dodec[1][13], dodec[0][1], dodec[1][1] 
	]        
	face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]     
	dodecNormals[5] = polygonNormal([
		dodec[0][1], dodec[1][1], dodec[2][1], dodec[0][14], dodec[1][14], dodec[2][14], dodec[0][5], dodec[1][5], dodec[2][5], 
		dodec[0][6], dodec[1][6], dodec[2][6], dodec[0][13], dodec[1][13], dodec[2][13], dodec[0][1], dodec[1][1], dodec[2][1] 
	], dodec)

	face7 = [
		dodec[0][2], dodec[1][2], dodec[0][17], dodec[1][17], dodec[0][9], dodec[1][9], dodec[0][10], dodec[1][10], dodec[0][18], dodec[1][18], dodec[0][2], dodec[1][2] 
	]        
	face7 = [translate(face7[i], face7[i+1], w, h) for i in range(0, len(face7), 2)] 
	dodecNormals[6] = polygonNormal([
		dodec[0][2], dodec[1][2], dodec[2][2], dodec[0][17], dodec[1][17], dodec[2][17], dodec[0][9], dodec[1][9], dodec[2][9], 
		dodec[0][10], dodec[1][10], dodec[2][10], dodec[0][18], dodec[1][18], dodec[2][18], dodec[0][2], dodec[1][2], dodec[2][2] 
	], dodec)

	face8 = [
		dodec[0][4], dodec[1][4], dodec[0][0], dodec[1][0], dodec[0][10], dodec[1][10], dodec[0][9], dodec[1][9], dodec[0][19], dodec[1][19], dodec[0][4], dodec[1][4] 
	]        
	face8 = [translate(face8[i], face8[i+1], w, h) for i in range(0, len(face8), 2)]
	dodecNormals[7] = polygonNormal([
		dodec[0][4], dodec[1][4], dodec[2][4], dodec[0][0], dodec[1][0], dodec[2][0], dodec[0][10], dodec[1][10], dodec[2][10], 
		dodec[0][9], dodec[1][9], dodec[2][9], dodec[0][19], dodec[1][19], dodec[2][19], dodec[0][4], dodec[1][4], dodec[2][4]
	], dodec)

	face9 = [
		dodec[0][7], dodec[1][7], dodec[0][8], dodec[1][8], dodec[0][19], dodec[1][19], dodec[0][9], dodec[1][9], dodec[0][17], dodec[1][17], dodec[0][7], dodec[1][7] 
	]        
	face9 = [translate(face9[i], face9[i+1], w, h) for i in range(0, len(face9), 2)]
	dodecNormals[8] = polygonNormal([
		dodec[0][7], dodec[1][7], dodec[2][7], dodec[0][8], dodec[1][8], dodec[2][8], dodec[0][19], dodec[1][19], dodec[2][19], 
		dodec[0][9], dodec[1][9], dodec[2][9], dodec[0][17], dodec[1][17], dodec[2][17], dodec[0][7], dodec[1][7], dodec[2][7] 
	], dodec)

	face10 = [
		dodec[0][6], dodec[1][6], dodec[0][15], dodec[1][15], dodec[0][8], dodec[1][8], dodec[0][7], dodec[1][7], dodec[0][13], dodec[1][13], dodec[0][6], dodec[1][6] 
	]        
	face10 = [translate(face10[i], face10[i+1], w, h) for i in range(0, len(face10), 2)]
	dodecNormals[9] = polygonNormal([
		dodec[0][6], dodec[1][6], dodec[2][6], dodec[0][15], dodec[1][15], dodec[2][15], dodec[0][8], dodec[1][8], dodec[2][8], 
		dodec[0][7], dodec[1][7], dodec[2][7], dodec[0][13], dodec[1][13], dodec[2][13], dodec[0][6], dodec[1][6], dodec[2][6]
	], dodec)

	face11 = [
		dodec[0][5], dodec[1][5], dodec[0][14], dodec[1][14], dodec[0][11], dodec[1][11], dodec[0][12], dodec[1][12], dodec[0][16], dodec[1][16], dodec[0][5], dodec[1][5] 
	]        
	face11 = [translate(face11[i], face11[i+1], w, h) for i in range(0, len(face11), 2)] 
	dodecNormals[10] = polygonNormal([
		dodec[0][5], dodec[1][5], dodec[2][5], dodec[0][14], dodec[1][14], dodec[2][14], dodec[0][11], dodec[1][11], dodec[2][11], 
		dodec[0][12], dodec[1][12], dodec[2][12], dodec[0][16], dodec[1][16], dodec[2][16], dodec[0][5], dodec[1][5], dodec[2][5]
	], dodec)  

	face12 = [
		dodec[0][10], dodec[1][10], dodec[0][0], dodec[1][0], dodec[0][12], dodec[1][12], dodec[0][11], dodec[1][11], dodec[0][18], dodec[1][18], dodec[0][10], dodec[1][10] 
	]        
	face12 = [translate(face12[i], face12[i+1], w, h) for i in range(0, len(face12), 2)] 
	dodecNormals[11] = polygonNormal([
		dodec[0][10], dodec[1][10], dodec[2][10], dodec[0][0], dodec[1][0], dodec[2][0], dodec[0][12], dodec[1][12], dodec[2][12], 
		dodec[0][11], dodec[1][11], dodec[2][11], dodec[0][18], dodec[1][18], dodec[2][18], dodec[0][10], dodec[1][10], dodec[2][10]
	], dodec)                 
	faces = [face1, face2, face3, face4, face5, face6, face7, face8, face9, face10, face11, face12]            
	facesToDraw = backfaceCulling(dodecNormals)
	for faceNumber in facesToDraw:
		canvas.create_polygon(faces[faceNumber], outline='red',
            fill='black', width=1)
		if (normalsOn):
			drawNormal(dodecNormals[faceNumber], faces[faceNumber])

def drawIcosahedron(ico, col):
	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.delete(ALL) # delete all edges
	global icoNormals
	global normalsOn

	face1 = [ico[0][6], ico[1][6], ico[0][2], ico[1][2], ico[0][1], ico[1][1], ico[0][6], ico[1][6]]
	face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
	icoNormals[0] = polygonNormal([
		ico[0][6], ico[1][6], ico[2][6], ico[0][2], ico[1][2], ico[2][2], ico[0][1], ico[1][1], ico[2][1]
		], ico)

	face2 = [ico[0][2], ico[1][2], ico[0][7], ico[1][7], ico[0][1], ico[1][1], ico[0][2], ico[1][2]]
	face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]
	icoNormals[1] = polygonNormal([
		ico[0][2], ico[1][2], ico[2][2], ico[0][7], ico[1][7], ico[2][7], ico[0][1], ico[1][1], ico[2][1]
	], ico)

	face3 = [ico[0][5], ico[1][5], ico[0][4], ico[1][4], ico[0][3], ico[1][3], ico[0][5], ico[1][5]]
	face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]
	icoNormals[2] = polygonNormal([
		ico[0][5], ico[1][5], ico[2][5], ico[0][4], ico[1][4], ico[2][4], ico[0][3], ico[1][3], ico[2][3]
		], ico)

	face4 = [ico[0][8], ico[1][8], ico[0][3], ico[1][3], ico[0][4], ico[1][4], ico[0][8], ico[1][8]]
	face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]
	icoNormals[3] = polygonNormal([
		ico[0][8], ico[1][8], ico[2][8], ico[0][3], ico[1][3], ico[2][3], ico[0][4], ico[1][4], ico[2][4]
		], ico)

	face5 = [ico[0][11], ico[1][11], ico[0][5], ico[1][5], ico[0][6], ico[1][6], ico[0][11], ico[1][11]]
	face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]
	icoNormals[4] = polygonNormal([
		ico[0][11], ico[1][11], ico[2][11], ico[0][5], ico[1][5], ico[2][5], ico[0][6], ico[1][6], ico[2][6]
		], ico)
	
	face6 = [ico[0][10], ico[1][10], ico[0][6], ico[1][6], ico[0][5], ico[1][5], ico[0][10], ico[1][10]]
	face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]
	icoNormals[5] = polygonNormal([
		ico[0][10], ico[1][10], ico[2][10], ico[0][6], ico[1][6], ico[2][6], ico[0][5], ico[1][5], ico[2][5]
		], ico)

	face7 = [ico[0][2], ico[1][2], ico[0][10], ico[1][10], ico[0][9], ico[1][9], ico[0][2], ico[1][2]]
	face7 = [translate(face7[i], face7[i+1], w, h) for i in range(0, len(face7), 2)]
	icoNormals[6] = polygonNormal([
		ico[0][2], ico[1][2], ico[2][2], ico[0][10], ico[1][10], ico[2][10], ico[0][9], ico[1][9], ico[2][9]
	], ico)

	face8 = [ico[0][3], ico[1][3], ico[0][9], ico[1][9], ico[0][10], ico[1][10], ico[0][3], ico[1][3]]
	face8 = [translate(face8[i], face8[i+1], w, h) for i in range(0, len(face8), 2)]
	icoNormals[7] = polygonNormal([
		ico[0][3], ico[1][3], ico[2][3], ico[0][9], ico[1][9], ico[2][9], ico[0][10], ico[1][10], ico[2][10]
	], ico)

	face9 = [ico[0][9], ico[1][9], ico[0][8], ico[1][8], ico[0][7], ico[1][7], ico[0][9], ico[1][9]]
	face9 = [translate(face9[i], face9[i+1], w, h) for i in range(0, len(face9), 2)]
	icoNormals[8] = polygonNormal([
		ico[0][9], ico[1][9], ico[2][9], ico[0][8], ico[1][8], ico[2][8], ico[0][7], ico[1][7], ico[2][7]
	], ico)

	face10 = [ico[0][0], ico[1][0], ico[0][7], ico[1][7], ico[0][8], ico[1][8], ico[0][0], ico[1][0]]
	face10 = [translate(face10[i], face10[i+1], w, h) for i in range(0, len(face10), 2)]
	icoNormals[9] = polygonNormal([
		ico[0][0], ico[1][0], ico[2][0], ico[0][7], ico[1][7], ico[2][7], ico[0][8], ico[1][8], ico[2][8]
	], ico)

	face11 = [ico[0][1], ico[1][1], ico[0][0], ico[1][0], ico[0][11], ico[1][11], ico[0][1], ico[1][1]]
	face11 = [translate(face11[i], face11[i+1], w, h) for i in range(0, len(face11), 2)]
	icoNormals[10] = polygonNormal([
		ico[0][1], ico[1][1], ico[2][1], ico[0][0], ico[1][0], ico[2][0], ico[0][11], ico[1][11], ico[2][11]
	], ico)

	face12 = [ico[0][4], ico[1][4], ico[0][11], ico[1][11], ico[0][0], ico[1][0], ico[0][4], ico[1][4]]
	face12 = [translate(face12[i], face12[i+1], w, h) for i in range(0, len(face12), 2)]
	icoNormals[11] = polygonNormal([
		ico[0][4], ico[1][4], ico[2][4], ico[0][11], ico[1][11], ico[2][11], ico[0][0], ico[1][0], ico[2][0]
	], ico)

	face13 = [ico[0][10], ico[1][10], ico[0][2], ico[1][2], ico[0][6], ico[1][6], ico[0][10], ico[1][10]]
	face13 = [translate(face13[i], face13[i+1], w, h) for i in range(0, len(face13), 2)]
	icoNormals[12] = polygonNormal([
		ico[0][10], ico[1][10], ico[2][10], ico[0][2], ico[1][2], ico[2][2], ico[0][6], ico[1][6], ico[2][6]
	], ico)

	face14 = [ico[0][11], ico[1][11], ico[0][6], ico[1][6], ico[0][1], ico[1][1], ico[0][11], ico[1][11]]
	face14 = [translate(face14[i], face14[i+1], w, h) for i in range(0, len(face14), 2)]
	icoNormals[13] = polygonNormal([
		ico[0][11], ico[1][11], ico[2][11], ico[0][6], ico[1][6], ico[2][6], ico[0][1], ico[1][1], ico[2][1]
	], ico)

	face15 = [ico[0][10], ico[1][10], ico[0][5], ico[1][5], ico[0][3], ico[1][3], ico[0][10], ico[1][10]]
	face15 = [translate(face15[i], face15[i+1], w, h) for i in range(0, len(face15), 2)]
	icoNormals[14] = polygonNormal([
		ico[0][10], ico[1][10], ico[2][10], ico[0][5], ico[1][5], ico[2][5], ico[0][3], ico[1][3], ico[2][3]
	], ico)

	face16 = [ico[0][11], ico[1][11], ico[0][4], ico[1][4], ico[0][5], ico[1][5], ico[0][11], ico[1][11]]
	face16 = [translate(face16[i], face16[i+1], w, h) for i in range(0, len(face16), 2)]
	icoNormals[15] = polygonNormal([
		ico[0][11], ico[1][11], ico[2][11], ico[0][4], ico[1][4], ico[2][4], ico[0][5], ico[1][5], ico[2][5]
	], ico)

	face17 = [ico[0][9], ico[1][9], ico[0][7], ico[1][7], ico[0][2], ico[1][2], ico[0][9], ico[1][9]]
	face17 = [translate(face17[i], face17[i+1], w, h) for i in range(0, len(face17), 2)]
	icoNormals[16] = polygonNormal([
		ico[0][9], ico[1][9], ico[2][9], ico[0][7], ico[1][7], ico[2][7], ico[0][2], ico[1][2], ico[2][2]
	], ico)

	face18 = [ico[0][0], ico[1][0], ico[0][1], ico[1][1], ico[0][7], ico[1][7], ico[0][0], ico[1][0]]
	face18 = [translate(face18[i], face18[i+1], w, h) for i in range(0, len(face18), 2)]
	icoNormals[17] = polygonNormal([
		ico[0][0], ico[1][0], ico[2][0], ico[0][1], ico[1][1], ico[2][1], ico[0][7], ico[1][7], ico[2][7]
	], ico)

	face19 = [ico[0][8], ico[1][8], ico[0][9], ico[1][9], ico[0][3], ico[1][3], ico[0][8], ico[1][8]]
	face19 = [translate(face19[i], face19[i+1], w, h) for i in range(0, len(face19), 2)]
	icoNormals[18] = polygonNormal([
		ico[0][8], ico[1][8], ico[2][8], ico[0][9], ico[1][9], ico[2][9], ico[0][3], ico[1][3], ico[2][3]
	], ico)

	face20 = [ico[0][0], ico[1][0], ico[0][8], ico[1][8], ico[0][4], ico[1][4], ico[0][0], ico[1][0]]
	face20 = [translate(face20[i], face20[i+1], w, h) for i in range(0, len(face20), 2)]
	icoNormals[19] = polygonNormal([
		ico[0][0], ico[1][0], ico[2][0], ico[0][8], ico[1][8], ico[2][8], ico[0][4], ico[1][4], ico[2][4]
	], ico)

	faces = [face1, face2, face3, face4, face5, face6, face7, face8, face9, face10, face11, 
		face12, face13, face14, face15, face16, face17, face18, face19, face20]            
	facesToDraw = backfaceCulling(icoNormals)
	for faceNumber in facesToDraw:
		canvas.create_polygon(faces[faceNumber], outline='red',
            fill='black', width=1)
		if (normalsOn):
			drawNormal(icoNormals[faceNumber], faces[faceNumber])

	

def innerProduct(v1, v2):
	return sum([v1[i]*v2[i] for i in range(len(v1))])

def backfaceCulling(normals):
	facesToDraw = []
	for i in range(len(normals)):	
		if innerProduct([0, 0, -1], normals[i]) > 0:
		# if (normals[i][2] > 0):
			facesToDraw.append(i)
	return facesToDraw
    
def polygonNormal(polygon, polyhedron):
	normal = [0, 0, 0]
	nv = len(polygon)//3 # each vertex has 3 coordinates
	n = len(polygon)
	for i in range(0, n, 3):
		x1, y1, z1 = polygon[i], polygon[i+1], polygon[i+2]
		x2, y2, z2 = polygon[(i+3)%n], polygon[(i+3+1)%n], polygon[(i+3+2)%n]
		normal[0] += (y1-y2)*(z1+z2)
		normal[1] += (z1-z2)*(x1+x2)
		normal[2] += (x1-x2)*(y1+y2)
	
	centroid = polygonCentroid(polygon)
	solid_centroid = polyhedronCentroid(polyhedron)
	centroid_dif = normalize(vecDif(solid_centroid, centroid))
	normal = normalize(normal)
	if innerProduct(centroid_dif, normal) > 0:
		normal = list(map(lambda x:-x, normal)) # invert direction
	return normal

def polygonCentroid(polygon):
	cx = cy = cz = 0
	nv = int(len(polygon)/3) # to do: use //; each vertex has 3 coordinates
	for i in range(0, nv*3, 3):
		cx += polygon[i]
		cy += polygon[i+1]
		cz += polygon[i+2]
	cx /= nv
	cy /= nv
	cz /= nv
	return [cx, cy, cz]

def polygonCentroid2D(polygon):
	cx = cy = 0
	nv = len(polygon)
	for i in range(nv-1):
		cx += polygon[i][0]
		cy += polygon[i][1]
	cx /= nv-1
	cy /= nv-1
	return [cx, cy]

def polyhedronCentroid(polyhedron):
	cx = cy = cz = 0
	faces = len(polyhedron)
	for i in range(faces):
		cx_temp, cy_temp, cz_temp = polygonCentroid(polyhedron[i])
		cx += cx_temp
		cy += cy_temp
		cz += cz_temp
	cx /= faces
	cy /= faces
	cz /= faces
	return [cx, cy, cz]

                                                                                    
    
def normalize(v):
	size = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
	return [v[0]/size, v[1]/size, v[2]/size]

def drawNormal(normal, face):
	cx, cy = polygonCentroid2D(face)
	normal = list(map(lambda x:x*30, normal))	
	canvas.create_line(cx, cy, normal[0]+cx, normal[1]+cy, fill='gold', width=2, arrow=LAST)

def drawNormalsPolyhedron(polyhedron):
	for polygon in polyhedron:
		drawNormals(polygon)

def drawBoundingBox(box):
	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.create_line(translate(box[0][0], box[1][0], w, h), translate(box[0][1], box[1][1], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][1], box[1][1], w, h), translate(box[0][3], box[1][3], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][3], box[1][3], w, h), translate(box[0][2], box[1][2], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][2], box[1][2], w, h), translate(box[0][0], box[1][0], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][0], box[1][0], w, h), translate(box[0][4], box[1][4], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][4], box[1][4], w, h), translate(box[0][5], box[1][5], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][5], box[1][5], w, h), translate(box[0][1], box[1][1], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][5], box[1][5], w ,h), translate(box[0][7], box[1][7], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][7], box[1][7], w ,h), translate(box[0][6], box[1][6], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][6], box[1][6], w, h), translate(box[0][4], box[1][4], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][3], box[1][3], w, h), translate(box[0][7], box[1][7], w, h), fill="OliveDrab1", width=5)
	canvas.create_line(translate(box[0][2], box[1][2], w, h), translate(box[0][6], box[1][6], w, h), fill="OliveDrab1", width=5)


def buildBox(polyhedron):
	dists = []
	# centroid = polyhedronCentroid(polyhedron)
	o = [0, 0, 0]
	for i in range(len(polyhedron)):
		for j in range(len(polyhedron[i])):
			dists.append(abs(polyhedron[i][j]))
	d = max(dists)
	box = [
			[-d, d, -d, 1], [d, d, -d, 1], [-d, -d, -d, 1], [d, -d, -d, 1],
			[-d, d, d, 1], [d, d, d, 1], [-d, -d, d, 1], [d, -d, d, 1]
	]
	box = matTrans(box)
	return box
                
def init():
	"""Initialize global variables."""

	global ROT_X, ROT_Y, ROT_Z
	global eps, EPS, tet, ax, boxes, cube, octa, dodec, ico
	global lastX, lastY, tetColor, bgColor
	global tetNormals, cubeNormals, octaNormals, dodecNormals, icoNormals
	global curPoly
	global normalsOn
	global activateAxes, activateBBox

	curPoly = 'cube'
	activateAxes = activateBBox = False
	normalsOn = False

	tetNormals = [[0]*9]*4
	cubeNormals = [[0]*12]*6
	octaNormals = [[0]*9]*8
	dodecNormals = [[0]*15]*12
	icoNormals = [[0]*9]*20

	boxes = []

	mapper = AffineMapper([-1, -1, -1, 1, 1, 1], [-200, -200, -200, 200, 200, 200])

	tet = [[-0.5, -0.5, -0.5, 1], [0.5, 0.5, -0.5, 1], [0.5, -0.5, 0.5, 1], [-0.5, 0.5, 0.5, 1]]
	tet = matTrans(tet)
	tet = mapper.worldToViewport(tet)
	boxes.append(buildBox(tet))


	cube = [
			[-0.5, 0.5, -0.5, 1], [0.5, 0.5, -0.5, 1], [-0.5, -0.5, -0.5, 1], [0.5, -0.5, -0.5, 1],
			[-0.5, 0.5, 0.5, 1], [0.5, 0.5, 0.5, 1], [-0.5, -0.5, 0.5, 1], [0.5, -0.5, 0.5, 1]
	]
	cube = matTrans(cube)
	cube = mapper.worldToViewport(cube)
	boxes.append(buildBox(cube))

	octa = [
		[0.5, 0, 0, 1], [0, -0.5, 0, 1], [-0.5, 0, 0, 1], [0, 0.5, 0, 1], [0, 0, 0.5, 1], [0, 0, -0.5, 1]
	]
	octa = matTrans(octa)
	octa = mapper.worldToViewport(octa)
	boxes.append(buildBox(octa))

	dodec = [
		[-0.57735, -0.57735, 0.57735, 1], [0.934172, 0.356822, 0, 1], [0.934172, -0.356822, 0, 1], [-0.934172, 0.356822, 0, 1], [-0.934172, -0.356822, 0, 1],
		[0, 0.934172, 0.356822, 1], [0, 0.934172, -0.356822, 1], [0.356822, 0, -0.934172, 1], [-0.356822, 0, -0.934172, 1], [0, -0.934172, -0.356822, 1],
		[0, -0.934172, 0.356822, 1], [0.356822, 0, 0.934172, 1], [-0.356822, 0, 0.934172, 1], [0.57735, 0.57735, -0.57735, 1], [0.57735, 0.57735, 0.57735, 1],
		[-0.57735, 0.57735, -0.57735, 1], [-0.57735, 0.57735, 0.57735, 1], [0.57735, -0.57735, -0.57735, 1], [0.57735, -0.57735, 0.57735, 1], [-0.57735, -0.57735, -0.57735, 1] 
	]
	dodec = matTrans(dodec)
	dodec = mapper.worldToViewport(dodec)
	boxes.append(buildBox(dodec))

	ico = [ [0, -0.525731, 0.850651, 1], [0.850651, 0, 0.525731, 1], [0.850651, 0, -0.525731, 1], [-0.850651, 0, -0.525731, 1], 
		[-0.850651, 0, 0.525731, 1], [-0.525731, 0.850651, 0, 1], [0.525731, 0.850651, 0, 1], [0.525731, -0.850651, 0, 1],
		[-0.525731, -0.850651, 0, 1], [0, -0.525731, -0.850651, 1], [0, 0.525731, -0.850651, 1], [0, 0.525731, 0.850651, 1]	]
	ico = matTrans(ico)
	ico = mapper.worldToViewport(ico)
	boxes.append(buildBox(ico))

	ax = [[0, 0, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1], [0, 1, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1]]
	ax = matTrans(ax)
	ax = mapper.worldToViewport(ax)

	# counter-clockwise rotation about the X axis
	ROT_X = lambda x: matTrans([[1,0,0, 0],           [0,cos(x),-sin(x), 0], [0,sin(x),cos(x), 0], [0, 0, 0, 1] ])

	# counter-clockwise rotation about the Y axis
	ROT_Y = lambda y: matTrans([[cos(y),0,sin(y), 0], [0,1,0, 0],            [-sin(y),0,cos(y), 0], [0, 0, 0, 1]])

	# counter-clockwise rotation about the Z axis
	ROT_Z = lambda z: matTrans([[cos(z),-sin(z),0, 0], [sin(z),cos(z),0, 0], [0,0,1, 0], [0, 0, 0, 1]])

	eps = lambda d: pi/300 if (d>0) else -pi/300
	EPS = lambda d: d*pi/300

	lastX = 0 
	lastY = 0
	tetColor = 'black'
	bgColor = 'white'

def cbClicked(event):
    """Save current mouse position."""

    global lastX, lastY

    lastX = event.x
    lastY = event.y

def cbMottion(event):
	"""Map mouse displacements in Y direction to rotations about X axis,
		and mouse displacements in X direction to rotations about Y axis.""" 

	global tet
	global ax
	global boxes
	global cube
	global octa
	global dodec
	global ico
	global curPoly
	global activateAxes, activateBBox

	canvas.delete(ALL)
	# Y coordinate is upside down
	dx = lastY - event.y 
	dy = lastX - event.x

	
	# box = matMul(ROT_X(EPS(-dx)), box)
	# box = matMul(ROT_Y(EPS(-dy)), box)

	tet = matMul(ROT_X(EPS(dx)),tet)
	tet = matMul(ROT_Y(EPS(-dy)),tet)

	for i in range(len(boxes)):		
		boxes[i] = matMul(ROT_X(EPS(dx)), boxes[i])
		boxes[i] = matMul(ROT_Y(EPS(-dy)), boxes[i])

	ax = matMul(ROT_X(EPS(dx)), ax)
	ax = matMul(ROT_Y(EPS(-dy)), ax)
	

	cube = matMul(ROT_X(EPS(dx)),cube)
	cube = matMul(ROT_Y(EPS(-dy)), cube)

	octa = matMul(ROT_X(EPS(dx)), octa)
	octa = matMul(ROT_Y(EPS(-dy)), octa)

	dodec = matMul(ROT_X(EPS(dx)), dodec)
	dodec = matMul(ROT_Y(EPS(-dy)), dodec)

	ico = matMul(ROT_X(EPS(dx)), ico)
	ico = matMul(ROT_Y(EPS(-dy)), ico)
	
	if (curPoly == 'tet'):
		drawTet(tet,tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[0])
	elif (curPoly == 'cube'):
		drawCube(cube, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[1])
	elif (curPoly == 'octa'):
		drawOctahedron(octa, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[2])
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, tetColor)    
		if (activateBBox):
			drawBoundingBox(boxes[3])
	elif (curPoly == 'ico'):		
		drawIcosahedron(ico, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[4])

	if (activateAxes):
		drawAxes(ax)	
	
	
	cbClicked(event)   

def wheelUp(event):
	"""Map mouse wheel up displacements to rotations about Z axis."""

	global tet, cube, octa, dodec, ico
	global activateBBox, curPoly
	canvas.delete(ALL)
	tet = matMul(ROT_Z(EPS(-10)),tet)
	cube = matMul(ROT_Z(EPS(-10)), cube)
	octa = matMul(ROT_Z(EPS(-10)),octa)
	dodec = matMul(ROT_Z(EPS(-10)),dodec)
	ico = matMul(ROT_Z(EPS(-10)),ico)
	for i in range(len(boxes)):		
		boxes[i] = matMul(ROT_Z(EPS(-10)), boxes[i])
	if (curPoly == 'tet'):
		drawTet(tet,tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[0])
	elif (curPoly == 'cube'):
		drawCube(cube, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[1])
	elif (curPoly == 'octa'):
		drawOctahedron(octa, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[2])
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, tetColor)    
		if (activateBBox):
			drawBoundingBox(boxes[3])
	elif (curPoly == 'ico'):		
		drawIcosahedron(ico, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[4])

	if (activateAxes):
		drawAxes(ax)

def wheelDown(event):
	"""Map mouse wheel down displacements to rotations about Z axis."""

	global tet, cube, octa, dodec, ico
	global activateBBox, curPoly
	canvas.delete(ALL)
	tet = matMul(ROT_Z(EPS(10)),tet)
	cube = matMul(ROT_Z(EPS(10)), cube)
	octa = matMul(ROT_Z(EPS(10)),octa)
	dodec = matMul(ROT_Z(EPS(10)),dodec)
	ico = matMul(ROT_Z(EPS(10)),ico)
	for i in range(len(boxes)):		
		boxes[i] = matMul(ROT_Z(EPS(10)), boxes[i])	
	if (curPoly == 'tet'):
		drawTet(tet,tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[0])
	elif (curPoly == 'cube'):
		drawCube(cube, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[1])
	elif (curPoly == 'octa'):
		drawOctahedron(octa, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[2])
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, tetColor)    
		if (activateBBox):
			drawBoundingBox(boxes[3])
	elif (curPoly == 'ico'):		
		drawIcosahedron(ico, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[4])

	if (activateAxes):
		drawAxes(ax)

def wheel(event):
	"""Map mouse wheel displacements to rotations about Z axis."""

	global tet, cube, octa, dodec, ico
	global activateBBox, curPoly

	tet = matMul(ROT_Z(EPS(10)),tet)
	cube = matMul(ROT_Z(EPS(10)), cube)
	octa = matMul(ROT_Z(EPS(10)),octa)
	dodec = matMul(ROT_Z(EPS(10)),dodec)
	ico = matMul(ROT_Z(EPS(10)),ico)
	if (curPoly == 'tet'):
		drawTet(tet,tetColor)
	if (activateBBox):
		drawBoundingBox(boxes[0])
	elif (curPoly == 'cube'):
		drawCube(cube, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[1])
	elif (curPoly == 'octa'):
		drawOctahedron(octa, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[2])
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, tetColor)    
		if (activateBBox):
			drawBoundingBox(boxes[3])
	elif (curPoly == 'ico'):		
		drawIcosahedron(ico, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[4])

	if (activateAxes):
		drawAxes(ax)

def resize(event):
	"""Redraw the tetrahedron, in case of a window change due to user resizing it.""" 

	global tet, cube, octa, dodec, ico
	global activateBBox, curPoly
	canvas.delete(ALL)
	if (curPoly == 'tet'):
		drawTet(tet,tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[0])
	elif (curPoly == 'cube'):
		drawCube(cube, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[1])
	elif (curPoly == 'octa'):
		drawOctahedron(octa, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[2])
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, tetColor)    
		if (activateBBox):
			drawBoundingBox(boxes[3])
	elif (curPoly == 'ico'):		
		drawIcosahedron(ico, tetColor)
		if (activateBBox):
			drawBoundingBox(boxes[4])

	if (activateAxes):
		drawAxes(ax)

def drawAxes(ax):
	"""Draw the axes in center"""
	w = canvas.winfo_width()/2
	h = canvas.winfo_height()/2
	canvas.create_line(translate(ax[0][0], ax[1][0], w, h),
		translate(ax[0][1], ax[1][1], w, h), fill='red', width=2)

	canvas.create_line(translate(ax[0][2], ax[1][2], w, h),
		translate(ax[0][3], ax[1][3], w, h), fill='green', width=2)

	canvas.create_line(translate(ax[0][4], ax[1][4], w, h),
		translate(ax[0][5], ax[1][5], w, h), fill='blue', width=2)
  


def switch(polyhedron):
	global curPoly
	global tet, cube, octa, dodec, ico
	curPoly = polyhedron

	canvas.delete(ALL) # delete all edges

	if (curPoly == 'tet'):
		drawTet(tet, col='red')
	elif (curPoly == 'cube'):
		drawCube(cube, col='red')
	elif (curPoly == 'octa'):
		drawOctahedron(octa, col='red')
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, col='red')
	else:
		drawIcosahedron(ico, col='red')

def switchNormals():
	global normalsOn, curPoly
	global tetNormals, cubeNormals, octaNormals, dodecNormals, icoNormals
	normalsOn = not normalsOn
	if (curPoly == 'tet'):
		drawTet(tet, col='red')
	elif (curPoly == 'cube'):
		drawCube(cube, col='red')
	elif (curPoly == 'octa'):
		drawOctahedron(octa, col='red')
	elif (curPoly == 'dode'):
		drawDodecahedron(dodec, col='red')
	else:
		drawIcosahedron(ico, col='red')

def axes():
	global activateAxes, ax
	activateAxes = not activateAxes
	if (activateAxes):
		drawAxes(ax)

def boundingBox():
	global activateBBox
	activateBBox = not activateBBox		
		

def main1():
	global canvas
	root = Tk()
	root.title('Platonic')
	root.geometry('+0+0')

	init()
	
	canvas = Canvas(root, width=400, height=400, background=bgColor)
	canvas.pack(fill=BOTH,expand=YES)               
	canvas.bind("<Button-1>", cbClicked)
	canvas.bind("<B1-Motion>", cbMottion)
	canvas.bind("<Configure>", resize)
	
	from platform import uname
	os = uname()[0]
	if ( os == "Linux" ):
			canvas.bind('<Button-4>', wheelUp)      # X11
			canvas.bind('<Button-5>', wheelDown)
	elif ( os == "Darwin" ):
			canvas.bind('<MouseWheel>', wheel)      # MacOS
	else: 
			canvas.bind_all('<MouseWheel>', wheel)  # windows
	tet_b = Button(root, text="Tetrahedron", command=lambda: switch('tet'))
	tet_b.pack()

	cube_b = Button(root, text="Cube", command=lambda: switch('cube'))
	cube_b.pack()

	octa_b = Button(root, text="Octahedron", command=lambda: switch('octa'))
	octa_b.pack()

	dode_b = Button(root, text="Dodecahedron", command=lambda: switch('dode'))
	dode_b.pack()

	ico_b = Button(root, text="Icosahedron", command=lambda: switch('ico'))
	ico_b.pack()

	normals_b = Button(root, text="Switch Normals", command=switchNormals)
	normals_b.pack()

	axes_b = Button(root, text="Axes", command=axes)
	axes_b.pack()	
	boundingb_b = Button(root, text="Bounding Box", command=boundingBox)
	boundingb_b.pack()		
	mainloop()

if __name__=='__main__':
    sys.exit(main1())