from django.db import models

class ServiceCheck(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=50, unique=True)
    command = models.CharField(max_length=250, null=True, blank=True, default=None)
    result = models.CharField(max_length=250, null=True, blank=True, default=None)

    @classmethod
    def create(klass,
               service_name,
               service_command,
               service_result
    ):
        servicecheck=klass(
            name=service_name,
            command=service_command,
            result=service_result
        )
        return servicecheck

class kssettings(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50, unique=True)
    setting = models.CharField(max_length=255, null=True, blank=True, default=None)
    permanent = models.BooleanField(default=False)

    @classmethod
    def create(klass,
               setting_name,
               setting_setting,
    ):
        kssetting=klass(
            name=setting_name,
            setting=setting_setting)

        return kssetting

class BootOption(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50, null=True, blank=True, default=None)
    kernel = models.CharField(max_length=255, null=True, blank=True, default=None)
    append = models.CharField(max_length=255, null=True, blank=True, default=None)

    @classmethod
    def create(klass,
               option_name,
               option_label,
               option_kernel,
               option_append,
           ):
        bootoption=klass(
            name=option_name,
            label=option_label,
            kernel=option_kernel,
            append=option_append)
        return bootoption
