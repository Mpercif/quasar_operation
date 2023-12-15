from flask import Response


def json_response(data, status=200):
    data_str = str(data.get("message", "Unexpected error occurred updating data."))
    return Response(response=data_str, status=status, mimetype="application/json")