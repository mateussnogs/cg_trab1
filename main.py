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

   
def drawTet(tet,col):
    # return
    """Draw a tetrahedron."""

    w = canvas.winfo_width()/2
    h = canvas.winfo_height()/2
    canvas.delete(ALL) # delete all edges
    nv = len(tet[0])   # number of vertices in tet (4)

    # draw the 6 edges of the tetrahedron
    
    # for p1 in range(nv):
    #     for p2 in range(p1+1,nv):       
    #         canvas.create_line(translate(tet[0][p1], tet[1][p1], w, h),
    #                            translate(tet[0][p2], tet[1][p2], w, h), fill = col)

    face1 = [tet[0][0], tet[1][0], tet[0][1], tet[1][1], tet[0][2], tet[1][2]]
    face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
    face2 = [tet[0][0], tet[1][0], tet[0][1], tet[1][1], tet[0][3], tet[1][3]]
    face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]

    face3 = [tet[0][0], tet[1][0], tet[0][2], tet[1][2], tet[0][3], tet[1][3]]
    face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]

    face4 = [tet[0][1], tet[1][1], tet[0][2], tet[1][2], tet[0][3], tet[1][3]]
    face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]

    canvas.create_polygon(face1, outline='red',
                fill='blue', width=2)
    canvas.create_polygon(face2, outline='yellow',
                fill='green', width=2)
    canvas.create_polygon(face3, outline='orange',
                fill='black', width=2)
    canvas.create_polygon(face4, outline='green',
                fill='grey', width=2)  


def drawCube(cube, col):
    w = canvas.winfo_width()/2
    h = canvas.winfo_height()/2
    canvas.delete(ALL) # delete all edges
    nv = len(cube[0])   # number of vertices in cube (8)

    # draw the 6 faces of the tetrahedron
    face1 = [
    	cube[0][0], cube[1][0], 
        cube[0][1], cube[1][1],
        cube[0][3], cube[1][3],
        cube[0][2], cube[1][2],
        cube[0][0], cube[1][0]
       ]
    face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]
    face2 = [
    	cube[0][1], cube[1][1],
        cube[0][5], cube[1][5], 
        cube[0][7], cube[1][7],
        cube[0][3], cube[1][3],
        cube[0][1], cube[1][1] 
    ]
    face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]
    face3 = [
    	cube[0][0], cube[1][0],
        cube[0][4], cube[1][4], 
        cube[0][6], cube[1][6],
        cube[0][2], cube[1][2],
        cube[0][0], cube[1][0] 
    ]
    face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]
    face4 = [
    	cube[0][0], cube[1][0],
        cube[0][1], cube[1][1], 
        cube[0][5], cube[1][5],
        cube[0][4], cube[1][4],
        cube[0][0], cube[1][0] 
	]	
    face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]
    face5 = [
    	cube[0][2], cube[1][2],
	    cube[0][3], cube[1][3], 
	    cube[0][7], cube[1][7],
	    cube[0][6], cube[1][6],
	    cube[0][2], cube[1][2]
	]	
    face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]
    face6 = [
    	cube[0][4], cube[1][4],
        cube[0][5], cube[1][5], 
        cube[0][7], cube[1][7],
        cube[0][6], cube[1][6],
        cube[0][4], cube[1][4]
	]	
    face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]

    canvas.create_polygon(face1, outline='red',
                fill='blue', width=2)
    canvas.create_polygon(face2, outline='yellow',
                fill='green', width=2)
    canvas.create_polygon(face3, outline='yellow',
                fill='red', width=2)
    canvas.create_polygon(face4, outline='yellow',
                fill='black', width=2)
    canvas.create_polygon(face5, outline='yellow',
                fill='yellow', width=2)
    canvas.create_polygon(face6, outline='yellow',
                fill='orange', width=2)


