import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import *

c11 = 167.7
c44 = 80.4
pv = 2.3301
kv = 1.67
wv = 1

x, y, k, c1, c4, p, t = sp.symbols('x y k c1 c4 p t')
n1 = sp.sin(x) * sp.cos(y)
n2 = sp.sin(x) * sp.sin(y)
n3 = sp.cos(x)
# epsi = n1 ** 2 * n2 ** 2 + n1 ** 2 * n3 ** 2 + n2 ** 2 * n3 ** 2
# nu = n1 ** 2 * n2 ** 2 * n3 ** 2
# r = sp.sqrt(1 + 3 * (k ** 2 - 1) * epsi)
# q = sp.acos((1 + 4.5 * (k ** 2 - 1) * epsi + 13.5 * nu * (1 - 3 * k ** 2 + 2 * k ** 3)) / r ** 3)
# z = (2 * r * sp.cos(q / 3 + t)) / 3
#Sp = sp.sqrt((c4 * (1 + ((c1 - c4) * (1 / 3 + z)) / c4)) / p)
simp_sp = sp.sqrt(3) * sp.sqrt((3 * c4 + (c1 - c4) * (2 * sp.sqrt((3 * k ** 2 - 3) * (
            -(1 - sp.cos(x) ** 2) ** 2 * (1 - sp.cos(y) ** 2) ** 2 - (1 - sp.cos(x) ** 2) ** 2 * sp.cos(
        y) ** 2 - sp.cos(x) ** 2 + 1) + 1) * sp.cos(t + sp.acos(((4.5 - 4.5 * k ** 2) * (
            sp.sin(x) ** 4 * sp.sin(y) ** 4 + sp.sin(x) ** 4 * sp.cos(y) ** 2 + sp.cos(x) ** 2 - 1) + (
                                                                             27.0 * k ** 3 - 40.5 * k ** 2 + 13.5) * sp.sin(
    x) ** 4 * sp.sin(y) ** 2 * sp.cos(x) ** 2 * sp.cos(y) ** 2 + 1) / ((3 - 3 * k ** 2) * (
            sp.sin(x) ** 4 * sp.sin(y) ** 4 + sp.sin(x) ** 4 * sp.cos(y) ** 2 + sp.cos(x) ** 2 - 1) + 1) ** (
                                                                            3 / 2)) / 3) + 1.0)) / p) / 3
difx_sp = sp.diff(simp_sp, x)
dify_sp = sp.diff(simp_sp, y)
diffxx_sp = sp.diff(difx_sp, x)
diffxy_sp = sp.diff(difx_sp, y)
diffyy_sp = sp.diff(dify_sp, y)
n = sp.Matrix([sp.sin(x) * sp.cos(y), sp.sin(x) * sp.sin(y), sp.cos(x)])
e_t = sp.Matrix([sp.cos(x) * sp.cos(y), sp.cos(x) * sp.sin(y), (-1) * sp.sin(x)])
e_p = sp.Matrix([(-1) * sp.sin(y), sp.cos(y), 0])
e_pp = sp.Matrix([(-1) * sp.cos(y), (-1) * sp.sin(y), 0])
e_tp = sp.cos(x) * e_p
ex1 = sp.cos(x) * sp.cos(y)
ex2 = sp.cos(x) * sp.sin(y)
ex3 = (-1) * sp.sin(x)
ey1 = (-1) * sp.sin(y)
ey2 = sp.cos(y)
ey3 = 0


def load_constants(a, b, c, d, e):
    global c11, c44, pv, kv, wv
    c11 = round(a * 100, 2)
    c44 = round(c * 100, 2)
    pv = round(d, 4)
    kv = round(1 + (b + 2 * c - a) / (a - c), 3)
    wv = round(e, 4)
    arguments = {c1: c11, c4: c44, p: pv, k: kv}


def get_speed(radians, move, opt=0):
    dist = []
    for rad in radians:
        res = simp_sp.subs({x: rad, y: move, k: kv, c1: c11, c4: c44, p: pv, t: opt})
        dist.append(res)
    return dist


