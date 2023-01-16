from django.contrib import admin

from ads.models import Ad, Category, Location, User

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)
