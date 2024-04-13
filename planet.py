from dataclasses import dataclass
from panda3d.core import Vec3

@dataclass
class PlanetAttributes:
    mass = 2
    radius = 5.0
    position = [0, 0, 0]
    velocity = [0, 0, 0]

class Planet():
    def __init__(self, attributes: PlanetAttributes):
        self.attributes = attributes


class Planet3D(Planet):
    def __init__(self, world, attributes: PlanetAttributes):
        Planet.__init__(self, attributes)

        self.model = loader.loadModel("models/planet_sphere")
        self.texture = loader.loadTexture("models/sun_1k_tex.jpg")

        self.model.setTexture(self.texture, 1)
        self.model.reparentTo(world)
        print(type(attributes))
        self.model.setScale(self.attributes.radius)

        self.model.setPos(
                self.attributes.position[0],
                self.attributes.position[1],
                self.attributes.position[2]
                )

    def update(self):
        self.model.setPos(
                self.attributes.position[0],
                self.attributes.position[1],
                self.attributes.position[2]
                )
        self.model.setScale(self.attributes.radius)

    def delete(self):
        self.model.removeNode()
