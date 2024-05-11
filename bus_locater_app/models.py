from django.db import models

class BusRoute(models.Model):
    bus_route_name = models.CharField(max_length=200)
    bus_number = models.IntegerField()

    def __str__(self):
        return self.bus_route_name

    class Meta:
        ordering = ['bus_route_name']
