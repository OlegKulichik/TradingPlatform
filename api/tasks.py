from celery import shared_task
from trading.models import Offer, Item
from api.services import pass_offer, trade_create


@shared_task
def search_offers():
    offers = Offer.objects.filter(is_active=True)
    buyer = [buy for buy in offers if buy.order_type == 1]
    seller = [sel for sel in offers if sel.order_type == 2]
    for buyer_offer in buyer:
        for seller_offer in seller:
            if pass_offer(buyer_offer, seller_offer):
                continue
            else:
                trade_create(buyer_offer, seller_offer)


@shared_task
def item_app_date(item):
    Item.objects.filter(pk__in=item['id']).update(price=item['price'])
