from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()


def get_token(user: User) -> dict:
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    user_details = dict()
    user_details['name'] = user.username
    user_details['token'] = token

    return user_details


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        new_user = User.objects.get(id=serializer.data['id'])
        token = get_token(new_user)

        return Response(token)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username, password=password)
        except ObjectDoesNotExist:
            res = {'error': 'invalid username or password'}
            return Response(res)

        token = get_token(user)

        return Response(token)