def get_iso_surface(radians, move, opt=0):
    dist = []
    for rad in radians:
        res = simp_sp.subs({x: rad, y: move, k: kv, c1: c11, c4: c44, p: pv, t: opt})
        dist.append(1 / res)
    return dist


def show_phase_speed():
    theta = np.linspace(0, np.pi / 2, 90)
    plt.polar(theta, get_speed(theta, 0), label='L')
    plt.polar(theta, get_speed(theta, 0, np.pi * 2 / 3), label='t2')
    plt.legend(fontsize=10)
    plt.polar(theta, get_speed(theta, 0, np.pi * (-2) / 3), label='t1')
    plt.legend(fontsize=10)
    plt.polar(theta, get_speed(theta, sp.pi / 4), label='L')
    plt.polar(theta, get_speed(theta, np.pi / 4, sp.pi * 2 / 3), label='d2')
    plt.legend(fontsize=10)
    plt.polar(theta, get_speed(theta, np.pi / 4, sp.pi * (-2) / 3), label='d1')
    plt.legend(fontsize=10)
    plt.show()


#show_phase_speed()

def show_iso_surface():
    theta = np.linspace(0, np.pi / 2, 90)
    plt.polar(theta, get_iso_surface(theta, 0), label='L')
    plt.polar(theta, get_iso_surface(theta, 0, sp.pi * 2 / 3), label='t1')
    plt.polar(theta, get_iso_surface(theta, 0, sp.pi * (-2) / 3), label='t1')
    plt.legend()
    plt.show()


#show_iso_surface()

def get_v(radians, move, opt=0):
    v1 = []
    v2 = []
    v3 = []
    for rad in radians:
        arguments = {x: rad, y: move, k: kv, c1: c11, c4: c44, p: pv, t: opt}
        s = simp_sp.subs(arguments)
        sx = difx_sp.subs(arguments)
        sy = dify_sp.subs(arguments)
        v1.append(s * n1.subs({x: rad, y: move}) + sx * ex1.subs({x: rad, y: move})
                  + sy * ey1.subs({x: rad, y: move}) / sp.sin(rad))
        v2.append(s * n2.subs({x: rad, y: move}) + sx * ex2.subs({x: rad, y: move})
                  + sy * ey2.subs({x: rad, y: move}) / sp.sin(rad))
        v3.append(s * n3.subs({x: rad, y: move}) + sx * ex3.subs({x: rad, y: move}))
    return v1, v2, v3


def get_sTheta(move=0):
    radians = np.linspace(0, np.pi / 2, 90)
    st1 = []
    st2 = []
    arguments = {y: move, k: kv, c1: c11, c4: c44, p: pv}
    sx = difx_sp.subs(arguments)
    #sy = dify_sp.subs(arguments)
    for rad in radians:
        st1.append(sx.subs({x: rad, t: sp.pi * (-2) / 3}))
        st2.append(sx.subs({x: rad, t: sp.pi * (2) / 3}))
    return st1, st2


def show_Stheta():
    st1, st2 = get_sTheta()
    radians = np.linspace(0, np.pi / 2, 90)
    plt.plot(radians, st1)
    plt.plot(radians, st2)
    plt.show()


def show_group_speed():
    v1, v2, v3 = get_v(theta, 0, sp.pi * (-2) / 3)
    plt.plot(theta, v1, label='x')
    plt.plot(theta, v2, label='y')
    plt.plot(theta, v3, label='z')
    plt.legend()
    plt.title('Компоненты вектора групповой скорости Si\nпродольных волн в плоскости грани куба')
    plt.xlabel("Угол в радианах", fontsize=10, fontweight="bold")
    plt.ylabel("Групповая скорость ", fontsize=10, fontweight="bold")
    plt.show()


#show_group_speed()

def make_plot(x, y, label, xlabe, ylabe):
    plt.plot(x, y, label=label)
    plt.xlabel(xlabe, fontsize=10)
    plt.ylabel(ylabe, fontsize=10)
    plt.legend()


