from django.db import models

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address =  models.CharField(max_length=200, blank=True)
    phone =  models.CharField(max_length=16, blank=True)
    email =  models.EmailField(max_length=50, blank=True)
    website = models.URLField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    @classmethod
    def create(klass, area_name, area_phone, area_address, area_email):
        area = klass(name=area_name, phone=area_phone, address=area_address, email=area_email)
        return area

    def __unicode__(self):
        return self.name

class Rack(models.Model):
    area = models.ForeignKey(Area)
    name = models.CharField(max_length=20)
    numu = models.IntegerField()
    def __unicode__(self):
        return self.name

class PhysicalStatusCode(models.Model):
    code = models.CharField(max_length=20)
    def __unicode__(self):
        return self.code

class LogicalStatusCode(models.Model):
    code = models.CharField(max_length=20)
    def __unicode__(self):
        return self.code

class Role(models.Model):
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return self.name

class AssetType(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class Asset(models.Model):
    type = models.ForeignKey(AssetType)
    model = models.CharField(max_length=50, blank=True, null=True, default=None)
    serial = models.CharField(max_length=50, blank=True, null=True, default=None)
    purchase_date = models.DateField(blank=True, null=True, default=None)
    hostname = models.CharField(max_length=50,unique=True)
    eth0_ip = models.IPAddressField(unique=True, null=True, default=None, blank=True)
    eth0_mac = models.CharField(max_length=12,unique=True, null=True, blank=True, default=None)
    eth1_ip = models.IPAddressField(unique=True, null=True, blank=True, default=None)
    eth1_mac = models.CharField(max_length=12,unique=True, null=True, blank=True, default=None)
    console = models.CharField(max_length=50,unique=True,default=None, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True, null=True, default=None)
    physical_status = models.ForeignKey(PhysicalStatusCode)
    logical_status = models.ForeignKey(LogicalStatusCode)
    rack = models.ForeignKey(Rack,null=True,blank=True,default=None)
    rack_u = models.IntegerField(max_length=3,null=True,blank=True,default=None)
    rack_u_size = models.IntegerField(max_length=3,null=True,blank=True,default=None)
    def __unicode__(self):
        return self.hostname

