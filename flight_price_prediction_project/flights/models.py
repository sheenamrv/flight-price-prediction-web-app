from django.db import models


class SearchRecord(models.Model):
    origin = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    departure_date = models.DateField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average_live_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} → {self.destination} on {self.departure_date} (searched {self.searched_at:%Y-%m-%d %H:%M})"
