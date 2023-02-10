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
import logging

from modelCore.models import Case
from api import serializers

logger = logging.getLogger(__file__)

class UserCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

# not used
class GetCurrentAddressView(APIView):

    def get(self, request, format=None):
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')

        # need to query google api for address

        return Response({'message': "this is test address!"})

class GetCurrentCaseStateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        case_id = self.request.query_params.get('case_id')
        
        case = Case.objects.get(id=case_id)
        if case.user == user:
            serializer = serializers.CaseSerializer(case)
            return Response(serializer.data)
        else:
            raise APIException("error")


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
            try:
                onUrl = path+case.on_address+"&key="+"AIzaSyCdP86OffSMXL82nbHA0l6K0W2xrdZ5xLk"
                response = requests.get(onUrl)
                resp_json_payload = response.json()
                case.on_lat = resp_json_payload['results'][0]['geometry']['location']['lat']
                case.on_lng = resp_json_payload['results'][0]['geometry']['location']['lng']
            except Exception as e:
                print(f'on location error {e}')
                logger.error(f'on location error {e}')
                raise APIException("error")

            if data['off_address'] != None and data['off_address'] != '':
                case.off_address = data['off_address']
                try:
                    onUrl = path+case.off_address+"&key="+"AIzaSyCdP86OffSMXL82nbHA0l6K0W2xrdZ5xLk"
                    response = requests.get(onUrl)
                    resp_json_payload = response.json()
                    case.off_lat = resp_json_payload['results'][0]['geometry']['location']['lat']
                    case.off_lng = resp_json_payload['results'][0]['geometry']['location']['lng']
                except Exception as e:
                    print(f'off location error {e}')
                    logger.error(f'off location error {e}')

            case.create_time = datetime.now() + timedelta(hours=8)
            case.save()

            return Response({'message': "success create case!",'case_id':case.id})
        else:
            raise APIException("error")