def show_group_speed_parametrized():
    get_v(theta, 0, sp.pi * (-2) / 3)
    plt.figure(figsize=(9, 9))
    plt.subplot(2, 2, 1)
    plt.title('Сечение волновой поверхности в пространстве\nгрупповых скоростей в плоскости грани', fontsize=10,
              fontweight="bold")
    make_plot(v1, v3, 't1', 'Vx', 'Vy')
    get_v(theta, 0, sp.pi * (2) / 3)
    plt.plot(v1, v3, label='t2')
    plt.legend()
    get_v(theta, sp.pi / 4, sp.pi * (-2) / 3)
    plt.subplot(2, 2, 2)
    plt.title('Сечение волновой поверхности в пространстве\nгрупповых скоростей в диагональной плоскости', fontsize=10,
              fontweight="bold")
    make_plot(v1, v3, 't1', 'Vx', 'Vy')
    plt.subplot(2, 2, 3)
    plt.title('((Vx(theta)+Vy(theta))/sqrt(2), Vz(theta)) для t1', fontsize=10, fontweight="bold")
    make_plot([x / sp.sqrt(2) for x in np.add(v1, v2)], v3, 't1', '', '')
    plt.subplot(2, 2, 2)
    get_v(theta, sp.pi / 4, sp.pi * (2) / 3)
    plt.plot(v1, v3, label='t2')
    plt.legend()
    plt.subplot(2, 2, 4)
    plt.title('((Vx(theta)+Vy(theta))/sqrt(2), Vz(theta)) для t2', fontsize=10, fontweight="bold")
    make_plot([x / sp.sqrt(2) for x in np.add(v1, v2)], v3, 't2', '', '')
    plt.show()


#show_group_speed_parametrized()

s_val = []
s_t_val = []
s_p_val = []
v_abs = []
s_tt_val = []
s_pp_val = []
s_tp_val = []
s, st, Sp, stt, stp, spp, v, k, w = sp.symbols('s st Sp stt stp spp v k w')
q = w / s
qtt = q * ((2 * st ** 2) / s - stt) / s
qtp = q * ((2 * Sp * st) / s - stp) / s
qp = (-1) * q * Sp / s
qt = (-1) * q * st / s
qpp = q * (2 * Sp ** 2 / s - spp) / s
n_v = (s * n + st * e_t + (Sp * e_p) / sp.sin(x)) / v
vq_tt = (qtt - q) * n + 2 * qt * e_t
vq_pp = qpp * n + 2 * qp * sp.sin(x) * e_p + sp.sin(x) * e_pp * q
vq_tp = qtp * n + qp * e_t + (qt * sp.sin(x) + sp.cos(x) * q) * e_p
L = vq_tt.dot(n_v)
M = vq_tp.dot(n_v)
N = vq_pp.dot(n_v)
Curve = s ** 2 * (L * N - M ** 2) / (q ** 4 * v ** 2 * sp.sin(x) ** 2)
Acc = (s) / (v * q ** 2 * abs(k))
s_arguments = [(x, y, k, c1, c4, p, t)]
c_arguments = [(s, st, Sp, stt, stp, spp, v, x, y, w)]
Curve = lambdify(c_arguments, Curve, modules='numpy')
nsimp_sp = lambdify(s_arguments, simp_sp, modules='numpy')
ndifx_sp = lambdify(s_arguments, difx_sp, modules='numpy')
ndify_sp = lambdify(s_arguments, dify_sp, modules='numpy')
ndiffxx_sp = lambdify(s_arguments, diffxx_sp, modules='numpy')
ndiffxy_sp = lambdify(s_arguments, diffxy_sp, modules='numpy')
ndiffyy_sp = lambdify(s_arguments, diffyy_sp, modules='numpy')


