from django.db import models, transaction, IntegrityError

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address =  models.CharField(max_length=200, blank=True)
    phone =  models.CharField(max_length=16, blank=True)
    email =  models.EmailField(max_length=50, blank=True)
    website = models.URLField(max_length=255, blank=True)
    notes = models.TextField(blank=True, null=True)

    @classmethod
    def create(klass, area_name, area_phone, area_address, area_email, area_website, area_notes):
        area = klass(name=area_name, phone=area_phone, address=area_address, email=area_email,
                     website=area_website, notes=area_notes)
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

class Interface(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True, default=None)
    ip4 = models.IPAddressField(unique=True, null=True, blank=True, default=None)
    vlan = models.IntegerField(max_length=4, null=True, blank=True, default='0')
    mac = models.CharField(max_length=12,unique=True, null=True, blank=True, default=None)
    owner = models.ForeignKey('Asset', null=True, blank=True, default=None)
    partner = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def create(klass,
               interface_name,
               interface_ip4,
               interface_mac,
               interface_vlan,
               interface_owner=None):
        interface = klass(
            name=interface_name,
            ip4=interface_ip4,
            mac=interface_mac,
            vlan=interface_vlan,
            owner=interface_owner,
        )
        return interface

    @classmethod
    def create_full(klass,
               interface_name,
               interface_ip4,
               interface_mac,
               interface_vlan,
               interface_owner=None,
               interface_partner=None):
        interface = klass(
            name=interface_name,
            ip4=interface_ip4,
            mac=interface_mac,
            vlan=interface_vlan,
            owner=interface_owner,
            partner=interface_partner
        )
        return interface

class AssetType(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class Asset(models.Model):
    asset_type = models.ForeignKey(AssetType, default=None)
    alt_id = models.CharField(max_length=50, blank=True, null=True, default=None)
    model = models.CharField(max_length=50, blank=True, null=True, default=None)
    serial = models.CharField(max_length=50, blank=True, null=True, default=None)
    asset_tag = models.CharField(max_length=50, blank=True, null=True, default=None)
    purchase_date = models.DateField(blank=True, null=True, default=None)
    hostname = models.CharField(max_length=50, unique=True)
    primary_interface = models.OneToOneField(Interface, null=True, blank=True)
    console = models.CharField(max_length=50, default=None, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True, null=True, default=None)
    physical_status = models.ForeignKey(PhysicalStatusCode)
    logical_status = models.ForeignKey(LogicalStatusCode)
    rack = models.ForeignKey(Rack,null=True, blank=True, default=None)
    rack_u = models.IntegerField(max_length=3, null=True, blank=True, default=None)
    rack_u_size = models.IntegerField(max_length=3, null=True, blank=True, default=None)
#    pdu0_id = models.ForeignKey('self', null=True, blank=True, default=None)

    def __unicode__(self):
        return self.hostname

    @classmethod
    def create(klass,
               asset_model,
               asset_asset_type,
               asset_serial,
               asset_purchase_date,
               asset_hostname,
               asset_console,
               asset_notes,
               asset_physical_status,
               asset_logical_status,
               asset_rack,
               asset_rack_u,
               asset_rack_u_size,
               asset_alt_id):
        asset = klass(
            model=asset_model,
            asset_type=asset_asset_type,
            serial=asset_serial,
            purchase_date=asset_purchase_date,
            hostname=asset_hostname,
            console=asset_console,
            notes=asset_notes,
            physical_status=asset_physical_status,
            logical_status=asset_logical_status,
            rack=asset_rack,
            rack_u=asset_rack_u,
            rack_u_size=asset_rack_u_size,
            alt_id=asset_alt_id)
        return asset

