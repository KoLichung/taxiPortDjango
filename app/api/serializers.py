from rest_framework import serializers
from modelCore.models import Case


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ('id',)