from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        from shop.signals.balance import balanceFirebaseUpdate,
                                        balanceFirebaseDelete
