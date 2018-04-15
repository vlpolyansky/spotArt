# -*- coding: utf-8 -*-
"""
Use GLImageItem to display image data on rectangular planes.

In this example, the image data is sampled from a volume and the image planes 
placed as if they slice through the volume.
"""
## Add path to library (just for examples; you do not need this)

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import scipy.ndimage
import scipy.misc
from tinydb import TinyDB
import math

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Constants
floor_sz = [1000, 500]
wall_height = 250
painting_width = 100
painting_spacing = 50


def tile(array, size):
    array = np.tile(array, [size[0] / array.shape[0] + 1, size[1] / array.shape[1] + 1, 1])
    array = array[:size[0], :size[1], :]
    return array


class MyView(gl.GLViewWidget):
    def __init__(self):
        super(MyView, self).__init__()
        self.opts['distance'] = 10
        self.opts['center'].setX(floor_sz[0] * 0.5)
        self.opts['center'].setY(floor_sz[1] * 0.5)
        self.opts['center'].setZ(wall_height * 0.5)
        self.opts['elevation'] = 0
        self.show()
        self.setWindowTitle('Hack4Sweden')

        # Floor
        floor_tex = scipy.ndimage.imread('textures/wood.jpeg', mode='RGBA')
        floor_tex = tile(floor_tex, floor_sz)
        floor = gl.GLImageItem(floor_tex)
        self.addItem(floor)

        # Walls
        wall1_tex = scipy.ndimage.imread('textures/wall_tex.jpg', mode='RGBA')
        wall1_tex = tile(wall1_tex, [floor_sz[0], wall_height])
        wall1 = gl.GLImageItem(wall1_tex)
        wall1.rotate(90, 1, 0, 0)
        self.addItem(wall1)

        wall2 = gl.GLImageItem(wall1_tex)
        wall2.rotate(90, 1, 0, 0)
        wall2.translate(0, floor_sz[1], 0)
        self.addItem(wall2)

        # Lighting

        globAmb = [0.3, 0.3, 0.3, 1.0]
        lightAmb = [0.75, 0.75, 0.75, 1.0]
        lightDifAndSpec = [0.7, 0.7, 0.7, 1.0]

        # glEnable(GL_LIGHTING)
        # glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmb)
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDifAndSpec)
        # glLightfv(GL_LIGHT0, GL_SPECULAR, lightDifAndSpec)
        # # glLightfv(GL_LIGHT0, GL_POSITION, [500, 250, 100, 0])
        # glEnable(GL_LIGHT0)
        # glLightModelfv(GL_LIGHT_MODEL_AMBIENT, globAmb)
        # glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        # glEnable(GL_DEPTH_TEST)

        # Load paintings
        db = TinyDB('paintings/db.json')

        # db.insert({'name': 'Captain Planet', 'img': 'test.jpg'})

        added = 0
        for item in db.all():
            painting_tex = scipy.ndimage.imread('paintings/' + item['img'], mode='RGBA')
            painting = gl.GLImageItem(painting_tex, smooth=True)
            scale = painting_width * 1.0 / painting_tex.shape[1]
            painting.rotate(90, 0, 1, 0)
            painting.rotate(90, 0, 0, 1)
            painting.scale(scale, scale, scale)

            added += painting_spacing + painting_width
            painting.translate(added, 5, painting_tex.shape[0] * scale / 2 + wall_height / 2)
            self.addItem(painting)


    def keyPressEvent(self, ev):
        gl.GLViewWidget.keyPressEvent(self, ev)
        key = ev.key()
        x = self.opts['center'][0]
        y = self.opts['center'][1]
        len = 10
        angle = self.opts['azimuth'] / 180.0 * 3.1416
        if key == QtCore.Qt.Key_W:
            x -= len * math.cos(angle)
            y -= len * math.sin(angle)
        if key == QtCore.Qt.Key_S:
            x += len * math.cos(angle)
            y += len * math.sin(angle)
        if key == QtCore.Qt.Key_A:
            x += len * math.sin(angle)
            y -= len * math.cos(angle)
        if key == QtCore.Qt.Key_D:
            x -= len * math.sin(angle)
            y += len * math.cos(angle)
        self.opts['center'].setX(x)
        self.opts['center'].setY(y)
        self.update()


app = QtGui.QApplication([])

w = MyView()
w.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
