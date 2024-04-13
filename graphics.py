from panda3d.core import NodePath
from direct.gui.DirectSlider import DirectSlider

class Graphics:
    def __init__(self):
        self.aspect2d = NodePath("aspect2d")
        self.aspect2d.setPos(-1, 0, -1)  # Set the position of aspect2d node
        
        slider = DirectSlider(range=(0, 100), value=50, command=self.slider_callback)
        slider.setScale(0.5)
        slider.setPos(-0.8, 0, -0.8)
        slider.reparentTo(self.aspect2d)
        
    def slider_callback(self):
        # Handle slider value changes here
        pass
