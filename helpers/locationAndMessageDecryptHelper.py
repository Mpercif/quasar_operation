import numpy as np
from app.exceptions.errors import SatelliteValidationNotSuccess


class LocationAndMessageDecryptHelper(object):
    def __init__(self, satellites):
        self.satellites = satellites
        self.message_length = 0
        self.message = ""

    def get_message(self, messages=None):
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
        return np.min([len(x) for x in messages])

    def remove_offset_messages(self, messages):
        messages_fixed = []
        for message in messages:
            len_message = len(message)
            new_message = message
            if len_message > self.message_length:
                new_message = new_message[len_message - self.message_length:]

            messages_fixed.append(new_message)

        return messages_fixed

    def get_columns_to_rows_words(self, messages):
        return [set(messages[:, i]) for i in range(self.message_length)]

    def find_message_encrypted(self, set_words):
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
        return [x[parameter] for x in self.satellites]
