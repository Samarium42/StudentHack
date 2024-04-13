from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectSlider import DirectSlider

class Graphics(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Create a slider
        slider = DirectSlider(range=(0, 100), value=50, command=self.slider_callback)
        slider.setScale(0.5)
        slider.setPos(-0.8, 0, -0.8)
        slider.reparentTo(self.aspect2d)
        
    def slider_callback(self):
        # Handle slider value changes here
        pass
