from django.contrib import admin

from .models import TaggedItem, Charity, Donor, Donation


class TaggedItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(TaggedItem, TaggedItemAdmin)


class CharityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Charity, CharityAdmin)


class DonorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Donor, DonorAdmin)


class DonationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Donation, DonationAdmin)
