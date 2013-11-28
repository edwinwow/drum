from time import time
from urlparse import urlparse

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.core.models import Displayable, Ownable
from mezzanine.generic.models import Rating
from mezzanine.generic.fields import RatingField, CommentsField
from django.contrib.gis.db.models import PointField


class Rooms(Displayable, Ownable):
    
    address = models.OneToOne(RoomAddress)
    check_list = models.OneToOne(CheckList)
    addon = models.OneToOne(addon)
    status = models.ChoiceField()
    rating = RatingField()
    comments = CommentsField()
    

    @models.permalink
    def get_absolute_url(self):
        return ("rooms_detail", (), {"slug": self.slug})
        
        
class RoomAddress(models.Model):
    location = PointField(null=False, blank=False)
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=64, default="Zanesville")
    state = USStateField(_("state"), default="OH")
    zip_code = models.CharField(_("zip code"), max_length=5, default="43701")
    country = models.CharField()
    


class RoomForRent(models.Model):
    rooms= ForeignKey(Rooms)
    start_date = models.DateTimeField(auto_now+True)
    publish_date = models.DateTimeField(auto_now=True)
    price = models.IntegreteField()
    internet_status = models.ChoiceField()
    HUB_status = models.ChoiceField()

    
class CheckList(models.Model):
    aircon = models.CharField(choices=CHECKLIST_CHOICES)
    fan = models.CharField(choices=CHECKLIST_CHOICES)
    tv = models.CharField(choices=CHECKLIST_CHOICES)
    door_status = models.CharField(choices=CHECKLIST_CHOICES)
    lock_status = models.CharField(choices=CHECKLIST_CHOICES)
    bed_status = models.CharField(choices=CHECKLIST_CHOICES)
    frezzer_status = models.CharField(choices=CHECKLIST_CHOICES)
    table_status = models.CharField(choices=CHECKLIST_CHOICES)
    chair_status = models.CharField(choices=CHECKLIST_CHOICES)
    celling_status = models.CharField(choices=CHECKLIST_CHOICES)
    mirror_status = models.CharField(choices=CHECKLIST_CHOICES)
    
        
        
class Rental(models.Model):
    
    rooms = models.ForeignKey(Rooms)
    status = models.ChoiceField()
    rent_to = models.ForeignKey("auth.User")
    date_start = models.TimeField(auto.now, null=False, blank=False)
    date_end = models.TimeField(null=True, blank=True)

class Payment(models.Model):
    rooms = models.ForeignKey(Rooms)
    rental_fee = models. integretField()
    rental_fee_status = models.ChoiceField()
    internet_fee = models. integretField()
    internet_fee_status = models.ChoiceField()
    HUB_fee = models. integretField()
    HUB_fee_status = models.ChoiceField()
    

class Profile(models.Model):

    user = models.OneToOneField("auth.User")
    bio = models.TextField(blank=True)
    rating = RatingField()
    comments = CommentsField()

    def __unicode__(self):
        return "%s (%s)" % (self.user)

