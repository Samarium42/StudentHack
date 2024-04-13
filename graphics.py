from direct.gui.DirectButton import DirectButton
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import NodePath
from planet import Planet,PlanetAttributes

class Graphics:
    def __init__(self, base):
        self.aspect2d = base.aspect2d
        self.aspect2d.setDepthTest(False)
        
        self.planet = Planet(PlanetAttributes)  # Assuming default attributes are set in Planet class
        
        self.button = DirectButton(text="Menu", command=self.show_slider_and_label)
        self.button.setScale(0.1)
        self.button.setPos(-0.9, 0, 0.8)
        self.button.reparentTo(self.aspect2d)

        self.slider = DirectSlider(range=(0, 100), command=self.slider_callback)
        self.slider.setScale(0.3)
        self.slider.setPos(-0.8, 0, 0.8)
        self.slider.reparentTo(self.aspect2d)
        self.slider.hide()

        self.label = DirectLabel(text="Select number of planets: 0", pos=(-0.8, 0, 0.9), scale=0.06, parent=self.aspect2d)
        self.label.setTransparency(1)
        self.label.hide()


    def show_slider_and_label(self):
        if self.slider.isHidden():
            self.slider.show()
            self.label.show()
            self.button.hide()
        else:
            self.slider.hide()
            self.label.hide()

    def slider_callback(self):
        slider_value = round(self.slider['value'])
        self.label['text'] = f"Number of planets: {slider_value}"

