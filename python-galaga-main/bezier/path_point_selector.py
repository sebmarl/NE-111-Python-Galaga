""" SM (Sebastian Marion-Landais) """ 
from .control_point_handler import ControlPointHandler


class PathPointSelector():
    def __init__(self, control_point_quartet_collection):
        self.control_point_quartet_collection = control_point_quartet_collection
        self.path_point_mapping = {}

    def create_key(self, quartet_index, control_point_index):
        return f'Q{quartet_index}/P{control_point_index}'

    def is_path_point(self, control_point_handler: ControlPointHandler):
        if control_point_handler.control_point_index == 0 or control_point_handler.control_point_index == 3:
            return True
        return False
        #Creates the intialize function that works with quartets in order to determine the path of control points for the enemies class\
        #using the is path point method, it checks if the control point is part of the path. SM """ 

    def create_path_point_mapping(self):

        nr_quartets = self.control_point_quartet_collection.number_of_quartets()

        for index in range(nr_quartets):
            mapped_first_quartet_index = 0
            if index == 0:
                mapped_first_quartet_index = nr_quartets - 1
            else:
                mapped_first_quartet_index = index - 1

            mapped_last_quartet_index = 0
            if index < nr_quartets - 1:
                mapped_last_quartet_index = index + 1
            else:
                mapped_last_quartet_index = 0

            self.path_point_mapping[self.create_key(index, 0)] = ControlPointHandler(mapped_first_quartet_index, 3)
            self.path_point_mapping[self.create_key(index, 3)] = ControlPointHandler(mapped_last_quartet_index, 0)
            #The path point mapping function creates mappings between the first and last control points of the quartet. These values are then\
            #stored in the path point mapping method and then turned into keys for future reference SM """ 

    
    def find_related_path_point(self, control_point_handler: ControlPointHandler):
        if self.is_path_point(control_point_handler):
            key = self.create_key(control_point_handler.quartet_index, control_point_handler.control_point_index)
            return self.path_point_mapping[key]
        else:
            print('error')
            exit(1)
        #checks if something is a path point, if so it hten creates a key and looks up the valid path point in\
            #path point mapping method. Otherwise an error is printed if it is not a path point SM """ 

    def find_related_control_point(self, control_point_handler: ControlPointHandler):
        related_control_point = ControlPointHandler(-1, -1)
        last_quartet_index = self.control_point_quartet_collection.number_of_quartets() - 1

        if control_point_handler.control_point_index == 1:
            related_control_point.control_point_index = 2
            if control_point_handler.quartet_index == 0:
                related_control_point.quartet_index = last_quartet_index
            elif control_point_handler.quartet_index > 0:
                related_control_point.quartet_index = control_point_handler.quartet_index - 1

        elif control_point_handler.control_point_index == 2:
            related_control_point.control_point_index = 1
            if control_point_handler.quartet_index < last_quartet_index:
                related_control_point.quartet_index = control_point_handler.quartet_index + 1
            else:
                related_control_point.quartet_index = 0
        return related_control_point
        #This function checks the related control point based on the ControlPointHandler \
                #method and the it is set to specific conditions based on the original points index and\
                #quartet index. SM """ 

    def get_last_quartet_index(self):
        return self.control_point_quartet_collection.number_of_quartets() - 1
        """ Gets last quarter index SM """ 

    def get_number_of_quartets(self):
        return self.control_point_quartet_collection.number_of_quartets()
        """ Gets the # of quartets SM """ 

    def find_path_point_of_control_point(self, control_point_handler: ControlPointHandler):
        related_control_point = ControlPointHandler(-1, -1)

        if control_point_handler.control_point_index == 1:
            related_control_point.control_point_index = 0
        elif control_point_handler.control_point_index == 2:
            related_control_point.control_point_index = 3

        related_control_point.quartet_index = control_point_handler.quartet_index

        return related_control_point
    #Determines the control point solely on the control point index. If the quartet index\
        #is related ot the control point, it is then set to the same quartet index as the original control\
        #point. SM """ 

    def find_control_points_of_path_point(self, path_point_handler: ControlPointHandler):
        related_control_points = []
        number_of_quartets = self.control_point_quartet_collection.number_of_quartets()
        last_quartet_index = number_of_quartets - 1

        if path_point_handler.control_point_index == 0:
            related_control_points.append(ControlPointHandler(path_point_handler.quartet_index, 1))
            if path_point_handler.quartet_index == 0:
                related_control_points.append(ControlPointHandler(last_quartet_index, 2))
            else:
                related_control_points.append(ControlPointHandler(path_point_handler.quartet_index - 1, 2))

        elif path_point_handler.control_point_index == 3:
            related_control_points.append(ControlPointHandler(path_point_handler.quartet_index, 2))
            if path_point_handler.quartet_index == 0 and number_of_quartets > 1:
                related_control_points.append(ControlPointHandler(path_point_handler.quartet_index + 1, 1))
            else:
                if path_point_handler.quartet_index == last_quartet_index:
                    related_control_points.append(ControlPointHandler(0, 1))
                else:
                    related_control_points.append(ControlPointHandler(path_point_handler.quartet_index + 1, 1))
        else:
            print('error')
            exit(1)

        return related_control_points
        #This function determines the related control points based on their path. The related\
        #points are then added to a list which gets returned. IF there are any invalid point indexes in the\ 
        #list, an error is returned and the game exits with error 1 SM """ 

    def get_control_point_pairs(self):
        line_list = []

        control_point1 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(0, 1))
        last_quartet_index = self.get_last_quartet_index()
        control_point2 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(last_quartet_index, 2))
        line_list.append(((control_point1.x, control_point1.y), (control_point2.x, control_point2.y)))

        if self.get_number_of_quartets() > 1:
            for index in range(last_quartet_index):
                control_point1 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(index, 2))
                control_point2 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(index + 1, 1))
                line_list.append(((control_point1.x, control_point1.y), (control_point2.x, control_point2.y)))

        return line_list
        """ Creates pairs of control points representing lines. Using the first and last control points\
        it creates line segments, and further line segments are created for adjacent quartets. Finally a list is\
        returned with control point pairs SM """ 
