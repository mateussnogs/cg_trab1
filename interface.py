import sys
from main import *
try:
   from tkinter import *     # python 3
except ImportError:
   from Tkinter import *     # python 2

def initTetrahedron():
    main1()

def main():
    global canvas
    root = Tk()
    root.title('Platonic')
    root.geometry('+0+0')
    bgColor = 'white'

    canvas = Canvas(root, width=400, height=400, background=bgColor)
    canvas.pack(fill=BOTH,expand=YES)               
    # canvas.bind("<Button-1>", cbClicked)
    # canvas.bind("<B1-Motion>", cbMottion)
    # canvas.bind("<Configure>", resize)
    
    from platform import uname
    os = uname()[0]
    # if ( os == "Linux" ):
    #      canvas.bind('<Button-4>', wheelUp)      # X11
    #      canvas.bind('<Button-5>', wheelDown)
    # elif ( os == "Darwin" ):
    #      canvas.bind('<MouseWheel>', wheel)      # MacOS
    # else: 
    #      canvas.bind_all('<MouseWheel>', wheel)  # windows
    b = Button(root, text="Tetrahedron", command=initTetrahedron)
    b.pack()
    mainloop()

if __name__=='__main__':
    sys.exit(main())