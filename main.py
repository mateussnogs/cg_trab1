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

def createZeroMat(m,n):
    """Return a matrix (m x n) filled with zeros."""

    ret = [0] * m
    for i in range(m):
        ret[i] = [0] * n
    return ret   

def matMul(mat1, mat2):
    """Return mat1 x mat2 (mat1 multiplied by mat2)."""

    m = len(mat1)
    n = len(mat2[0])
    common = len(mat2)
   
    ret = createZeroMat(m,n)
    if  len(mat1[0]) == len(mat2):
      for i in range(m):
          for j in range(n):
              for k in range(common):
                  ret[i][j] += mat1[i][k] * mat2[k][j]
    return ret

def matTrans(mat):
    """Return mat (n x m) transposed (m x n)."""

    m = len(mat[0])
    n = len(mat)

    ret = createZeroMat(m,n)
    for i in range(m):
        for j in range(n):
            ret[i][j] = mat[j][i]
    return ret

def translate(x,y,dx,dy):
    """Translate vector(x,y) by (dx,dy)."""

    return x+dx, y+dy
   
def drawTet(tet,col):
    # return
    """Draw a tetrahedron."""

    w = canvas.winfo_width()/2
    h = canvas.winfo_height()/2
    canvas.delete(ALL) # delete all edges
    nv = len(tet[0])   # number of vertices in tet (4)

    # draw the 6 edges of the tetrahedron
    
    for p1 in range(nv):
        for p2 in range(p1+1,nv):       
            canvas.create_line(translate(tet[0][p1], tet[1][p1], w, h),
                               translate(tet[0][p2], tet[1][p2], w, h), fill = col)

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
    # canvas.create_polygon(face3, outline='orange',
    #             fill='black', width=2)
    canvas.create_polygon(face4, outline='green',
                fill='grey', width=2)            
                
def init():
    """Initialize global variables."""

    global ROT_X, ROT_Y, ROT_Z
    global eps, EPS, tet, ax, box
    global lastX, lastY, tetColor, bgColor
    global mapp

    mapp = Mapper([-1, -1, 1, 1], [-200, -200, 200, 200])
    tet = [[0, 0.8, 0], [-0.8, -0.8, 0], [0.8, -0.8, 0], [0, 0, 2]]
    tet = mapp.windowToViewport(tet[0], tet[1], tet[2], tet[3])
    tet = [tet[i]+(0,) if i < 3 else tet[i]+(200,) for i in range(0, len(tet))]
    tet = matTrans(tet)
    # tet = matTrans([[0,-100,0],[-100,100,0],[100,100,0],[0,0,200]])


    ax = [[0, 0, 0], [0, -100, 0], [0, 0, 0], [100, 0, 0], [0, 0, 0], [0, 0, 100]]
    ax = matTrans(ax)
    
    # a = 200 y aumenta pra baixo
    box = [[-100, -100, 100], [100, -100, 100], [-100, -100, -100], [100, -100, -100],
           [-100, 100, 100], [100, 100, 100], [-100, 100, -100], [100, 100, -100] ]
    box = matTrans(box)

    # counter-clockwise rotation about the X axis
    ROT_X = lambda x: matTrans([[1,0,0],           [0,cos(x),-sin(x)], [0,sin(x),cos(x)] ])

    # counter-clockwise rotation about the Y axis
    ROT_Y = lambda y: matTrans([[cos(y),0,sin(y)], [0,1,0],            [-sin(y),0,cos(y)]])

    # counter-clockwise rotation about the Z axis
    ROT_Z = lambda z: matTrans([[cos(z),sin(z),0], [-sin(z),cos(z),0], [0,0,1]])

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

    canvas.delete(ALL)
    # Y coordinate is upside down
    dx = lastY - event.y 
    tet = matMul(ROT_X(EPS(-dx)),tet)
    ax = matMul(ROT_X(EPS(-dx)), ax)
    box = matMul(ROT_X(EPS(-dx)), box)
    dy = lastX - event.x
    tet = matMul(ROT_Y(EPS(dy)),tet)
    ax = matMul(ROT_Y(EPS(-dy)), ax)
    drawTet(tet,tetColor)  
    box = matMul(ROT_Y(EPS(-dy)), box)
    drawBox(box, tetColor)  
    # drawAxes(event)
    canvas.create_line(translate(ax[0][0], ax[1][0], 200, 200), 
        translate(ax[0][1], ax[1][1], 200, 200), fill='red', width=2)
    canvas.create_line(translate(ax[0][2], ax[1][2], 200, 200),
     translate(ax[0][3], ax[1][3], 200, 200), fill='green', width=2)
    
    canvas.create_line(translate(ax[0][4], ax[1][4], 200, 200),
     translate(ax[0][5], ax[1][5], 200, 200), fill='blue', width=2)
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

    drawTet(tet,tetColor)

def drawAxes(event):
    """Draw the axes in center"""
    global ax       
    canvas.create_line(translate(ax[0][0], ax[1][0], 200, 200),
     translate(ax[0][1], ax[1][1], 200, 200), fill='red', width=2)

    canvas.create_line(translate(ax[0][2], ax[1][2], 200, 200),
     translate(ax[0][3], ax[1][3], 200, 200), fill='green', width=2)
    
    canvas.create_line(translate(ax[0][4], ax[1][4], 200, 200),
     translate(ax[0][5], ax[1][5], 200, 200), fill='blue', width=2)

def drawBox(box, col):
    """Draw bounding box"""

    nv = len(box[0]) # number of vertices of cube (8)
    # draw the 12 edges of the cube
    
    for p1 in range(nv):
        for p2 in range(p1+1,nv):       
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
    drawBox(box, tetColor)
    mainloop()

if __name__=='__main__':
    sys.exit(main())