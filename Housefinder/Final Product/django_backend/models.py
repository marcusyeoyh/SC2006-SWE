# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllFlat(models.Model):
    month = models.TextField(blank=True, null=True)
    town = models.TextField(blank=True, null=True)
    flat_type = models.TextField(blank=True, null=True)
    block = models.IntegerField(blank=True, null=True)
    street_name = models.TextField(blank=True, null=True)
    storey_range = models.TextField(blank=True, null=True)
    floor_area_sqm = models.IntegerField(blank=True, null=True)
    flat_model = models.TextField(blank=True, null=True)
    lease_commence_date = models.IntegerField(blank=True, null=True)
    remaining_lease = models.IntegerField(blank=True, null=True)
    resale_price = models.IntegerField(blank=True, null=True)
    combined_blk_street_name = models.TextField(blank=True, null=True)
    onemapapi_name = models.TextField(db_column='oneMapAPI_Name', blank=True, null=True)  # Field name made lowercase.
    time_to_city = models.FloatField(blank=True, null=True)
    nearest_mall = models.IntegerField(blank=True, null=True)
    nearest_school = models.IntegerField(blank=True, null=True)
    nearest_mrt = models.IntegerField(blank=True, null=True)
    storey = models.IntegerField(blank=True, null=True)
    town_premium = models.IntegerField(blank=True, null=True)
    flat_model_premium = models.IntegerField(blank=True, null=True)
    predictedprice = models.FloatField(db_column='PredictedPrice', blank=True, null=True)  # Field name made lowercase.
    likes = models.IntegerField()
    id = models.AutoField(primary_key=True, null=False)

    class Meta:
        managed = False
        db_table = 'all_flat'