def get_K(theta, phi, opt, get_v=False):
    arguments = np.array([theta, phi, kv, c11, c44, pv, opt], dtype=np.float32)
    Curv_zero = (L * N - M ** 2)
    s_v = nsimp_sp(arguments)
    s_t_v = ndifx_sp(arguments)
    s_p_v = ndify_sp(arguments)
    if get_v:
        v1 = (s_v * n1.subs({x: theta, y: phi}) + s_t_v * ex1.subs({x: theta, y: phi})
              + s_p_v * ey1.subs({x: theta, y: phi}) / sp.sin(theta))
        v2 = (s_v * n2.subs({x: theta, y: phi}) + s_t_v * ex2.subs({x: theta, y: phi})
              + s_p_v * ey2.subs({x: theta, y: phi}) / sp.sin(theta))
        v3 = (s_v * n3.subs({x: theta, y: phi}) + s_t_v * ex3.subs({x: theta, y: phi}))
        return v1 / v3, v2 / v3, s_v

    s_tt_v = ndiffxx_sp(arguments)
    s_tp_v = ndiffxy_sp(arguments)
    s_pp_v = ndiffyy_sp(arguments)
    v_ab = (sp.sqrt(s_v ** 2 + s_t_v ** 2 + (s_p_v ** 2) / (sp.sin(theta) ** 2)))
    arguments = np.array([s_v, s_t_v, s_p_v, s_tt_v, s_tp_v,
                          s_pp_v, v_ab, theta, phi, wv], dtype=np.float32)
    return Curve(arguments)


def get_borders(phi, opt):
    Kl = 0
    Kr = 0
    step = sp.pi / 60
    r = 0
    borders = []
    for l in np.linspace(0.02, (sp.pi * 29 / 60) - 0.02, 30):
        if l == 0.02:
            Kl = get_K(l, phi, opt)
        r = l + step
        Kr = get_K(r, phi, opt)
        if ((Kl * Kr) < 0) or (Kl == 0 or Kr == 0):
            borders.append((l, r))
        Kl = Kr
    return borders


def get_Kzero(opt):
    theta_z = []
    phi_z = []
    for phi in np.linspace(0, np.pi / 2, 90):
        borders = get_borders(phi, opt)
        for l, r in borders:
            Kl = get_K(l, phi, opt)
            Kr = False
            while abs(l - r) >= 0.02:
                c = (r + l) / 2
                Kc = get_K(c, phi, opt)
                if (Kl * Kc) > 0:
                    l = c
                    Kl = Kc
                elif (Kl * Kc) < 0:
                    r = c
                else:
                    r = c
            theta_z.append((l + r) / 2)
            phi_z.append(phi)
            #zeros.append(((l+r)/2, phi))
    #return zeros
    return theta_z, phi_z


def get_caustic(opt):
    theta, phi = get_Kzero(opt)
    vx = []
    vz = []
    speed_val = []
    for i in range(len(theta)):
        v1, v2, speed = get_K(theta[i], phi[i], opt, True)
        #print(theta[i], phi[i], speed)
        vx.append(v1)
        vz.append(v2)
        speed_val.append(speed)
    #return [np.array(vx, dtype=np.float32).tolist(), np.array(vz, dtype=np.float32).tolist()]
    #return [np.array(elem, dtype=np.float32).tolist() for elem in [vx,vz,zeroes[0], zeroes[1], speed_val]]
    return [vx, vz, theta, phi, speed_val]

#get_caustic(sp.pi * (2) / 3)

def get_values_sympy(rad, move, opt):
    arguments = {x: rad, y: move, k: kv, c1: c11, c4: c44, p: pv, t: opt}
    s_val.append(simp_sp.subs(arguments))
    s_t_val.append(difx_sp.subs(arguments))
    s_p_val.append(dify_sp.subs(arguments))
    s_tt_val.append(diffxx_sp.subs(arguments))
    s_tp_val.append(diffxy_sp.subs(arguments))
    s_pp_val.append(diffyy_sp.subs(arguments))


def get_values_numpy(arguments):
    s_val.append(nsimp_sp(arguments))
    s_t_val.append(ndifx_sp(arguments))
    s_p_val.append(ndify_sp(arguments))
    s_tt_val.append(ndiffxx_sp(arguments))
    s_tp_val.append(ndiffxy_sp(arguments))
    s_pp_val.append(ndiffyy_sp(arguments))


def get_caustic3d():
    caus = get_caustic(sp.pi * (2) / 3)
    theta = np.array(caus[2], dtype=np.float32)
    phi = np.array(caus[3], dtype=np.float32)
    speed = caus[4]
    X = []
    Y = []
    Z = []
    for i in range(len(theta)):
        X.append(speed[i] * np.sin(theta) * np.cos(phi))
        Y.append(speed[i] * np.sin(theta) * np.sin(phi))
        Z.append(speed[i] * np.cos(theta))
    print(len(X))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z)
    plt.show()


