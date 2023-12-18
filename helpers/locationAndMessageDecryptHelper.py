import numpy as np
from app.exceptions.errors import SatelliteValidationNotSuccess


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

    def get_location(self, distances):
        pass

    def get_parameter_list(self, parameter):
        """
        Returns the parameter of each element within the satellites list.
        :param parameter: Parameter to search within the satellites list. Ie, "message".
        :return:
        """
        return [x[parameter] for x in self.satellites]