def drawOctahedron(octa, col):
    w = canvas.winfo_width()/2
    h = canvas.winfo_height()/2
    canvas.delete(ALL) # delete all edges
    face1 = [
    	octa[0][4], octa[1][4], octa[0][0], octa[1][0], octa[0][1], octa[1][1], octa[0][4], octa[1][4]
    ]
    face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]

    face2 = [
    	octa[0][4], octa[1][4], octa[0][1], octa[1][1], octa[0][2], octa[1][2], octa[0][4], octa[1][4]
    ]
    face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]

    face3 = [
		octa[0][4], octa[1][4], octa[0][2], octa[1][2], octa[0][3], octa[1][3], octa[0][4], octa[1][4]
    ]
    face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]

    face4 = [
		octa[0][4], octa[1][4], octa[0][3], octa[1][3], octa[0][0], octa[1][0], octa[0][4], octa[1][4]
    ]
    face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]

    face5 = [
		octa[0][5], octa[1][5], octa[0][1], octa[1][1], octa[0][0], octa[1][0], octa[0][5], octa[1][5]
    ]
    face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]

    face6 = [
		octa[0][5], octa[1][5], octa[0][2], octa[1][2], octa[0][1], octa[1][1], octa[0][5], octa[1][5]
    ]
    face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]    

    face7 = [
		octa[0][5], octa[1][5], octa[0][3], octa[1][3], octa[0][2], octa[1][2], octa[0][5], octa[1][5]
    ]
    face7 = [translate(face7[i], face7[i+1], w, h) for i in range(0, len(face7), 2)]
    face8 = [
		octa[0][5], octa[1][5], octa[0][0], octa[1][0], octa[0][3], octa[1][3], octa[0][5], octa[1][5]
    ]
    face8 = [translate(face8[i], face8[i+1], w, h) for i in range(0, len(face8), 2)]          
    canvas.create_polygon(face1, outline='red',
                fill='blue', width=2)
    canvas.create_polygon(face2, outline='red',
                fill='green', width=2)
    canvas.create_polygon(face3, outline='red',
                fill='red', width=2)
    canvas.create_polygon(face4, outline='red',
                fill='yellow', width=2)
    canvas.create_polygon(face5, outline='red',
                fill='black', width=2)
    canvas.create_polygon(face6, outline='red',
                fill='gray', width=2)
    canvas.create_polygon(face7, outline='red',
                fill='orange', width=2)
    canvas.create_polygon(face8, outline='red',
                fill='pink', width=2)
    
