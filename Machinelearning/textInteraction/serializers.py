from textInteraction.models import Test
from rest_framework import serializers


class NameSerializer(serializers.ModelSerializer):
    # ModelSerializer和Django中ModelForm功能相似
    # Serializer和Django中Form功能相似
    class Meta:
        model = Test
        # 和"__all__"等价
        fields = ('id', 'name')