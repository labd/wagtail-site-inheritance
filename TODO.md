Things left TODO
================

 - [ ] Cleanup & finish page sync / copy
   - [ ] Add readonly fields which are always synced
 - [x] Remove non modified pages when parent page is unpublished
 - [x] Remove PageInheritanceItem for all inherited pages on page_unpublish signal
 - [ ] Make fields actually readonly in inherited sites
 - [ ] Restrict delete / copy / move actions on inherited sites (not allowed, via PagePermissions?)
 - [ ] All urls should be relative (i.e. copied content should point to the visited site)
 - [ ] Add tests
 - [ ] Add documentation