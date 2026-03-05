from django.contrib.auth.models import User
from django.template.context_processors import request
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at')
        read_only_fields = ['creator']

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context['request']
        user = request.user

        if not self.instance:
            open_ads = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()

            if open_ads >=10:
                raise serializers.ValidationError(
                    'Нельзя иметь больше 10 открытых объявлений.'
                )
        return data
