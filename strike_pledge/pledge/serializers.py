from rest_framework import serializers
from pledge.models import Pledge

class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = ('id', 'email_hash', 'union')
    