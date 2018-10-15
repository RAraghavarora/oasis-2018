from django.contrib import admin

from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.models.transaction import Transaction
from shop.models.item import ItemClass, ItemInstance, Tickets
from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.teller import Teller


class ItemInstanceInLine(admin.TabularInline):
    model = ItemInstance
    extra = 1


class OrderFragmentInLine(admin.TabularInline):
    model = OrderFragment
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderFragmentInLine]


class ItemClassAdmin(admin.ModelAdmin):
    inlines = [ItemInstanceInLine]


class WalletInLine(admin.TabularInline):
    model = Wallet
    extra = 1


class BalanceAdmin(admin.ModelAdmin):
    inlines = [WalletInLine]


class OrderFragmentAdmin(admin.ModelAdmin):
    inlines = [ItemInstanceInLine]

admin.site.register(Wallet)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Transaction)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderFragment, OrderFragmentAdmin)
admin.site.register(Stall)
admin.site.register(ItemClass, ItemClassAdmin)
admin.site.register(ItemInstance)
admin.site.register(Tickets)
admin.site.register(Teller)
