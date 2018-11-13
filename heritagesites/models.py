from django.db import models
from django.urls import reverse


# Create your models here.

# This part has been manually created
class Location(models.Model):
    """
    New model: unesco_heritage_sites.location
    """
    location_id = models.AutoField(primary_key=True)
    planet = models.ForeignKey('Planet', models.DO_NOTHING)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'
        ordering = ["location_id"]
        verbose_name = "UNESCO heritage sites location"
        verbose_name_plural = "UNESCO heritage sites locations"

    def __str__(self):
        return str(self.location_id)

# This part has been manually created
class Planet(models.Model):
    """
    New model: unesco_heritage_sites.planet
    """
    planet_id = models.AutoField(primary_key=True)
    planet_name = models.CharField(unique=True, max_length=50)
    unsd_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "planet"
        ordering = ["planet_name"]
        verbose_name = "UNSD Global World"
        verbose_name_plural = "UNSD Global Worlds"

    def __str__(self):
        return self.planet_name

# This part has been manually created
class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    location = models.ForeignKey('Location', models.DO_NOTHING)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'
        ordering = ["country_area_name"]
        verbose_name = "UNESCO Country Area"
        verbose_name_plural = "UNESCO Country Areas"

    def __str__(self):
        return self.country_area_name

# This part has been manually created
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)
    planet = models.ForeignKey(Planet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'region'
        ordering = ["region_name"]
        verbose_name = "UNESCO Region"
        verbose_name_plural = "UNESCO Regions"

    def __str__(self):
        return self.region_name

# This part has been manually created
class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_region'
        ordering = ["sub_region_name"]
        verbose_name = "UNESCO Sub-Region"
        verbose_name_plural = "UNESCO Sub-Regions"

    def __str__(self):
        return self.sub_region_name

# This part has been manually created
class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'dev_status'
        ordering = ["dev_status_name"]
        verbose_name = "Development Status"
        verbose_name_plural = "Development Statuses"

    def __str__(self):
        return self.dev_status_name

# This part has been manually created
class HeritageSite(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    justification = models.TextField(blank=True, null=True)
    date_inscribed = models.IntegerField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=True)
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', models.DO_NOTHING)
    transboundary = models.IntegerField()
    country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')

    class Meta:
        managed = False
        db_table = 'heritage_site'
        ordering = ["site_name"]
        verbose_name = "Heritage Site"
        verbose_name_plural = "Heritage Sites"

    def get_absolute_url(self):
        return reverse('site_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.site_name

class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, models.DO_NOTHING)
    country_area = models.ForeignKey(CountryArea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_site_jurisdiction'
        ordering = ['heritage_site', 'country_area']
        verbose_name = 'UNESCO Heritage Site Jurisdiction'
        verbose_name_plural = 'UNESCO Heritage Site Jurisdictions'

# This part has been manually created
class HeritageSiteCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'heritage_site_category'
        ordering = ["category_name"]
        verbose_name = "Heritage Site Category"
        verbose_name_plural = "Heritage Site Categories"

    def __str__(self):
        return self.category_name

# This part has been manually created
class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
        ordering = ["intermediate_region_name"]
        verbose_name = "Intermediate Region Name"
        verbose_name_plural = "Intermediate Region Names"

    def __str__(self):
        return self.intermediate_region_name
