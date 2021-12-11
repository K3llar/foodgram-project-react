from rest_framework import status
from rest_framework.response import Response

from djoser import utils
from djoser.views import TokenDestroyView


class CustomTokenDestroyView(TokenDestroyView):

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)
