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
    status = mdoels.ChoiceField()
    rating = RatingField()
    comments = CommentsField()
    

    @models.permalink
    def get_absolute_url(self):
        return ("rooms_detail", (), {"slug": self.slug})
        
class RoomAddress(models.Model):
    location = PointField()
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=64, default="Zanesville")
    state = USStateField(_("state"), default="OH")
    zip_code = models.CharField(_("zip code"), max_length=5, default="43701")
    country = models.CharField()
    
class CheckList()
        
        
class Rental(models.Model):
    
    rooms = models.ForeignKey(Rooms)
    status = models.ChoiceField()
    rent_to = models.ForeignKey("auth.User")
    date_start = models.TimeField(auto.now, null=False, blank=False)
    date_end = models.TimeField(null=True, blank=True)



class Profile(models.Model):

    user = models.OneToOneField("auth.User")
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    karma = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        return "%s (%s)" % (self.user, self.karma)


@receiver(post_save, sender=Rating)
def karma(sender, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2.
    """
    rating = kwargs["instance"]
    value = int(rating.value)
    if not kwargs["created"]:
        value *= 2
    content_object = rating.content_object
    if rating.user != content_object.user:
        queryset = Profile.objects.filter(user=content_object.user)
        queryset.update(karma=models.F("karma") + value)
