from rest_framework.exceptions import APIException


class Conflict(APIException):
    status_code = 409
    default_detail = 'Conflict detected.'
    default_code = 'conflict'


class PreconditionFailed(APIException):
    status_code = 412
    default_detail = 'Access to the target resource denied.'
    default_code = 'precondition_failed'


class UnprocessableEntity(APIException):
    status_code = 422
    default_detail = 'Provided data cannot be processed.'
    default_code = 'unprocessable_entity'
