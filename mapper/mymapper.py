import sys
sys.path.append('../')
from matrix.ops import *
class AffineMapper:
    def __init__(self, world, viewport):
        self.world = world
        self.viewport = viewport
        x_min, y_min, z_min, x_max, y_max, z_max = self.world[:6]
        X_min, Y_min, Z_min, X_max, Y_max, Z_max = self.viewport[:6]
        self.sx = float(X_max-X_min) / float(x_max-x_min)
        self.sy = float(Y_max-Y_min) / float(y_max-y_min)
        self.sz = float(Z_max-Z_min) / float(z_max-z_min)
        self.tx = (float(X_min*x_max)-float(X_max*x_min)) / (x_max-x_min)
        self.ty = (float(Y_min*y_max)-float(Y_max*y_min)) / (y_max-y_min)
        self.tz = (float(Z_min*z_max)-float(Z_max*z_min)) / (z_max-z_min)

        self.t = [[self.sx, 0, 0, self.tx], [0, self.sy, 0, self.ty], [0, 0, self.sz, self.tz], [0, 0, 0, 1]]


    def worldToViewport(self, w):
        # return [matMul(self.t, [w[i]]) for i in range(len(w))]
        return matMul(self.t, w)




def main():
    mapper = AffineMapper([-1, -1, -1, 1, 1, 1], [-100, -100, -100, 100, 100, 100])
    tet = [[0,-1, 0, 1],[-1, 1, 0, 1],[1, 1, 0, 1],[0, 0, 2, 1]]
    tetT = mapper.worldToViewport(tet)
    print(tetT)


if __name__ == "__main__":
   sys.exit(main())