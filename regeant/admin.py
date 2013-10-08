from django.contrib import admin
from .models import *

class ProducerAdmin(admin.ModelAdmin):
	pass


class BrandAdmin(admin.ModelAdmin):
	pass


class RegeantAdmin(admin.ModelAdmin):
	list_display = ('product_name', 'product_no', 'create_date')

admin.site.register(Producer, ProducerAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Regeant, RegeantAdmin)