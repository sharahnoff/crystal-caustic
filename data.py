import calcualtions as cs
import numpy as np
import os.path
import csv
from crystal import *

name = ''
t1 = []
t2 = []
t1d = []
t2d = []
t1c = []
t2c = []


def check_save(crystals):
    for cr in crystals:
        element = cr.name
        file_name = f'calculatedData/{element.lower()}'
        if os.path.exists(f'{file_name}t1.csv'):
            cr.saved = True
    return


def load_crystals():
    with open('elements.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        crystals = []
        for row in reader:
            crystals.append(Crystal(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4])))
            #elements[row[0]] = [float(row[1]), float(row[2]), float(row[3]), float(row[4])]
        check_save(crystals)
        return crystals

def save_data(cr):
    try:
        file_name = f'calculatedData/{cr.name.lower()}'
        t1 = np.array([cr.t1[0][:180], cr.t1[1][:180], cr.t1[2][:180], cr.t1[3][:180], cr.t1[4][:180], cr.t1[5][:180],
                       cr.t1d[0][:180], cr.t1d[1][:180], cr.t1d[2][:180], cr.t1d[3][:180], cr.t1d[4][:180], cr.t1d[5][:180]])
        np.savetxt(f'{file_name}t1.csv', t1, delimiter=',', fmt='%e')
        t2 = np.array([cr.t2[0][:180], cr.t2[1][:180], cr.t2[2][:180], cr.t2[3][:180], cr.t2[4][:180], cr.t2[5][:180],
                       cr.t2d[0][:180], cr.t2d[1][:180], cr.t2d[2][:180], cr.t2d[3][:180], cr.t2d[4][:180], cr.t2d[5][:180]])
        np.savetxt(f'{file_name}t2.csv', t2, delimiter=',', fmt='%e')
        t1c = np.array([cr.t1c[0], cr.t1c[1]])
        np.savetxt(f'{file_name}t1c.csv', t1c, delimiter=',', fmt='%e')
        t2c = np.array([cr.t2c[0], cr.t2c[1]])
        np.savetxt(f'{file_name}t2c.csv', t2c, delimiter=',', fmt='%e')
        return True
    except Exception as e:
        print(e)
        return False


def load_data(cr):
    try:
        file_name = f'calculatedData/{cr.name.lower()}'
        if not os.path.exists(f'{file_name}t1.csv'):
            return False
        t1_loaded = np.loadtxt(f'{file_name}t1.csv', delimiter=',').tolist()
        t2_loaded = np.loadtxt(f'{file_name}t2.csv', delimiter=',').tolist()
        t1 = t1_loaded[:6]
        t2 = t2_loaded[:6]
        t1d = t1_loaded[6:]
        t2d = t2_loaded[6:]
        t1c = np.loadtxt(f'{file_name}t1c.csv', delimiter=',').tolist()
        t2c = np.loadtxt(f'{file_name}t2c.csv', delimiter=',').tolist()
        cr.load_data(t1, t2, t1d, t2d, t1c, t2c)
        return True
    except:
        return False


