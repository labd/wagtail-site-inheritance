from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, FormView, ListView, UpdateView, View)

from wagtail.core.models import Page, Site
from wagtail_site_inheritance import models


class SiteInheritanceListView(ListView):
    model = models.SiteTree
    template_name = 'wagtail_site_inheritance/site_list.html'

    def get_queryset(self):
        return Site.objects.select_related('inheritance_info__parent')


class SiteInheritanceCreateView(CreateView):
    model = models.SiteTree
    fields = ['site', 'parent']


class PageCloneInheritedView(View):
    def get(self, request, parent_pk, pk):
        page = Page.objects.get(pk=pk)
        parent_page = Page.objects.get(pk=parent_pk)

        with transaction.atomic():
            new_page = page.specific.copy(
                recursive=False,
                to=parent_page,
                keep_live=True,
                user=request.user,
            )
            models.SiteInheritanceItem.objects.create(
                page=page,
                inherited_page=new_page
            )
        return redirect('wagtailadmin_pages:edit', new_page.pk)
