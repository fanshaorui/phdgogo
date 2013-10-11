from django.contrib import admin
from .models import Provider

class ProviderAdmin(admin.ModelAdmin):
	pass

admin.site.register(Provider,ProviderAdmin)