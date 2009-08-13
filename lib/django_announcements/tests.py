__test__ = {"ANNOUNCEMENT_TESTS": r"""
>>> from models import Announcement

>>> a1 = Announcement.objects.create(title="Down for Maintenance")
>>> a2 = Announcement.objects.create(title="Down for Maintenance Again")
>>> a3 = Announcement.objects.create(title="Down for Maintenance Again And Again", site_wide=True)
>>> a4 = Announcement.objects.create(title="Members Need to Fill Out New Profile Info", members_only=True)
>>> a5 = Announcement.objects.create(title="Expected Down Time", members_only=True, site_wide=True)

# get the announcements that are publically viewable. this is the same as
# calling as using site_wide=False, for_members=False
>>> Announcement.objects.current()
[<Announcement: Down for Maintenance Again And Again>, <Announcement: Down for Maintenance Again>, <Announcement: Down for Maintenance>]

# get just the publically viewable site wide announcements
>>> Announcement.objects.current(site_wide=True)
[<Announcement: Down for Maintenance Again And Again>]

# get the announcements that authenticated users can see.
>>> Announcement.objects.current(for_members=True)
[<Announcement: Expected Down Time>, <Announcement: Members Need to Fill Out New Profile Info>, <Announcement: Down for Maintenance Again And Again>, <Announcement: Down for Maintenance Again>, <Announcement: Down for Maintenance>]

# get just site wide announcements that authenticated users can see.
>>> Announcement.objects.current(site_wide=True, for_members=True)
[<Announcement: Expected Down Time>, <Announcement: Down for Maintenance Again And Again>]

# exclude a couple of announcements from the publically viewabled messages.
>>> Announcement.objects.current(exclude=[a1.pk, a5.pk])
[<Announcement: Down for Maintenance Again And Again>, <Announcement: Down for Maintenance Again>]

"""}
