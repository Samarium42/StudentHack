from direct.gui.DirectSlider import DirectSlider
from panda3d.core import NodePath
from direct.gui.DirectLabel import DirectLabel

class Graphics:
    def __init__(self, base):  # Add base as an argument
        self.aspect2d = base.aspect2d  # Get the aspect2d node from the base
        self.aspect2d.setPos(0, 0, 0)  # Set the position of aspect2d node
        
        self.aspect2d.setDepthTest(False)  # Disable depth testing for GUI elements
        
        slider = DirectSlider(range=(0, 100), value=50, command=self.slider_callback)
        slider.setScale(0.5)
        slider.setPos(-0.7, 0, 0.7)
        slider.reparentTo(self.aspect2d)

        label = DirectLabel(text=f"Slider Value: {slider['value']}", pos=(-0.7, 0, 0.9), scale=0.1, parent=self.aspect2d)
        
    
    def slider_callback(self):
        pass
    
