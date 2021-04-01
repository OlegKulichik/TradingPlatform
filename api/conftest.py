import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from trading.models import WatchList, Currency, Item


@pytest.fixture(autouse=True)
def access_db(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='admin', password='123456')
    user.save()
    return user


@pytest.fixture
def get_token(db, api_client, create_user):
    response = api_client.post(
        'http://0.0.0.0:8000/api/token/',
        {
            "username": "admin",
            "password": "123456"
        },
        format='json'
    )
    return response.data['access']


@pytest.fixture
def login(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(get_token))


@pytest.fixture
def create_currency():
    currency = Currency.objects.create(name='Dollar', code='USD',)
    currency.save()
    return currency


@pytest.fixture
def create_item():
    item = Item.objects.create(code="TLSA", name="Tesla", price=600, details="Tesla promotion")
    item.save()
    return item


# @pytest.fixture
# def watchlist_data():
#     data = {"item": []}

# @pytest.fixture
# def create_watchlist():
#     watchlist = WatchList.objects.create(item=2)
#     watchlist.save()
#     return watchlist
