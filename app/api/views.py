from unicodedata import category
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
import requests
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

            path = 'https://maps.googleapis.com/maps/api/geocode/json?address='

            case.on_address = data['on_address']
            # need to query google api for address to lat lng
            onUrl = path+case.on_address+"&key="+"AIzaSyCdP86OffSMXL82nbHA0l6K0W2xrdZ5xLk"
            response = requests.get(onUrl)
            resp_json_payload = response.json()
            case.on_lat = resp_json_payload['results'][0]['geometry']['location']['lat']
            case.on_lng = resp_json_payload['results'][0]['geometry']['location']['lng']

            if data['off_address'] != None:
                case.off_address = data['off_address']
                onUrl = path+case.off_address+"&key="+"AIzaSyCdP86OffSMXL82nbHA0l6K0W2xrdZ5xLk"
                response = requests.get(onUrl)
                resp_json_payload = response.json()
                case.off_lat = resp_json_payload['results'][0]['geometry']['location']['lat']
                case.off_lng = resp_json_payload['results'][0]['geometry']['location']['lng']

            case.create_time = datetime.now()
            case.save()

            return Response({'message': "success create case!"})
        else:
            raise APIException("error")