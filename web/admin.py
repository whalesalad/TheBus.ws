from django.contrib import admin

from thebus.web import models as web_models

class UpdateAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'published', )
    prepopulated_fields = { 'slug': ('title', ) }
    search_fields = ('title', 'slug', 'url', )

admin.site.register(web_models.Update, UpdateAdmin)