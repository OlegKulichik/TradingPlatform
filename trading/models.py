from django.db import models
from rest_framework_simplejwt.state import User
from .enums import OrderType


class Profile(models.Model):
    """User profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"


class StockBase(models.Model):
    """Base"""
    code = models.CharField("Code", max_length=8, unique=True)
    name = models.CharField("Name", max_length=128, unique=True)

    class Meta:
        abstract = True


class Currency(StockBase):
    """Currency"""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class Item(StockBase):
    """Particular stock"""
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(
        Currency,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="item_currency"
    )
    details = models.TextField("Details", blank=True, null=True, max_length=20)

    def __str__(self):
        return f"{self.name}"


class WatchList(models.Model):
    """Current user, favorite list of stocks"""
    profile = models.OneToOneField(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )
    item = models.ManyToManyField(Item, related_name="watchlist_item")

    def __str__(self):
        return f"{self.profile}"


class Inventory(models.Model):
    """The number of stocks a particular user has"""
    profile = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='inventory_user'
    )
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name='inventory_item')
    quantity = models.IntegerField("Stocks quantity", default=0)

    def __str__(self):
        return f"{self.profile}, {self.item}, {self.quantity}"


class Offer(models.Model):
    """Request to buy or sell specific stocks"""
    profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE, related_name='offer_user')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name='offer_item')
    quantity = models.IntegerField("Current quantity")
    order_type = models.PositiveSmallIntegerField(choices=OrderType.choices(), default=1)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.profile}, {self.order_type}, {self.item}"


class Trade(models.Model):
    """Information about a certain transaction"""
    item = models.ForeignKey(
        Item,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='trade_item'
    )
    seller = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade'
    )
    buyer = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade'
    )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    buyer_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade'
    )
    seller_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade'
    )
