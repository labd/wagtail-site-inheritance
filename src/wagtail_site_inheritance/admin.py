from django.contrib import admin

from wagtail_site_inheritance import models


@admin.register(models.PageInheritanceItem)
class PageInheritanceItemAdmin(admin.ModelAdmin):
    list_display = ["page", "inherited_page", "modified"]
    list_filter = ["modified"]
    raw_id_fields = ["page", "inherited_page"]
    search_fields = ["=page__id", "=inherited_page__id"]


@admin.register(models.SiteInheritance)
class SiteInheritanceAdmin(admin.ModelAdmin):
    list_display = ["parent", "site"]
    list_filter = ["parent"]
    raw_id_fields = ["parent", "site"]
