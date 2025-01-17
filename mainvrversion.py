#!/usr/bin/env python
from planet import Planet3D, PlanetAttributes
from graphics import Graphics
from mlmodel import RConserved

from direct.showbase.ShowBase import ShowBase
base = ShowBase()

from panda3d.core import Point3
from panda3d.core import AudioManager, AudioSound
from panda3d.core import loadPrcFileData
from panda3d.openvr import OpenVRDevice, OpenVRStereoDisplayRegion


from panda3d.core import NodePath, PandaNode, TextNode, Vec3
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.task.Task import TaskManager
import sys
from physics import updateAllObjects
import random

NO_PLANETS = 4
SPEED = 45


class SolarSystem():
    def __init__(self):
        self.ready = False

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

    def update(self):
        updateAllObjects(self.planets, time=SPEED)
        for planet in self.planets:
            planet.update()


class World(DirectObject):
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.05)

    def __init__(self, task_manager):
        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        #base.disableMouse()
        camera.setPos(0, 0, 45)
        camera.setHpr(0, -90, 0)


        # Enable VR
        loadPrcFileData("", "load-display pandagl")
        self.vr_device = OpenVRDevice()
        if not self.vr_device.init():
            print("Failed to initialize VR device")
            return
        # Create a stereo display region for VR
        self.vr_display_region = OpenVRStereoDisplayRegion(self.vr_device, base.cam, base.win)


        self.solar_system = SolarSystem()
        self.solar_system.loadPlanets(NO_PLANETS)  # Load, texture, and position the planets

        self.audio_manager = AudioManager.create_AudioManager()
        self.sound = self.audio_manager.get_sound("Sounds/51230__rutgermuller__atmospheric-ambient-spacy-synth-beat.wav")

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
        self.solar_system.update()
        print(RConserved(self.solar_system.planets))
        if self.sound.status() != AudioSound.PLAYING:
            # Restart the sound
            self.sound.play()
        return task.cont

#########################################################################
# Except for the one commented line below, this is all as it was before #
# Scroll down to the next comment to see an example of sending messages #
#########################################################################


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.setupTaskChain("taskChain", numThreads = 1, tickClock = True,
                           frameBudget = -1,
                           frameSync = True, timeslicePriority = False)
    w = World(task_manager)
    g = Graphics(base) 

    base.run()