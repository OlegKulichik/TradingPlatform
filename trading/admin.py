from django.contrib import admin
from .models import Currency, Item, WatchList, Inventory, Offer, Trade, Profile

admin.site.register(Profile)
admin.site.register(Currency)
admin.site.register(Item)
admin.site.register(WatchList)
admin.site.register(Inventory)
admin.site.register(Offer)
admin.site.register(Trade)