#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Last Updated: 2015-03-13
#
# This tutorial will cover events and how they can be used in Panda
# Specifically, this lesson will use events to capture keyboard presses and
# mouse clicks to trigger actions in the world. It will also use events
# to count the number of orbits the Earth makes around the sun. This
# tutorial uses the same base code from the solar system tutorial.

from planet import Planet, PlanetAttributes
from graphics import Graphics

from direct.showbase.ShowBase import ShowBase
from graphics import Graphics
base = ShowBase()

from panda3d.core import NodePath, PandaNode, TextNode, Vec3
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.task.Task import TaskManager
import sys

import random

# We start this tutorial with the standard class. However, the class is a
# subclass of an object called DirectObject. This gives the class the ability
# to listen for and respond to events. From now on the main class in every
# tutorial will be a subclass of DirectObject

class SolarSystem():
    def loadPlanets(self, num_planets: int):
        self.planets = []

        sunattr = PlanetAttributes()
        sunattr.mass = 10
        sunattr.radius = 1.2
        sunattr.position=Vec3( 0,0,0)

        sun = Planet(render, sunattr)
        self.planets.append(sun)
        for x in range(num_planets - 1):
            attr = PlanetAttributes()
            attr.mass = random.randint(1, 20)
            attr.radius = random.randint(1, 5)*0.1
            print(type(attr.radius))
            attr.position=Vec3(
                random.randint(-10, 10),
                random.randint(-10, 10),
                random.randint(-10, 10)
                )

            planet = Planet(render, attr)

        self.planets.append(planet)

    def update(self):
        # todo add physics here
        print("test task")

class World(DirectObject):
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.05)

    def __init__(self):

        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        #base.disableMouse()
        camera.setPos(0, 0, 45)
        camera.setHpr(0, -90, 0)

        self.solar_system = SolarSystem()
        self.solar_system.loadPlanets(3)  # Load, texture, and position the planets

        self.title = OnscreenText(
            text="Panda3D: Tutorial 3 - Events",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)

        self.accept("escape", sys.exit)
        self.accept("mouse1", self.handleMouseClick)

    def handleMouseClick(self):
        pass

    def handleEarth(self):
        self.togglePlanet("Earth", self.day_period_earth,
                          self.orbit_period_earth, self.ekeyEventText)
        self.togglePlanet("Moon", self.day_period_moon,
                          self.orbit_period_moon)

    def update(self, task):

        print(camera.getPos())
        self.solar_system.update()

#########################################################################
# Except for the one commented line below, this is all as it was before #
# Scroll down to the next comment to see an example of sending messages #
#########################################################################


if __name__ == "__main__":
    w = World()
    g = Graphics(base)

    task_manager = TaskManager()
    task_manager.setupTaskChain("taskChain", numThreads = 1, tickClock = True,
                           frameBudget = -1,
                           frameSync = True, timeslicePriority = False)
    task_manager.add(w.update, "updateSolarSystem", taskChain="taskChain")

    base.run()
