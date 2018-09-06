from rest_framework import serializers

from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.models.item import ItemClass, ItemInstance
from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.transaction import Transaction


class ItemClassSerializer(serializers.ModelSerializer):

	class Meta:
		model = ItemClass
		fields = '__all__'


class ItemInstanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = ItemInstance
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		fields = '__all__'


class OrderFragmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = OrderFragment
		fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Transaction
		fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Balance
		fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):

	class Meta:
		model = Wallet
		fields = '__all__'
