from django.contrib.auth.models import User
from trading.models import Item


def test_user(create_user):
    assert User.objects.count() == 1


def test_currency_list(api_client, login):
    url = '/api/currency/'
    response = api_client.get(url)
    assert response.status_code == 200


def test_item_list(api_client, login):
    url = '/api/item/'
    response = api_client.get(url)
    assert response.status_code == 200


def test_currency_create(api_client, login):
    url = '/api/currency/'
    currency_data = {
            "code": "USD",
            "name": "Dollar"
        }
    response = api_client.post(url, currency_data, format='json')
    assert response.status_code == 201


def test_item_create(api_client, login, create_currency):
    url = '/api/item/'
    data = {
            "code": "TLSA",
            "name": "Tesla",
            "price": 600,
            "currency": create_currency.id,
            "details": "Tesla promotion"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201


def test_watchlist_get(api_client, login):
    url = '/api/watchlist/get-watchlist/'
    response = api_client.get(url)
    assert response.status_code == 200


def test_auth(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer sfdasfdaf')
    url = '/api/item/'
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_offer(api_client, create_item):
    url_offer = '/api/offer/'
    data_offer = {
        "item": create_item.id,
        "quantity": 100
    }
    response_post = api_client.post(url_offer, data_offer, format='json')
    response_get = api_client.get(url_offer)
    assert response_get.status_code == 200


# def test_watchlist_patch(api_client, create_item, login):
#     url = '/api/watchlist/add-watchlist/'
#     new_watchlist_data = {"item": create_item.id}
#     response = api_client.patch(url, new_watchlist_data, format='json')
#     watchlist_new = response.data
#     assert response.status_code == 200
