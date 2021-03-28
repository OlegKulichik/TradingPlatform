from .views import (
    CurrencyViewSet,
    ItemViewSet,
    WatchListViewSet,
    InventoryViewSet,
    OfferViewSet,
    TradeViewSet,
    ProfileViewSet
)
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r"currency", CurrencyViewSet)
router.register(r"item", ItemViewSet)
router.register(r"watchlist", WatchListViewSet)
router.register(r"inventory", InventoryViewSet)
router.register(r"offer", OfferViewSet)
router.register(r"trade", TradeViewSet)
router.register(r"profile", ProfileViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]