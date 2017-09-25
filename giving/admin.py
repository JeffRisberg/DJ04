from django.contrib import admin

from .models import Charity, Donor, Donation


class CharityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Charity, CharityAdmin)


class DonorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Donor, DonorAdmin)


class DonationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Donation, DonationAdmin)
