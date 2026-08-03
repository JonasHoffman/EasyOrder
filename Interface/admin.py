from django.contrib import admin
from Interface.models import MenuItem,NavTop
# Register your models here.
@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    ...

@admin.register(NavTop)
class NavTopAdmin(admin.ModelAdmin):
    ...