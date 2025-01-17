#!/usr/bin/env python
from mlmodel import genetic, planet_to_array, populate
from planet import Planet3D, PlanetAttributes
from graphics import Graphics
#from mlmodel import RConserved

from direct.showbase.ShowBase import ShowBase, WindowProperties
from direct.filter.CommonFilters import CommonFilters
base = ShowBase()

from panda3d.core import Point3
from panda3d.core import AudioManager, AudioSound

from panda3d.core import NodePath, PandaNode, TextNode, Vec3
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.task.Task import TaskManager
import sys
from physics import updateAllObjects
import random
from panda3d.core import AmbientLight

NO_PLANETS = 20
SPEED = 45000
AMBIENT_LEVEL = 0.7



states = genetic(10,10,10,10)
print(len(states))

class SolarSystem():
    def __init__(self):
        self.ready = False
        self.createSky()

    def createSky(self):
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky_tex = loader.loadTexture("models/stars.png")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(400)

        alight = AmbientLight('alight')
        alight.setColor((
            AMBIENT_LEVEL,
            AMBIENT_LEVEL,
            AMBIENT_LEVEL,
            1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        render.setShaderAuto()


    def delete(self):
        for planet in self.planets:
            planet.delete()

        for i in range(len(self.planets)-1, -1, -1):
            planet = self.planets[i]
            self.planets.pop(i)


        print(len(self.planets))


    def loadPlanets(self, planets: list):
        self.planets = []
        self.deleted_trails = []

        sunattr = PlanetAttributes()
        sunattr.mass = 500 
        sunattr.radius = 1
        sunattr.position=Vec3(0,0,0)
        sunattr.velocity = Vec3(1E-7,1E-7,10E-7)

        sunattr.sun = True
        sun = Planet3D(render, sunattr, "Sun")
        self.planets.append(sun)

        for p in planets:
            attr = p.attributes
            attr.texture = random.random()
            planet = Planet3D(render, p.attributes, "")
            self.planets.append(planet)

        # for x in range(num_planets - 1):
        #     attr = PlanetAttributes()
        #     attr.mass = random.randint(1, 20) * 10
        #     attr.radius = random.randint(1, 5) * 0.05
        #     attr.position = [
        #         random.randint(-20, 20),
        #         random.randint(-20, 20),
        #         random.randint(-20, 20)
        #         ]
        #     attr.velocity = [
        #         random.randint(-10, 10)*10E-7,
        #         random.randint(-10, 10)*10E-7,
        #         random.randint(-10, 10)*10E-7
        #         ]
        #     attr.texture = random.random()
        #
        #     planet = Planet3D(render, attr, f"Planet{x}")
        #     self.planets.append(planet)
        #
        self.ready = True

    def update(self, task):
        dt = globalClock.getDt()
        time = int(globalClock.getFrameTime())

        updateAllObjects(self.planets, time=dt*SPEED)
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

    def __init__(self, task_manager, planets):
        self.update_counter = 0
        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        #base.disableMouse()
        camera.setPos(0, 45, 45)
        camera.setHpr(0, -90, 0)

        self.solar_system = SolarSystem()
        self.solar_system.loadPlanets(NO_PLANETS)  # Load, texture, and position the planets

        self.audio_manager = AudioManager.create_AudioManager()
        self.sound = self.audio_manager.get_sound("Sounds/Sound.wv")

        self.title = OnscreenText(
            text="Panda3D: Tutorial 3 - Events",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)
        self.solar_system.loadPlanets(planets)  # Load, texture, and position the planets

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

    planets = states[75]

    wp = WindowProperties()
    wp.setFullscreen(0)
    wp.setSize(3072, 1920)
    base.openMainWindow()
    base.win.requestProperties(wp)

    filters = CommonFilters(base.win, base.cam)
    filters.setBloom(size = "medium")

    task_manager = TaskManager()
    task_manager.setupTaskChain("taskChain", numThreads = 4, tickClock = True,
                           frameBudget = -1,
                           frameSync = True, timeslicePriority = False)

    w = World(task_manager, planets)
    g = Graphics(base, w.solar_system, states)

    base.run()