from django.db import models


class Actioncustomerlist(models.Model):
    userid = models.TextField(db_column='UserID',primary_key=True)  # Field name made lowercase.
    basket_icon_click = models.BigIntegerField(blank=True, null=True)
    basket_add_list = models.BigIntegerField(blank=True, null=True)
    basket_add_detail = models.BigIntegerField(blank=True, null=True)
    sort_by = models.BigIntegerField(blank=True, null=True)
    image_picker = models.BigIntegerField(blank=True, null=True)
    account_page_click = models.BigIntegerField(blank=True, null=True)
    promo_banner_click = models.BigIntegerField(blank=True, null=True)
    detail_wishlist_add = models.BigIntegerField(blank=True, null=True)
    list_size_dropdown = models.BigIntegerField(blank=True, null=True)
    closed_minibasket_click = models.BigIntegerField(blank=True, null=True)
    checked_delivery_detail = models.BigIntegerField(blank=True, null=True)
    checked_returns_detail = models.BigIntegerField(blank=True, null=True)
    sign_in = models.BigIntegerField(blank=True, null=True)
    saw_checkout = models.BigIntegerField(blank=True, null=True)
    saw_sizecharts = models.BigIntegerField(blank=True, null=True)
    saw_delivery = models.BigIntegerField(blank=True, null=True)
    saw_account_upgrade = models.BigIntegerField(blank=True, null=True)
    saw_homepage = models.BigIntegerField(blank=True, null=True)
    device_computer = models.BigIntegerField(blank=True, null=True)
    device_tablet = models.BigIntegerField(blank=True, null=True)
    returning_user = models.BigIntegerField(blank=True, null=True)
    loc_uk = models.BigIntegerField(blank=True, null=True)
    propensity = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actionCustomerList'

    def __str__(self) -> str:
        return f'Customer UserID: {self.userid}'