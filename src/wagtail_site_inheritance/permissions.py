from wagtail.contrib.modeladmin.helpers import PermissionHelper


class SiteInheritancePermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        """
        Do not allow any edit actions.

        Editing SiteInheritance objects isn't possible at the moment since it will give
        us a lot of weird results, f.e. a site that inherits from 2 sites.
        """
        return False
