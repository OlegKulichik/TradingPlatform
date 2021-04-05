from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.tasks import item_app_date
from trading.models import (
    Currency,
    Item,
    WatchList,
    Offer,
    Trade,
    Inventory,
    Profile
)
from .serializers import (
    CurrencySerializer,
    ItemSerializer,
    WatchListSerializer,
    InventorySerializer,
    OfferSerializer,
    TradeSerializer,
    ProfileSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(methods=('post', ), detail=False, url_path='post-item-v1')
    def post_items(self, request, *args, **kwargs):
        item = Item.objects.filter(pk__in=request.data['id'])
        serializer = ItemSerializer(item, data=request.data)
        serializer.update(item, request.data)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('post', ), detail=False, url_path='post-item-v2')
    def post_item(self, request, *args, **kwargs):
        Item.objects.filter(pk__in=request.data['id']).update(price=request.data['price'])
        return Response(status=status.HTTP_200_OK)

    @action(methods=('post', ), detail=False, url_path='post-item-v3')
    def post_item(self, request, *args, **kwargs):
        item = request.data
        item_app_date.apply_async([item])
        return Response(status=status.HTTP_200_OK)


class WatchListViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=('get', ), detail=False, url_path='get-watchlist')
    def get_watchlist(self, request, *args, **kwargs):
        watchlist = request.user.profile.watchlist
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('patch', ), detail=False, url_path='add-watchlist')
    def patch_watchlist(self, request, *args, **kwargs):
        watchlist = request.user.profile.watchlist
        serializer = WatchListSerializer(watchlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(watchlist, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

