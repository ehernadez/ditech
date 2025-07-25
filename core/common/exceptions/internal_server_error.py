from rest_framework.exceptions import APIException
from rest_framework import status

class InternalServerError(APIException):
	status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	default_detail = "Se produjo un error interno en el servidor."
	default_code = "internal_server_error"