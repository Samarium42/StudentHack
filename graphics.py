from direct.gui.DirectButton import DirectButton
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import NodePath
from planet import Planet,PlanetAttributes
from direct.gui.DirectEntry import DirectEntry
from mlmodel import PERIOD

class Graphics:
    def __init__(self, base, solar_system, states):
        self.solar_system = solar_system
        self.states = states
        self.aspect2d = base.aspect2d
        self.aspect2d.setDepthTest(False)
        
        self.planet = Planet()  # Assuming default attributes are set in Planet class
        
        self.button = DirectButton(text="Menu", command=self.show_slider_and_label)
        self.button.setScale(0.1)
        self.button.setPos(-0.9, 0, 0.8)
        self.button.reparentTo(self.aspect2d)

        self.slider = DirectSlider(range=(0, len(self.states) - 1), command=self.slider_callback)
        self.slider.setScale(0.4)
        self.slider.setPos(-0.8, 0, 0.8)
        self.slider.reparentTo(self.aspect2d)
        self.slider.hide()

        self.label = DirectLabel(text="Select generation: 0", pos=(-0.8, 0, 0.9), scale=0.06, parent=self.aspect2d)
        self.label.setTransparency(1)
        self.label.hide()

        self.button2 = DirectButton(text = "Simulate", command = self.show_epoch)
        self.button2.setScale(0.07)
        self.button2.setPos(-0.8, 0, 0.7)
        self.button2.hide()

        self.x_input = DirectEntry(command=self.entry_callback_x)
        self.x_input.setScale(0.03)
        self.x_input.setPos(-0.9, 0, 0.9)
        self.x_input.reparentTo(self.aspect2d)
        self.x_input.hide()

        self.y_input = DirectEntry(command=self.entry_callback_y)
        self.y_input.setScale(0.03)
        self.y_input.setPos(0, 0, 0.9)
        self.y_input.reparentTo(self.aspect2d)
        self.y_input.hide()
        

        self.z_input = DirectEntry(command=self.entry_callback_z)
        self.z_input.setScale(0.03)
        self.z_input.setPos(0.9, 0, 0.9)
        self.z_input.reparentTo(self.aspect2d)
        self.z_input.hide()
        

        self.v_x_in = DirectEntry(command=self.entry_callback_v_x)
        self.v_x_in.setScale(0.03)
        self.v_x_in.setPos(-0.9, 0, 0.7)
        self.v_x_in.reparentTo(self.aspect2d)
        self.v_x_in.hide()

        self.v_y_in = DirectEntry(command=self.entry_callback_v_y)
        self.v_y_in.setScale(0.03)
        self.v_y_in.setPos(0, 0, 0.7)
        self.v_y_in.reparentTo(self.aspect2d)
        self.v_y_in.hide()

        self.v_z_in = DirectEntry(command=self.entry_callback_v_z)
        self.v_z_in.setScale(0.03)
        self.v_z_in.setPos(0.9, 0, 0.7)
        self.v_z_in.reparentTo(self.aspect2d)
        self.v_z_in.hide()


    def show_slider_and_label(self):
        if self.slider.isHidden():
            self.slider.show()
            self.label.show()
            self.button2.show()
            self.button.hide()
            self.x_input.hide()
            self.y_input.hide()
            self.z_input.hide()
            self.v_x_in.hide()
            self.v_y_in.hide()
            self.v_z_in.hide()
        else:
            self.slider.hide()
            self.label.hide()
            self.button2.hide()
            self.button.show()
            self.x_input.hide()
            self.y_input.hide()
            self.z_input.hide()
            self.v_x_in.hide()
            self.v_y_in.hide()
            self.v_z_in.hide()

    def slider_callback(self):
        slider_value = round(self.slider['value'])
        self.label['text'] = f"Generation number: {slider_value*PERIOD}"


    def entry_callback_x(self, value):
        entry_value = float(value)
        self.planet.attributes.position[0] = entry_value
        self.label['text'] = f"X position: {entry_value}"

    def entry_callback_y(self, value):
        entry_value = float(value)
        self.planet.attributes.position[1] = entry_value
        self.label['text'] = f"Y position: {entry_value}"

    def entry_callback_z(self, value):
        entry_value = float(value)
        self.planet.attributes.position[2] = entry_value
        self.label['text'] = f"Z position: {entry_value}"        
        

    def entry_callback_v_x(self, value):        
        entry_value = float(value)
        self.planet.attributes.velocity[0] = entry_value
        self.label['text'] = f"X velocity: {entry_value}"  

    def entry_callback_v_y(self, value):
        entry_value = float(value)
        self.planet.attributes.velocity[1] = entry_value
        self.label['text'] = f"Y velocity: {entry_value}"

    def entry_callback_v_z(self, value):
        entry_value = float(value)
        self.planet.attributes.velocity[2] = entry_value
        self.label['text'] = f"Z velocity: {entry_value}"

    def show_epoch(self):
        self.solar_system.delete()
        slider_value = round(self.slider['value'])
        planets = self.states[slider_value]
        self.solar_system.loadPlanets(planets)


    def show_add_planet_menu(self):
        if self.x_input.isHidden():
            self.x_input.show()
            self.y_input.show()
            self.z_input.show()
            self.v_x_in.show()
            self.v_y_in.show()
            self.v_z_in.show()
            self.button2.hide()
            self.button.hide()
            self.label.hide()
            self.slider.hide()
        else:
            self.x_input.hide()
            self.y_input.hide()
            self.z_input.hide()
            self.v_x_in.hide()
            self.v_y_in.hide()
            self.v_z_in.hide()
            self.button2.show()
            self.button.hide()
            self.label.hide()
            self.slider.hide()
            self.aspect2d.hide()


        

