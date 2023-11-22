from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from airport.models import Passenger, Airline, Aircraft, Flight, Airport


@admin.register(Passenger)
class PassengerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("passport",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("passport",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "passport",
                    )
                },
            ),
        )
    )


@admin.register(Aircraft)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("type",)
    list_filter = ("airline",)


admin.site.register(Airline)

admin.site.register(Flight)

admin.site.register(Airport)
