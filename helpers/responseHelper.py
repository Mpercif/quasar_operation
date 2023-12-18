from flask import Response


def json_response(data, status=200):
    """
    Prepare data and make the response.
    :param data: dict, the dict data for the response.
    :param status: integer, code status. Ie, 200
    :return: Response, the response object to return.
    """
    data_str = str(data.get("message", "Unexpected error occurred updating data."))
    return Response(response=data_str, status=status, mimetype="application/json")