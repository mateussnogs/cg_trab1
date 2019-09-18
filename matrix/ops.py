from math import sqrt 

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

def vecDif(m1, m2):
    m = [0]*3
    for i in range(3):
        m[i] = m1[i] - m2[i]
    return m

def vecLength(v):
    return sqrt(v[0]**2 + v[1]**2 + v[2]**2)