def drawDodecahedron(dodec, col):
    w = canvas.winfo_width()/2
    h = canvas.winfo_height()/2
    canvas.delete(ALL) # delete all edges

    face1 = [
    	dodec[0][1], dodec[1][1], dodec[0][2], dodec[1][2], dodec[0][18], dodec[1][18], dodec[0][11], dodec[1][11], dodec[0][14], dodec[1][14], dodec[0][1], dodec[1][1] 
    ]        
    face1 = [translate(face1[i], face1[i+1], w, h) for i in range(0, len(face1), 2)]

    face2 = [
		dodec[0][1], dodec[1][1], dodec[0][13], dodec[1][13], dodec[0][7], dodec[1][7], dodec[0][17], dodec[1][17], dodec[0][2], dodec[1][2], dodec[0][1], dodec[1][1] 
	]        
    face2 = [translate(face2[i], face2[i+1], w, h) for i in range(0, len(face2), 2)]

    face3 = [
		dodec[0][3], dodec[1][3], dodec[0][4], dodec[1][4], dodec[0][19], dodec[1][19], dodec[0][8], dodec[1][8], dodec[0][15], dodec[1][15], dodec[0][3], dodec[1][3] 
	]        
    face3 = [translate(face3[i], face3[i+1], w, h) for i in range(0, len(face3), 2)]

    face4 = [
		dodec[0][3], dodec[1][3], dodec[0][16], dodec[1][16], dodec[0][12], dodec[1][12], dodec[0][0], dodec[1][0], dodec[0][4], dodec[1][4], dodec[0][3], dodec[1][3] 
	]        
    face4 = [translate(face4[i], face4[i+1], w, h) for i in range(0, len(face4), 2)]

    face5 = [
		dodec[0][3], dodec[1][3], dodec[0][15], dodec[1][15], dodec[0][6], dodec[1][6], dodec[0][5], dodec[1][5], dodec[0][16], dodec[1][16], dodec[0][3], dodec[1][3] 
	]        
    face5 = [translate(face5[i], face5[i+1], w, h) for i in range(0, len(face5), 2)]                   

    face6 = [
		dodec[0][1], dodec[1][1], dodec[0][14], dodec[1][14], dodec[0][5], dodec[1][5], dodec[0][6], dodec[1][6], dodec[0][13], dodec[1][13], dodec[0][1], dodec[1][1] 
	]        
    face6 = [translate(face6[i], face6[i+1], w, h) for i in range(0, len(face6), 2)]     

    face7 = [
		dodec[0][2], dodec[1][2], dodec[0][17], dodec[1][17], dodec[0][9], dodec[1][9], dodec[0][10], dodec[1][10], dodec[0][18], dodec[1][18], dodec[0][2], dodec[1][2] 
	]        
    face7 = [translate(face7[i], face7[i+1], w, h) for i in range(0, len(face7), 2)] 

    face8 = [
		dodec[0][4], dodec[1][4], dodec[0][0], dodec[1][0], dodec[0][10], dodec[1][10], dodec[0][9], dodec[1][9], dodec[0][19], dodec[1][19], dodec[0][4], dodec[1][4] 
	]        
    face8 = [translate(face8[i], face8[i+1], w, h) for i in range(0, len(face8), 2)]

    face9 = [
		dodec[0][7], dodec[1][7], dodec[0][8], dodec[1][8], dodec[0][19], dodec[1][19], dodec[0][9], dodec[1][9], dodec[0][17], dodec[1][17], dodec[0][7], dodec[1][7] 
	]        
    face9 = [translate(face9[i], face9[i+1], w, h) for i in range(0, len(face9), 2)]

    face10 = [
		dodec[0][6], dodec[1][6], dodec[0][15], dodec[1][15], dodec[0][8], dodec[1][8], dodec[0][7], dodec[1][7], dodec[0][13], dodec[1][13], dodec[0][6], dodec[1][6] 
	]        
    face10 = [translate(face10[i], face10[i+1], w, h) for i in range(0, len(face10), 2)]

    face11 = [
		dodec[0][5], dodec[1][5], dodec[0][14], dodec[1][14], dodec[0][11], dodec[1][11], dodec[0][12], dodec[1][12], dodec[0][16], dodec[1][16], dodec[0][5], dodec[1][5] 
	]        
    face11 = [translate(face11[i], face11[i+1], w, h) for i in range(0, len(face11), 2)]   

    face12 = [
		dodec[0][10], dodec[1][10], dodec[0][0], dodec[1][0], dodec[0][12], dodec[1][12], dodec[0][11], dodec[1][11], dodec[0][18], dodec[1][18], dodec[0][10], dodec[1][10] 
	]        
    face12 = [translate(face12[i], face12[i+1], w, h) for i in range(0, len(face12), 2)]                  
    canvas.create_polygon(face1, outline='red',
                fill='blue', width=1)
    canvas.create_polygon(face2, outline='red',
                fill='green', width=1)
    canvas.create_polygon(face3, outline='red',
                fill='yellow', width=1)
    canvas.create_polygon(face4, outline='red',
                fill='red', width=1)
    canvas.create_polygon(face5, outline='red',
                fill='gold', width=1)
    canvas.create_polygon(face6, outline='red',
                fill='medium turquoise', width=1)   
    canvas.create_polygon(face7, outline='red',
                fill='sea green', width=1)                               
    canvas.create_polygon(face8, outline='red',
                fill='dark olive green', width=1)                               
    canvas.create_polygon(face9, outline='red',
                fill='DarkOrchid1', width=1)
    canvas.create_polygon(face10, outline='red',
                fill='SteelBlue4', width=1)
    canvas.create_polygon(face11, outline='red',
                fill='dark green', width=1)  
    canvas.create_polygon(face12, outline='red',
                fill='indian red', width=1)                                                                                     
    

def normalSurface(solid, vertexes):
	normal = [0, 0, 0]
	nv = len(polygon)
	for i in range(nv):
		x, y, z = polygon[i], polygon[i+1], polygon[i+2]

                
