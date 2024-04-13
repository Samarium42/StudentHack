from direct.gui.DirectSlider import DirectSlider
from panda3d.core import NodePath
from direct.gui.DirectLabel import DirectLabel

class Graphics:
    def __init__(self, base):
        self.aspect2d = base.aspect2d  # Get the aspect2d node from the base
        self.aspect2d.setPos(0, 0, 0)  # Set the position of aspect2d node
        self.aspect2d.setDepthTest(False)
        
        self.slider = DirectSlider(range=(0, 100), command=self.slider_callback)
        self.slider.setScale(0.5)
        self.slider.setPos(-0.7, 0, 0.7)
        self.slider.reparentTo(self.aspect2d)

        self.label = DirectLabel(text="Slider Value: 0", pos=(-0.7, 0, 0.9), scale=0.1, parent=self.aspect2d)

    def slider_callback(self):
        slider_value = round(self.slider['value'])
        self.label['text'] = f"Slider Value: {slider_value}"
