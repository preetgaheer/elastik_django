from django.db import models


class Cook(models.Model):
    name = models.TextField()
    latitude = models.DecimalField(
        null=True, blank=True, decimal_places=15,
        max_digits=19, default=0)
    longitude = models.DecimalField(
        null=True, blank=True, decimal_places=15,
        max_digits=19, default=0)

    @property
    def location_field_indexing(self):
        """Location for indexing.
        Used in Elasticsearch indexing/tests of `geo_distance` native filter.
        """
        return {
            'lat': self.latitude,
            'lon': self.longitude,
        }


class MenuItems(models.Model):
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE)
    name = models.TextField()
