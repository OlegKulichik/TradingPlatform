from trading.models import Inventory, Trade


def pass_offer(buyer_offer, seller_offer):
    if (buyer_offer.item != seller_offer.item or buyer_offer.profile == seller_offer.profile or
            buyer_offer.profile.balance < seller_offer.price or buyer_offer.quantity > seller_offer.quantity or
            buyer_offer.price < seller_offer.price):
        return True
    return False


def trade_create(buyer_offer, seller_offer):
    price = seller_offer.price
    item = seller_offer.item
    quantity = seller_offer.quantity
    seller = seller_offer.profile
    buyer = buyer_offer.profile

    inventory, created = Inventory.objects.get_or_create(profile=buyer, item=item)
    inventory.quantity += quantity
    inventory.save(update_fields=('quantity',))

    seller.balance += price
    seller.save(update_fields=('balance',))
    buyer.balance -= price
    buyer.save(update_fields=('balance',))
    seller_offer.is_active = False
    seller_offer.save(update_fields=('is_active',))
    buyer_offer.is_active = False
    buyer_offer.save(update_fields=('is_active',))

    trade = Trade.objects.create(
        item=item,
        seller=seller,
        buyer=buyer,
        quantity=quantity,
        price=price,
        buyer_offer=buyer_offer,
        seller_offer=seller_offer
    )
    trade.save()
