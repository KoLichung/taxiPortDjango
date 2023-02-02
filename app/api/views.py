from unicodedata import category
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
# Create your views here.

from modelCore.models import Case
from api import serializers

class UserCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

class GetCurrentAddressView(APIView):

    def get(self, request, format=None):
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')

        # need to query google api for address

        return Response({'message': "this is test address!"})

class PostNewCaseView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        if data!=None:
            case = Case()
            case.user = user
            case.user_name = user.name
            case.user_email = user.email
            case.case_state = 'wait'

            case.on_address = data['on_address']
            # need to query google api for address to lat lng

            case.off_address = data['off_address']
            # need to query google api for address to lat lng

            case.create_time = datetime.now()
            case.save()

            return Response({'message': "success create case!"})
        else:
            raise APIException("error")