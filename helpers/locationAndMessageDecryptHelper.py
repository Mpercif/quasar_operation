import math

import numpy as np
from app.api.exceptions.errors import SatelliteValidationNotSuccess


class LocationAndMessageDecryptHelper(object):
    """
    Contain methods related to Location And Message Decrypt
    """

    def __init__(self, satellites):
        """
        Initialize instance of LocationAndMessageDecryptHelper
        :param satellites: list of satellites configuration
        [
            {
              "name": "kenobi",
              "distance": 100.0,
              "message": ["este", "", "", "mensaje", ""]
            },
            ...
        ]
        """
        self.satellites = satellites
        self.message_length = 0
        self.message = ""
        self.satellites_length = 0

    def get_message(self, messages=None):
        """
        Find the encrypted message, removing the offset in each message and determining the minimum message length.
        :param messages: List of message lists [["", "es", "","secreto"],["es", "mensaje", ""]]
        :return: Return decrypted message. Ie, "este es un mensaje secreto"
        """
        try:
            self.message_length = self.get_message_length(messages)
            np_messages = np.array(self.remove_offset_messages(messages))
            new_set_words = self.get_columns_to_rows_words(np_messages)
            self.message = self.find_message_encrypted(new_set_words)

            return self.message
        except SatelliteValidationNotSuccess as e:
            raise e
        except Exception as e:
            raise e

    def get_message_length(self, messages):
        """
        Find the minimum message length
        :param messages: List of message lists. Ie, [["", "es", "","secreto"],["es", "mensaje", ""]]
        :return: message length. Ie, 5
        """
        return np.min([len(x) for x in messages])

    def remove_offset_messages(self, messages):
        """
        Searches for and removes the message de-facing
        :param messages: List of message lists [["", "es", "","secreto"],["es", "mensaje", ""]]
        :return: List of message lists without offset [["es", "","secreto"],["es", "mensaje", ""]]
        """
        messages_fixed = []
        for message in messages:
            len_message = len(message)
            new_message = message
            if len_message > self.message_length:
                new_message = new_message[len_message - self.message_length :]

            messages_fixed.append(new_message)

        return messages_fixed

    def get_columns_to_rows_words(self, messages):
        """
        Iterate message length to convert message columns to rows
        :param messages: List of message lists [["es", "","secreto"],["es", "mensaje", ""]]
        :return:
        """
        return [set(messages[:, i]) for i in range(self.message_length)]

    def find_message_encrypted(self, set_words):
        """
        Validates each of the sets of words to determine the word at each position in the message
        :param set_words: sets of words from each message sent on the satellite. Ie, [("","es"), ("un", "es")]
        :return: Return decrypted message. Ie, "este es un mensaje secreto"
        """
        message = ""
        for words in set_words:
            if len(words) > 2:
                raise SatelliteValidationNotSuccess
            decrypted_word = list(filter(lambda x: x != "", list(words)))
            if len(decrypted_word) == 0:
                raise SatelliteValidationNotSuccess
            if len(decrypted_word) > 1:
                raise SatelliteValidationNotSuccess

            message += "{0} ".format(decrypted_word[0])
        return message

    def get_location(self):
        """
        Determines how to process satellite information
        :return: Return the position of the imperial fleet. Ie, [300, 200]
        """
        satellites_length = len(self.satellites)

        if satellites_length == 1:
            raise SatelliteValidationNotSuccess

        if satellites_length == 2:
            return self.find_position_two_satellites()

        return self.find_position_three_satellites()

    def find_position_three_satellites(self):
        """
        Process the information from the 3 satellites and find the position of the imperial fleet.
        :return: Return the position of the imperial fleet. Ie, [300, 200]
        """
        sat_1_2, sat_1_3, sat_2_3 = self.get_combinations_intersection()

        position_fleet = []
        for position in sat_1_2:
            is_intersection_13 = self.validate_each_intersection_points(
                position, sat_1_3
            )
            is_intersection_23 = self.validate_each_intersection_points(
                position, sat_2_3
            )

            if is_intersection_13 and is_intersection_23:
                position_fleet = position

        return position_fleet

    def validate_each_intersection_points(self, position_base, possible_solution):
        """
        Validates if there is an intersection between the points
        :param position_base: x-axis and y-axis positions of the main satellite. Ie, [300, 200]
        :param possible_solution: possible x-axis and y-axis positions of the satellite to be intersected.
            Ie, [[200, 300], [100, 50]]
        :return: Returns a boolean value indicating whether there is intersection or not.
        """
        has_intersection = len(list(filter(
            lambda x: self.is_equal_with_error(x, position_base), possible_solution))
        ) > 0
        return has_intersection

    def is_equal_with_error(self, possible_solution, position_base):
        """
        Configure objects to determine the difference between the base position and the possible solutions
        :param position_base: x-axis and y-axis positions of the main satellite. Ie, [300, 200]
        :param possible_solution: possible x-axis and y-axis positions of the satellite to be intersected.
            Ie, [100, 50]
        :return: Returns a boolean value indicating whether there is intersection or not.
        """
        position_x1 = position_base[0]
        position_x2 = possible_solution[0]

        position_y1 = position_base[1]
        position_y2 = possible_solution[1]

        x_axis = self.validate_position_error_range(position_x1, position_x2)
        y_axis = self.validate_position_error_range(position_y1, position_y2)

        return x_axis and y_axis

    def validate_position_error_range(self, pos_1, pos_2, alpha=0.10):
        """
        Determines the difference between position and position 2 with a degree of error
        :param pos_1: position value of some axis of satellite A. Ie, 200
        :param pos_2: position value of some axis of satellite B. Ie, 300
        :param alpha: The alpha value that determines the degree of error we are allowing. Ie, 0.10
        :return: Boolean value that determines whether the difference is within the error spectrum.
        """
        return abs(abs(pos_1) - abs(pos_2)) <= alpha

    def get_combinations_intersection(self):
        """
        Obtains the possible positions with respect to each satellite by combining the 3 satellites.
        :return: [[200,200], [300, 300]], [[150,400], [100, 400]], [[250,100], [140, 100]]
        """
        sat_1, sat_2, sat_3 = self.satellites
        sat_1_2 = self.get_intersection_radius(sat_1, sat_2)
        sat_1_3 = self.get_intersection_radius(sat_1, sat_3)
        sat_2_3 = self.get_intersection_radius(sat_2, sat_3)
        return sat_1_2, sat_1_3, sat_2_3

    def find_position_two_satellites(self):
        """
        Find the position between two satellites
        :return: Return the position where the imperial fleet is located. Ie, [200, 300]
        """
        location, alter_location = self.get_intersection_radius(
            self.satellites[0], self.satellites[1]
        )

        if location == alter_location:
            return location

        raise SatelliteValidationNotSuccess

    def get_intersection_radius(self, satellite_1, satellite_2):
        """
        Obtains the intersection points of the satellites
        :param satellite_1: Object containing satellite information. Ie,
        {
            "position": [300, 200],
            "distance": 200.5
        }
        :param satellite_2: Object containing satellite information. Ie,
        {
            "position": [500, 300],
            "distance": 100.5
        }
        :return: Possible intersection points. Ie, [[200,200], [300, 300]]
        """
        axis_x1, axis_y1, rad_st1 = self.get_axes_and_radius(satellite_1)
        axis_x2, axis_y2, rad_st2 = self.get_axes_and_radius(satellite_2)

        x_axis_distance = axis_x2 - axis_x1
        y_axis_distance = axis_y2 - axis_y1

        distance = self.get_hypotenuse(x_axis_distance, y_axis_distance)
        self.validate_solutions(distance, rad_st1, rad_st2)
        rad_st3 = self.get_new_distance(distance, rad_st1, rad_st2)

        axis_x3 = axis_x1 + (x_axis_distance + rad_st3 / distance)
        axis_y3 = axis_y1 + (y_axis_distance + rad_st3 / distance)

        dp_x, dp_y = self.get_displacements_intersection_points(
            x_axis_distance, y_axis_distance, rad_st3, distance
        )

        possible_locations = self.get_possible_solutions(axis_x3, dp_x, axis_y3, dp_y)
        return possible_locations

    def get_axes_and_radius(self, satellite):
        """
        Obtains the x-axis and y-axis together with the radius
        :param satellite: Object containing satellite information. Ie,
        {
            "position": [300, 200],
            "distance": 200.5
        }
        :return: Returns each element separately. Ie, 300, 200, 200.5
        """
        x_axis, y_axis = satellite["position"]
        radius = satellite["distance"]

        return x_axis, y_axis, radius

    def get_possible_solutions(self, axis_x3, dp_x, axis_y3, dp_y):
        """
        Obtains the absolute intersection points, calculates the x-coordinates
        of the intersection points and the y-coordinates of the intersection points
        :param axis_x3: Possible x-axis fleet position. Ie, 200
        :param dp_x: displacements of the intersection x-axis. Ie, 100
        :param axis_y3: Possible y-axis fleet position. Ie, 150
        :param dp_y: displacements of the intersection y-axis. Ie, 20
        :return: Return possible solutions
        """
        intersection_x1 = round(axis_x3 + dp_x, 2)
        alter_intersection_x1 = round(axis_x3 - dp_x, 2)

        intersection_y1 = round(axis_y3 + dp_y, 2)
        alter_intersection_y1 = round(axis_y3 - dp_y, 2)

        return [
            [intersection_x1, intersection_y1],
            [alter_intersection_x1, alter_intersection_y1],
        ]

    def get_displacements_intersection_points(
        self, x_axis_distance, y_axis_distance, rad_3, distance
    ):
        """
        Determine the displacements of the intersection points from the new point
        in the direction perpendicular to the line
        :param x_axis_distance: Distance found from the x-axis between satellite 1 and satellite 2. Ie, 10
        :param y_axis_distance: Distance found from the y-axis between satellite 1 and satellite 2. Ie, 10
        :param rad_3: Radius found of possible point 3. Ie, 200.45
        :param distance: Distance found between satellite 1 and satellite 2. Ie, 300.40
        :return: Relative distances of the intersection points along the x and y axes.
        """
        displacements_x = -y_axis_distance * (rad_3 / distance)
        displacements_y = x_axis_distance * (rad_3 / distance)
        return displacements_x, displacements_y

    def get_new_distance(self, distance, rad_1, rad_2):
        """
        Find the new distance from the intersection point
        :param distance: Distance found between satellite 1 and satellite 2. Ie, 300.40
        :param rad_1: Radio del satellite 1. Ie, 100.20.
        :param rad_2: Radio del satellite 2. Ie, 400.20.
        :return: Return new distance. Ie, 500.12.
        """
        return (rad_1**2 - rad_2**2 + distance**2) / (2.0 * distance)

    def validate_solutions(self, distance, rad_1, rad_2):
        """
        Validate that the new distance between the satellites is valid or within the ranges
        :param distance: Distance found between satellite 1 and satellite 2. Ie, 300.40
        :param rad_1: Radio del satellite 1. Ie, 100.20.
        :param rad_2: Radio del satellite 2. Ie, 400.20.
        :return: Returns a boolean value if none of the conditions are met. Ie, True.
        """
        if distance > (rad_1 + rad_2):
            raise SatelliteValidationNotSuccess

        if distance < abs(rad_1 - rad_2):
            raise SatelliteValidationNotSuccess

        if distance == 0 and rad_1 == rad_2:
            raise SatelliteValidationNotSuccess

        return True

    def get_hypotenuse(self, x_axis_distance, y_axis_distance):
        """
        Obtain the hypotenuse between the distance found from the x-axis and y-axis of each satellite
        :param x_axis_distance: Distance found from the x-axis between satellite 1 and satellite 2. Ie, 10
        :param y_axis_distance: Distance found from the y-axis between satellite 1 and satellite 2. Ie, 10
        :return: Return scalar value. Ie, 300
        """
        return math.sqrt(x_axis_distance**2 + y_axis_distance**2)

    def get_parameter_list(self, parameter):
        """
        Returns the parameter of each element within the satellites list
        :param parameter: Parameter to search within the satellites list. Ie, "message".
        :return:
        """
        return [x[parameter] for x in self.satellites]
