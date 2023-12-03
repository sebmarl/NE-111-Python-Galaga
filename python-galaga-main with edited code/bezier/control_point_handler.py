"""AG(Advait Gore)"""
#This class creates the control point handler
#It is used to track the control point that is being manipulated
class ControlPointHandler():
    def __init__(self, quartet_index, control_point_index):
        self.quartet_index = quartet_index
        self.control_point_index = control_point_index
