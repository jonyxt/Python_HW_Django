from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite, \
    AdvertisementStatusChoices
from advertisements.permissions import IsAdminOrOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        qs = Advertisement.objects.all()
        if user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(
                Q(status=AdvertisementStatusChoices.OPEN) |
                Q(creator=user)
            )
        return qs.filter(status=AdvertisementStatusChoices.OPEN)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", 'destroy']:
            return [IsAdminOrOwner()]
        return [AllowAny()]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        ad = self.get_object()
        if ad.creator == request.user:
            return Response(
                {"detail": "Нельзя добавить своё объявление в избранное."},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            advertisement=ad
        )
        if not created:
            return Response(
                {"detail": "Объявление уже в избранном."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"detail": "Объявление добавлено в избранное."},
                        status=HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related('advertisement')
        ads = [fav.advertisement for fav in favorites]
        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)