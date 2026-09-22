from django.contrib import admin

from airport.models import (
    Airplane,
    AirplaneType,
    Order,
    Ticket,
    Crew,
    Flight,
    Route,
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)


admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Ticket)
admin.site.register(Crew)
admin.site.register(Flight)
admin.site.register(Route)
