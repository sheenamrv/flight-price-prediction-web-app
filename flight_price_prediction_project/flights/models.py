from django.db import models
from zoneinfo import ZoneInfo

EST = ZoneInfo("America/New_York")


class SearchRecord(models.Model):
    origin = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    departure_date = models.DateField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average_live_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    @property
    def searched_at_est(self):
        return self.searched_at.astimezone(EST)

    def __str__(self):
        return f"{self.origin} → {self.destination} on {self.departure_date} (searched {self.searched_at_est:%Y-%m-%d %H:%M %Z})"