def get_iso_surface3d(opt):
    X = []
    Y = []
    Z = []
    R = []
    i = 0
    for ph in np.linspace(0, np.pi * 2, 180):
        X.append([])
        Y.append([])
        Z.append([])
        R.append([])
        for th in np.linspace(0, np.pi, 90):
            arguments = np.array([th, ph, kv, c11, c44, pv, opt], dtype=np.float32)
            radius = 1 / nsimp_sp(arguments)
            theta = th
            phi = ph
            X[i].append(radius * np.sin(theta) * np.cos(phi))
            Y[i].append(radius * np.sin(theta) * np.sin(phi))
            Z[i].append(radius * np.cos(theta))
            R[i].append(radius)
        i += 1
    Z = np.array(Z)
    R = np.array(R)
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(X, Y, Z, rstride=2, cstride=2, shade=False, linewidth=0.5, edgecolors='k', color='grey')
    #ax.plot_surface(X, Y, Z, rstride=2, cstride=1, facecolors=cm.jet((R - R.min()) / (R.max() - R.min())), linewidth=0, shade=False)
    #plt.show()
    return X,Y,Z,R


from matplotlib import cm


#get_iso_surface3d()


def get_values(move, opt):
    global simp_sp, difx_sp, dify_sp, diffxx_sp, diffxy_sp, diffyy_sp
    count = 180
    part = 2
    radians = np.linspace(0, np.pi / part, count)
    K = []
    A = []
    v1 = []
    v2 = []
    v3 = []
    s_val.clear()
    s_t_val.clear()
    s_p_val.clear()
    v_abs.clear()
    s_tt_val.clear()
    s_tp_val.clear()
    s_pp_val.clear()
    for i, rad in enumerate(radians):
        arguments = np.array([rad, move, kv, c11, c44, pv, opt], dtype=np.float32)
        if rad >= 0.9 and rad <= 1:
            get_values_sympy(rad, move, opt)
        else:
            get_values_numpy(arguments)
        v1.append(s_val[-1] * n1.subs({x: rad, y: move}) + s_t_val[-1] * ex1.subs({x: rad, y: move})
                  + s_p_val[-1] * ey1.subs({x: rad, y: move}) / sp.sin(rad))
        v2.append(s_val[-1] * n2.subs({x: rad, y: move}) + s_t_val[-1] * ex2.subs({x: rad, y: move})
                  + s_p_val[-1] * ey2.subs({x: rad, y: move}) / sp.sin(rad))
        v3.append(s_val[-1] * n3.subs({x: rad, y: move}) + s_t_val[-1] * ex3.subs({x: rad, y: move}))
        if i == 0 or i == 1:
            v1[i] = v2[i] = 0
            v3[i] = s_val[i]
        if move == 0 and i == len(radians) - 1:
            v1[-1] = v1[-2] = s_val[-1]
            v2[-1] = v3[-1] = v2[-2] = v3[-2] = 0
        #v_abs.append(sp.sqrt(s_val[-1] ** 2 + s_t_val[-1] ** 2 + (s_p_val[-1] ** 2) / (sp.sin(rad) ** 2))) #c_arguments = [(s, st, Sp, stt, stp, spp, v)]
        v_abs.append(sp.sqrt(v1[-1] ** 2 + v2[-1] ** 2 + v3[-1] ** 2))
        arguments = np.array([s_val[-1], s_t_val[-1], s_p_val[-1], s_tt_val[-1], s_tp_val[-1],
                              s_pp_val[-1], v_abs[-1], rad, move, wv], dtype=np.float32)
        K.append(Curve(arguments))
        try:
            A.append(Acc.subs({s: s_val[-1], v: v_abs[-1], k: K[-1], w: wv}))
        except:
            A.append(0)
    K[0] = K[1] = K[2]
    K[-1] = K[-2] = K[-3]
    A[0] = A[1] = A[2]
    A[-1] = A[-2] = A[-3]
    return [v1, v2, v3, s_val.copy(), K, A]
