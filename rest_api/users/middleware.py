from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.exceptions import ValidationError

from rest_framework.authentication import get_authorization_header


class AuthenticationMiddlewareJWT(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        if not request.user.is_authenticated:
            token = get_authorization_header(request).split()[1]
            data = {'token': token}

            try:
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                request.user = valid_data['user']

            except ValidationError as v:
                print("validation error", v)

        return request.user
