from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import View

from wagtail.core.models import Page
from wagtail_site_inheritance import models


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
