from django.contrib import admin

from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.models.transaction import Transaction, TicketTransaction
from shop.models.item import ItemClass, ItemInstance, Tickets
from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.teller import Teller
from shop.models.debug import DebugInfo


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


class TicketTransactionInLine(admin.TabularInline):
    model = TicketTransaction
    extra = 1

class TicketAdmin(admin.ModelAdmin):
    inlines=[TicketTransactionInLine]

admin.site.register(Wallet)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Transaction)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderFragment, OrderFragmentAdmin)
admin.site.register(Stall)
admin.site.register(ItemClass, ItemClassAdmin)
admin.site.register(ItemInstance)
admin.site.register(Tickets,TicketAdmin)
admin.site.register(Teller)
admin.site.register(DebugInfo)
admin.site.register(TicketTransaction)
