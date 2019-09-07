from django.contrib import admin

from wagtail_site_inheritance import models


@admin.register(models.PageInheritanceItem)
class PageInheritanceItemAdmin(admin.ModelAdmin):
    list_display = ["page", "inherited_page", "modified"]
    list_filter = ["modified"]


@admin.register(models.SiteInheritance)
class SiteInheritanceAdmin(admin.ModelAdmin):
    list_display = ["parent", "site"]
    list_filter = ["parent"]
