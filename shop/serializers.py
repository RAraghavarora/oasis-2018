from rest_framework import serializers

from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.models.item import ItemClass, ItemInstance
from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.transaction import Transaction

'''
class ItemInstanceSerializer(serializers.ModelSerializer):

	name = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()

	def get_name(self, obj):
		name = obj.itemclass.name

		if not obj.size.name == 'NA':
		       name += (' ' + obj.size.name)
		               
		return name

	def get_description(self, obj):
		return obj.itemclass.description

	class Meta:
		model = Item
		fields = ('id', 'name', 'size', 'color', 'itemtype', 'price', 'is_available', 'is_veg')         
'''

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

	customer = serializers.SerializerMethodField()
	quantity = serializers.SerializerMethodField()
	timestamp = serializers.SerializerMethodField()

	def get_customer(self, obj):
		name = obj.order.customer.wallet.user.name                              
		return name

	def get_quantity(self, obj):
		quantity = {}
		for item_instance in obj.items:
		       quantity[item_instance.itemclass.id] = item_instance.quantity
		return quantity

	def get_timestamp(self, obj):
		timestamp = obj.order.timestamp
		return timestamp

	class Meta:
		model = OrderFragment
		fields = '__all__'


class NestedOrderSerializer(serializers.ModelSerializer):
	fragments = OrderFragmentSerializer(many=True)

	class Meta:
		model = Order
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
