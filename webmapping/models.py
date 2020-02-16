from django.db import models
from django.contrib.gis.db import models as gismodels
from django.conf import settings
from django.db.models import Manager as GeoManager
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class Marker(models.Model):
    markerID = models.AutoField(primary_key=True)
    name = models.CharField("Place Name", max_length=40)
    # text=models.CharField("Text",max_length=100)
    mpoint = gismodels.PointField()
    objects = GeoManager()
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True)
    image = ProcessedImageField(
        upload_to="webmapping/place_img/%y/%m/%d/",
        null=True,
        # blank=True,
        processors=[ResizeToFill(200, 200)], format="JPEG", options={'quality': 100}, verbose_name="Picture"
    )
    thumbnail = ImageSpecField(source='image', processors=[
                               ResizeToFill(50, 50)], format="JPEG", options={'quality': 90})
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name="user",
        blank=True, null=True,
    )

    def save(self, *args, **kwargs):
        self.latitude = self.mpoint.y
        self.longitude = self.mpoint.x
        super(Marker, self).save(*args, **kwargs)
