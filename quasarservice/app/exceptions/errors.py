import json

from werkzeug.exceptions import NotFound, BadRequest


class SatelliteNotFound(BadRequest):
    code = 400
    message = "Satellite not updated because not found"

class SatelliteValidationNotSuccess(NotFound):
    pass

class JsonDecodeError:
    def __init__(self, text):
        self._text = text
        self._message = "The received text couldn't be decoded: %s" % self._text

    @property
    def text(self):
        """The _text property - the getter"""
        return self._text

    @property
    def message(self):
        """The _message property - the getter"""
        return self._message

class JsonSchemaNotFound(NotFound):
    pass

def deserialize_json(text):
    try:
        return json.loads(text)
    except ValueError as e:
        raise JsonDecodeError(text)