def init():
    """Initialize global variables."""

    global ROT_X, ROT_Y, ROT_Z
    global eps, EPS, tet, ax, box, cube, octa, dodec
    global lastX, lastY, tetColor, bgColor
    # global mapp

    # mapp = Mapper([-1, -1, 1, 1], [-200, -200, 200, 200])
    # tet = [[0, 0.8, 0], [-0.8, -0.8, 0], [0.8, -0.8, 0], [0, 0, 2]]
    # tet = mapp.windowToViewport(tet[0], tet[1], tet[2], tet[3])
    # tet = [tet[i]+(0,) if i < 3 else tet[i]+(200,) for i in range(0, len(tet))]
    # tet = matTrans(tet)
    # tet = matTrans([[0,-100,0],[-100,100,0],[100,100,0],[0,0,200]])

    mapper = AffineMapper([-1, -1, -1, 1, 1, 1], [-200, -200, -200, 200, 200, 200])

    tet = [[0, 0.5, 0, 1], [-0.5, -0.5, 0, 1], [0.5, -0.5, 0, 1], [0, 0, 0.5, 1]]
    tet = matTrans(tet)
    tet = mapper.worldToViewport(tet)

    cube = [
         [-0.5, 0.5, -0.5, 1], [0.5, 0.5, -0.5, 1], [-0.5, -0.5, -0.5, 1], [0.5, -0.5, -0.5, 1],
         [-0.5, 0.5, 0.5, 1], [0.5, 0.5, 0.5, 1], [-0.5, -0.5, 0.5, 1], [0.5, -0.5, 0.5, 1]
    ]
    cube = matTrans(cube)
    cube = mapper.worldToViewport(cube)

    octa = [
    	[0.5, 0, 0, 1], [0, -0.5, 0, 1], [-0.5, 0, 0, 1], [0, 0.5, 0, 1], [0, 0, 0.5, 1], [0, 0, -0.5, 1]
    ]
    octa = matTrans(octa)
    octa = mapper.worldToViewport(octa)

    dodec = [
    	[-0.57735, -0.57735, 0.57735, 1], [0.934172, 0.356822, 0, 1], [0.934172, -0.356822, 0, 1], [-0.934172, 0.356822, 0, 1], [-0.934172, -0.356822, 0, 1],
    	[0, 0.934172, 0.356822, 1], [0, 0.934172, -0.356822, 1], [0.356822, 0, -0.934172, 1], [-0.356822, 0, -0.934172, 1], [0, -0.934172, -0.356822, 1],
    	[0, -0.934172, 0.356822, 1], [0.356822, 0, 0.934172, 1], [-0.356822, 0, 0.934172, 1], [0.57735, 0.57735, -0.57735, 1], [0.57735, 0.57735, 0.57735, 1],
    	[-0.57735, 0.57735, -0.57735, 1], [-0.57735, 0.57735, 0.57735, 1], [0.57735, -0.57735, -0.57735, 1], [0.57735, -0.57735, 0.57735, 1], [-0.57735, -0.57735, -0.57735, 1] 
    ]
    dodec = matTrans(dodec)
    dodec = mapper.worldToViewport(dodec)

    ax = [[0, 0, 0], [0, -100, 0], [0, 0, 0], [100, 0, 0], [0, 0, 0], [0, 0, 100]]
    ax = matTrans(ax)
    
    # a = 200 y aumenta pra baixo
    box = [[-100, -100, 100], [100, -100, 100], [-100, -100, -100], [100, -100, -100],
           [-100, 100, 100], [100, 100, 100], [-100, 100, -100], [100, 100, -100] ]
    box = matTrans(box)

    # counter-clockwise rotation about the X axis
    ROT_X = lambda x: matTrans([[1,0,0, 0],           [0,cos(x),-sin(x), 0], [0,sin(x),cos(x), 0], [0, 0, 0, 1] ])

    # counter-clockwise rotation about the Y axis
    ROT_Y = lambda y: matTrans([[cos(y),0,sin(y), 0], [0,1,0, 0],            [-sin(y),0,cos(y), 0], [0, 0, 0, 1]])

    # counter-clockwise rotation about the Z axis
    ROT_Z = lambda z: matTrans([[cos(z),sin(z),0, 0], [-sin(z),cos(z),0, 0], [0,0,1, 0], [0, 0, 0, 1]])

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
    global box
    global cube
    global octa
    global dodec

    canvas.delete(ALL)
    # Y coordinate is upside down
    dx = lastY - event.y 
    tet = matMul(ROT_X(EPS(-dx)),tet)
    ax = matMul(ROT_X(EPS(-dx)), ax)
    box = matMul(ROT_X(EPS(-dx)), box)
    dy = lastX - event.x
    tet = matMul(ROT_Y(EPS(dy)),tet)
    ax = matMul(ROT_Y(EPS(-dy)), ax)
    # drawTet(tet,tetColor)  
    box = matMul(ROT_Y(EPS(-dy)), box)
    cube = matMul(ROT_X(EPS(-dx)),cube)
    cube = matMul(ROT_Y(EPS(-dy)), cube)
    octa = matMul(ROT_X(EPS(-dx)), octa)
    octa = matMul(ROT_Y(EPS(-dy)), octa)
    dodec = matMul(ROT_X(EPS(-dx)), dodec)
    dodec = matMul(ROT_Y(EPS(-dy)), dodec)
    drawDodecahedron(dodec, tetColor)    
    # drawOctahedron(octa, tetColor)
    # drawCube(cube, tetColor)
    # drawBox(box, tetColor)  
    # drawAxes(event)
    # canvas.create_line(translate(ax[0][0], ax[1][0], 200, 200), 
    #     translate(ax[0][1], ax[1][1], 200, 200), fill='red', width=2)
    # canvas.create_line(translate(ax[0][2], ax[1][2], 200, 200),
    #  translate(ax[0][3], ax[1][3], 200, 200), fill='green', width=2)
    
    # canvas.create_line(translate(ax[0][4], ax[1][4], 200, 200),
    #  translate(ax[0][5], ax[1][5], 200, 200), fill='blue', width=2)
    cbClicked(event)   

