from django.db import models
from django.urls import reverse
from django.db.models import F

# Create your models here.

# This part has been manually created
class Location(models.Model):
    """
    New model: unesco_heritage_sites.location
    """
    location_id = models.AutoField(primary_key=True)
    planet = models.ForeignKey('Planet', on_delete=models.PROTECT)
    region = models.ForeignKey('Region', on_delete=models.PROTECT, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', on_delete=models.PROTECT, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', on_delete=models.PROTECT, blank=True, null=True)

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
    location = models.ForeignKey('Location', on_delete=models.PROTECT)
    dev_status = models.ForeignKey('DevStatus', on_delete=models.PROTECT, blank=True, null=True)

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
    planet = models.ForeignKey(Planet, on_delete=models.PROTECT)

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
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

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
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', on_delete=models.PROTECT)
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

    @property
    def country_area_names(self):
        """
        Returns a list of UNSD countries/areas (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a country/area (e.g., Old City
        Walls of Jerusalem). In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        countries = self.country_area.select_related('location').order_by('country_area_name')

        names = []
        for country in countries:
            name = country.country_area_name
            if name is None:
                continue
            iso_code = country.iso_alpha3_code

            name_and_code = ''.join([name, ' (', iso_code, ')'])
            if name_and_code not in names:
                names.append(name_and_code)

        return ', '.join(names)

    @property
    def region_names(self):
        """
        Returns a list of UNSD regions (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a region. In such cases the
        Queryset will return as <QuerySet [None]> and the list will need to be checked for
        None or a TypeError (sequence item 0: expected str instance, NoneType found) runtime
        error will be thrown.
        :return: string
        """

        # Add code that uses self to retrieve a QuerySet composed of regions, then loops over it
        # building a list of region names, before returning a comma-delimited string of names.
        regions = self.country_area.select_related('location').values(name=F('location__region__region_name'))
        names = []
        for region in regions:
            name = region['name'] # using .values() turns it to dictionary
            if name is None:
                continue
            if name not in names:
                names.append(name)
        return ', '.join(names)

    @property
    def sub_region_names(self):
        """
		Returns a list of UNSD subregions (names only) associated with a Heritage Site.
		Note that not all Heritage Sites are associated with a subregion. In such cases the
		Queryset will return as <QuerySet [None]> and the list will need to be checked for
		None or a TypeError (sequence item 0: expected str instance, NoneType found) runtime
		error will be thrown.
		:return: string
		"""

		# Add code that uses self to retrieve a QuerySet, then loops over it building a list of
		# sub region names, before returning a comma-delimited string of names using the string
		# join method.
        sub_regions = self.country_area.select_related('location').values(name=F('location__sub_region__sub_region_name'))
        names = []
        for sub_region in sub_regions:
            name = sub_region['name'] # using .values() turns it to dictionary
            if name is None:
                continue
            if name not in names:
                names.append(name)
        return ', '.join(names)

    @property
    def intermediate_region_names(self):
        """
        Returns a list of UNSD intermediate regions (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with an intermediate region. In such
        cases the Queryset will return as <QuerySet [None]> and the list will need to be
        checked for None or a TypeError (sequence item 0: expected str instance, NoneType found)
        runtime error will be thrown.
        :return: string
        """

		# Add code that uses self to retrieve a QuerySet, then loops over it building a list of
		# intermediate region names, before returning a comma-delimited string of names using the
		# string join method.
        intermediate_regions = self.country_area.select_related('location').values(name=F('location__intermediate_region__intermediate_region_name'))

        names=[]
        for intermediate_region in intermediate_regions:
            name = intermediate_region['name'] # using .values() turns it to dictionary
            if name is None:
                continue
            if name not in names:
                names.append(name)
        return ', '.join(names)

class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, on_delete=models.CASCADE)
    country_area = models.ForeignKey(CountryArea, on_delete=models.CASCADE)

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
    sub_region = models.ForeignKey('SubRegion', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
        ordering = ["intermediate_region_name"]
        verbose_name = "Intermediate Region Name"
        verbose_name_plural = "Intermediate Region Names"

    def __str__(self):
        return self.intermediate_region_name
