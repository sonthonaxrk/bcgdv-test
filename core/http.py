import json
from nameko.web.handlers import HttpRequestHandler
from werkzeug.wrappers import Response
from nameko.exceptions import safe_for_serialization


class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = 400


class InvalidArgumentsError(HttpError):
    error_code = 'INVALID_ARGUMENTS'


class HttpEntrypoint(HttpRequestHandler):
    def response_from_exception(self, exc):
        if isinstance(exc, HttpError):
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': safe_for_serialization(exc),
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


http = HttpEntrypoint.decorator


def jsonify(data, status=200):
    return Response(
        json.dumps(data),
        status=status,
        mimetype='application/json'
    )
