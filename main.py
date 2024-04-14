#!/usr/bin/env python
from planet import Planet3D, PlanetAttributes
from graphics import Graphics
#from mlmodel import RConserved

from direct.showbase.ShowBase import ShowBase, WindowProperties
base = ShowBase()

from panda3d.core import NodePath, PandaNode, TextNode, Vec3
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.task.Task import TaskManager
import sys
from physics import updateAllObjects
import random

NO_PLANETS = 6
SPEED = 45


class SolarSystem():
    def __init__(self):
        self.ready = False
        self.createSky()

    def createSky(self):
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(400)

    def loadPlanets(self, num_planets: int):
        self.planets = []
        self.deleted_trails = []

        sunattr = PlanetAttributes()
        sunattr.mass = 10
        sunattr.radius = 1.2
        sunattr.position=Vec3(0,0,0)

        sunattr.sun = True
        sun = Planet3D(render, sunattr, "Sun")
        self.planets.append(sun)
        for x in range(num_planets - 1):
            attr = PlanetAttributes()
            attr.mass = random.randint(1, 20) * 10
            attr.radius = random.randint(1, 5)*0.1
            attr.position = [
                random.randint(-10, 10),
                random.randint(-10, 10),
                random.randint(-10, 10)
                ]
            attr.velocity = [
                random.randint(-10, 10)*10E-7,
                random.randint(-10, 10)*10E-7,
                random.randint(-10, 10)*10E-7
                ]
            attr.texture = random.random()

            planet = Planet3D(render, attr, f"Planet{x}")
            self.planets.append(planet)

        self.ready = True

    def update(self, task):
        updateAllObjects(self.planets, time=SPEED)
        for i in range(len(self.planets)-1, -1, -1):
            planet = self.planets[i]
            if planet.deleted:
                self.planets.pop(i)
                continue

            planet.update()

class World(DirectObject):
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.05)

    def __init__(self, task_manager):
        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        #base.disableMouse()
        camera.setPos(0, 45, 45)
        camera.setHpr(0, -90, 0)

        self.solar_system = SolarSystem()
        self.solar_system.loadPlanets(NO_PLANETS)  # Load, texture, and position the planets

        self.title = OnscreenText(
            text="Panda3D: Tutorial 3 - Events",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)

        self.accept("escape", sys.exit)
        self.accept("mouse1", self.handleMouseClick)

        task_manager.add(self.update, "updateSolarSystem", taskChain="taskChain")

    def handleMouseClick(self):
        pass

    def handleEarth(self):
        self.togglePlanet("Earth", self.day_period_earth,
                          self.orbit_period_earth, self.ekeyEventText)
        self.togglePlanet("Moon", self.day_period_moon,
                          self.orbit_period_moon)

    def update(self, task):
        self.solar_system.update(task)
        #print(RConserved(self.solar_system.planets))
        return task.cont

#########################################################################
# Except for the one commented line below, this is all as it was before #
# Scroll down to the next comment to see an example of sending messages #
#########################################################################


if __name__ == "__main__":
    wp = WindowProperties()
    wp.setFullscreen(1)
    wp.setSize(1280, 720)
    base.openMainWindow()
    base.win.requestProperties(wp)

    task_manager = TaskManager()
    task_manager.setupTaskChain("taskChain", numThreads = 1, tickClock = True,
                           frameBudget = -1,
                           frameSync = True, timeslicePriority = False)

    w = World(task_manager)
    g = Graphics(base)

    base.run()

