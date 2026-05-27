import calcualtions as cs
import numpy as np


class Crystal:
    def __init__(self, name, c11, c12, c44, pv, saved=False, calculated=False):
        self.name = name
        self.c1 = c11
        self.c2 = c12
        self.c4 = c44
        self.p = pv
        self.saved = saved
        self.calculated = calculated

    def __eq__(self, other):
        return self.c1 == other.c1 and self.c2 == other.c2 and self.c4 == other.c4 and self.p == other.p

    def append_speed_values(self, values):
        appended = values + values[::-1]
        appended = appended + appended[::]
        return appended

    def append_group_speed(self, vector, opt=False):
        vector[0] = vector[0] + vector[0][::-1]
        vector[0] = vector[0] + [x * (-1) for x in vector[0]]
        if opt:
            vector[1] = vector[0]
        vector[2] = vector[2] + [x * (-1) for x in vector[2][::-1]]
        vector[2] = vector[2] + vector[2][::-1]

    def append_data(self):
        self.t1[3] = self.append_speed_values(self.t1[3])
        self.t2[3] = self.append_speed_values(self.t2[3])
        self.t1d[3] = self.append_speed_values(self.t1d[3])
        self.t2d[3] = self.append_speed_values(self.t2d[3])
        self.append_group_speed(self.t1)
        self.append_group_speed(self.t2)
        self.append_group_speed(self.t1d, True)
        self.append_group_speed(self.t2d, True)

    def load_data(self, t1, t2, t1d, t2d, t1c, t2c):
        self.t1 = t1
        self.t2 = t2
        self.t1d = t1d
        self.t2d = t2d
        self.t1c = t1c
        self.t2c = t2c
        self.t13d = cs.get_iso_surface3d(np.pi * (-2) / 3)
        self.t23d = cs.get_iso_surface3d(np.pi * (2) / 3)
        self.calculated = True
        self.append_data()

    def calculate(self):
        cs.load_constants(self.c1, self.c2, self.c4, self.p, 1)
        self.t1 = cs.get_values(0, np.pi * (-2) / 3)
        self.t2 = cs.get_values(0, np.pi * (2) / 3)
        self.t1d = cs.get_values(np.pi / 4, np.pi * (-2) / 3)
        self.t2d = cs.get_values(np.pi / 4, np.pi * (2) / 3)
        self.t1c = cs.get_caustic(np.pi * (-2) / 3)
        self.t2c = cs.get_caustic(np.pi * (2) / 3)
        self.t13d = cs.get_iso_surface3d(np.pi * (-2) / 3)
        self.t23d = cs.get_iso_surface3d(np.pi * (2) / 3)
        self.calculated = True
        self.saved = False
        self.append_data()

