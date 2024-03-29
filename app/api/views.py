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
from django.conf import settings

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

            case.is_english = data['is_english']
            case.on_address_en = data['on_address_en']
            case.off_address_en = data['off_address_en']

            path = 'https://maps.googleapis.com/maps/api/geocode/json?address='

            case.on_address = data['on_address']
            try:
                onUrl = path+case.on_address+"&key="+settings.API_KEY
                logger.info(onUrl)
                response = requests.get(onUrl)
                # logger.info(response.text)
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
                    onUrl = path+case.off_address+"&key="+settings.API_KEY
                    response = requests.get(onUrl)
                    resp_json_payload = response.json()
                    case.off_lat = resp_json_payload['results'][0]['geometry']['location']['lat']
                    case.off_lng = resp_json_payload['results'][0]['geometry']['location']['lng']
                except Exception as e:
                    print(f'off location error {e}')
                    logger.error(f'off location error {e}')

            try:
                if data['case_type'] != None:
                    case.case_type = data['case_type']
                else:
                    case.case_type = 'direct'

                if data['reserve_date_time'] != None:
                    #2023-02-24 15:00
                    theDateTime = datetime.strptime(data['reserve_date_time'], '%Y-%m-%d %H:%M')
                    case.reserve_date_time = theDateTime
            except Exception as e:
                print(e)

            case.create_time = datetime.now() + timedelta(hours=8)
            case.save()

            return Response({'message': "success create case!",'case_id':case.id})
        else:
            raise APIException("error")
        
class PutCaseFeedbackView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try: 
            case_id = self.request.query_params.get('case_id')
            case = Case.objects.get(id=case_id)

            if case.user == user:
                feedback = data['feedback']
                case.feedback = feedback
                case.save()
                return Response({'message': "ok"})
            else:
                return Response({'message': "this case not belong to you!"})

        except:
            raise APIException("error")
