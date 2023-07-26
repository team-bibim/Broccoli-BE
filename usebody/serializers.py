from rest_framework import serializers

from usebody.models import Usebody


class UsebodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usebody
        fields = '__all__'