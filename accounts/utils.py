import jwt
import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from accounts.models import User
from my_settings import SECRET_KEY


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access = request.COOKIES.get('access')
            # access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access, SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return Response({'message': 'INVALID TOKEN'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'INVALID USER'}, status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, *args, **kwargs)
    return wrapper
