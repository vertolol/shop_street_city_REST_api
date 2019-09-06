from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User
from .serializers import UserSerializer


def get_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    user_details = {}
    user_details['name'] = user.username
    user_details['token'] = token

    return Response(user_details)


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        new_user = User.objects.get(id=serializer.data['id'])

        return get_token(new_user)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    username = request.data['username']
    password = request.data['password']

    try:
        user = User.objects.get(username=username, password=password)
    except:
        res = {'error': 'invalid username or password'}
        return Response(res)

    return get_token(user)
