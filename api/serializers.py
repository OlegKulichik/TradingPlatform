from trading.models import Currency, Item, WatchList, Offer, Trade, Inventory, Profile
from rest_framework import serializers
from trading.enums import OrderType


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        item = validated_data['item']
        instance.item.add(*item)
        return instance

    class Meta:
        model = WatchList
        read_only_fields = ('profile', )
        exclude = ('profile', )


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        exclude = ('profile', )
        extra_kwargs = {'item': {'required': True}}

    def create(self, validated_data):
        profile = self.context['request'].user.profile
        validated_data['profile'] = profile
        item = validated_data['item']
        inventory = Inventory.objects.filter(profile=profile, item=item).exists()
        if inventory:
            raise serializers.ValidationError("Inventory with this Item already exists")

        return super(InventorySerializer, self).create(validated_data)


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('profile',)
        extra_kwargs = {'currency': {'required': True}}

    def create(self, validated_data):
        profile = self.context['request'].user.profile
        validated_data['profile'] = profile
        order_type = validated_data['order_type']

        if order_type == OrderType.SELLER.value:
            item = validated_data['item']
            quantity = validated_data['quantity']
            try:
                inventory = Inventory.objects.get(profile=profile, item=item)
                if inventory.quantity < quantity:
                    raise serializers.ValidationError("The number of shares is less than requested")
                inventory.quantity -= quantity
                inventory.save(update_fields=('quantity',))
            except Inventory.DoesNotExist:
                serializers.ValidationError("No inventory")
        else:
            raise serializers.ValidationError("You are a buyer")
        return super(OfferSerializer, self).create(validated_data)


class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'

