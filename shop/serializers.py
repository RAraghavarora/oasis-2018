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

	customer = serializers.SerializerMethodField()
	items_list = serializers.SerializerMethodField()
	status = serializers.SerializerMethodField()
	timestamp = serializers.SerializerMethodField()
	stall_id = serializers.SerializerMethodField()
	#items = serializers.ReadOnlyField(source="ItemInstanceSerializer")

	def get_stall_id(self, obj):
		return obj.stall.id

	def get_customer(self, obj):
		name = obj.order.customer.user.username
		return name

	def get_items_list(self, obj):
		items_list = []
		for item_instance in obj.items.all():
		       item = {
		       "id" : item_instance.itemclass.id,
		       "name" : item_instance.itemclass.name,
		       "qty" : item_instance.quantity,
		       "price" : item_instance.itemclass.price
		       }
		       items_list.append(item)
		return items_list

	def get_status(self, obj):
		return obj.get_status_display()

	def get_timestamp(self, obj):
		timestamp = obj.order.timestamp
		return timestamp

	class Meta:
		model = OrderFragment
		fields = ('id', 'order', 'customer', 'status', 'items_list', 'timestamp', 'stall_id', 'otp', 'show_otp',)


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

class StallSerializer(serializers.ModelSerializer):

	class Meta:
		model = Stall
		fields = ('id', 'name', 'description',)