def wheelUp(event):
    """Map mouse wheel up displacements to rotations about Z axis."""

    global tet
    tet = matMul(ROT_Z(EPS(1)),tet)
    drawTet(tet,tetColor)

def wheelDown(event):
    """Map mouse wheel down displacements to rotations about Z axis."""

    global tet
    tet = matMul(ROT_Z(EPS(-1)),tet)
    drawTet(tet,tetColor)

def wheel(event):
    """Map mouse wheel displacements to rotations about Z axis."""

    global tet
    tet = matMul(ROT_Z(EPS(event.delta/120)),tet)
    drawTet(tet,tetColor)

def resize(event):
    """Redraw the tetrahedron, in case of a window change due to user resizing it.""" 

    # drawTet(tet,tetColor)

def drawAxes(event):
    """Draw the axes in center"""
    canvas.create_line(translate(ax[0][0], ax[1][0], 200, 200),
     translate(ax[0][1], ax[1][1], 200, 200), fill='red', width=2)

    canvas.create_line(translate(ax[0][2], ax[1][2], 200, 200),
     translate(ax[0][3], ax[1][3], 200, 200), fill='green', width=2)
    
    canvas.create_line(translate(ax[0][4], ax[1][4], 200, 200),
     translate(ax[0][5], ax[1][5], 200, 200), fill='blue', width=2)

def drawBox(box, col):
    """Draw bounding box"""

    nv = len(box[0]) # number of vertices (of cube (8)
    # draw the 12 edges of the cube
    
    for p1 in range(nv):
        for p2 in range(p1+1,nv):
            s = sum([abs(box[i][p2] - box[i][p1]) for i in range(len(box))])
            if(s < 345):
                canvas.create_line(translate(box[0][p1], box[1][p1], 200, 200),
                            translate(box[0][p2], box[1][p2], 200, 200), fill = col)
    


                
def main():
    global canvas
    root = Tk()
    root.title('Tetrahedron')
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
    canvas.master.bind('<x>', drawAxes)
    # drawTet(tet,tetColor)
    # drawBox(box, tetColor)
    drawCube(cube, tetColor)
    mainloop()

if __name__=='__main__':
    sys.exit(main())