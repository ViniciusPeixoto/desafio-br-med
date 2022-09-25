from django.contrib import admin

from .models import Euro, Real, Yen


class EuroAdmin(admin.ModelAdmin):
    fields = ["exc_date", "value"]
    list_display = ("iso_code", "exc_date", "value")
    list_filter = ["exc_date"]


class RealAdmin(admin.ModelAdmin):
    fields = ["exc_date", "value"]
    list_display = ("iso_code", "exc_date", "value")
    list_filter = ["exc_date"]


class YenAdmin(admin.ModelAdmin):
    fields = ["exc_date", "value"]
    list_display = ("iso_code", "exc_date", "value")
    list_filter = ["exc_date"]


admin.site.register(Euro, EuroAdmin)
admin.site.register(Real, RealAdmin)
admin.site.register(Yen, YenAdmin)
