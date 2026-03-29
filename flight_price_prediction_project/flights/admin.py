from django.contrib import admin
from .models import SearchRecord


@admin.register(SearchRecord)
class SearchRecordAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "departure_date", "predicted_price", "average_live_price", "searched_at")
    list_filter = ("origin", "destination")
    ordering = ("-searched_at",)
