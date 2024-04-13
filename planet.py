from dataclasses import dataclass
from panda3d.core import Vec3, Point3, Vec4
from direct.motiontrail.MotionTrail import MotionTrail
import math

trail_thickness = 0.4
trail_lag = 8

@dataclass
class PlanetAttributes:
    mass = 2
    radius = 5.0
    position = [0, 0, 0]
    velocity = [0, 0, 0]

class Planet():
    def __init__(self, attributes: PlanetAttributes):
        self.attributes = attributes
    def delete(self):
        pass


class Planet3D(Planet):
    def __init__(self, world, attributes: PlanetAttributes, name):
        Planet.__init__(self, attributes)

        self.world = world
        self.deleted = False

        self.model = loader.loadModel("models/planet_sphere")
        self.texture = loader.loadTexture("models/sun_1k_tex.jpg")

        self.model.setTexture(self.texture, 1)
        self.model.reparentTo(world)
        self.model.setScale(self.attributes.radius)

        self.model.setPos(
                self.attributes.position[0],
                self.attributes.position[1],
                self.attributes.position[2]
                )

        self.motion_trail = MotionTrail(name, self.model)
        self.motion_trail.register_motion_trail()
        self.motion_trail.geom_node_path.reparent_to(render)

        self.motion_trail.add_vertex(Point3(0, trail_thickness/2, trail_thickness * math.sqrt(3)/4))
        self.motion_trail.add_vertex(Point3(0, -trail_thickness/2, trail_thickness * math.sqrt(3)/4))
        self.motion_trail.add_vertex(Point3(0, 0, -trail_thickness * math.sqrt(3)/4))

        self.motion_trail.set_vertex_color(0, Vec4(1.0, 1.0, 1.0, 1),     Vec4(0.0, 0.0, 0.0, 1))
        self.motion_trail.set_vertex_color(1, Vec4(1.0, 1.0, 1.0, 1),     Vec4(0.0, 0.0, 0.0, 1))
        self.motion_trail.set_vertex_color(2, Vec4(1.0, 1.0, 1.0, 1),     Vec4(0.0, 0.0, 0.0, 1))
        self.motion_trail.time_window = trail_lag
        self.motion_trail.update_vertices()

    

    def update(self):
        if self.deleted:
            return

        self.model.setPos(
                self.attributes.position[0],
                self.attributes.position[1],
                self.attributes.position[2]
                )
        self.model.setScale(self.attributes.radius)
        self.motion_trail.update_vertices()

    def delete(self):
        self.model.removeNode()
        #self.motion_trail.reset_motion_trail();
        #self.motion_trail.reset_motion_trail_geometry();
        self.motion_trail.reparentTo(self.world)
        self.deleted = True
