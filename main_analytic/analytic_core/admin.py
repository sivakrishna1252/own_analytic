from django.contrib import admin
from .models import TrackedSite, Visitor, session, pageview

@admin.register(TrackedSite)
class TrackedSiteAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'domain', 'site_id', 'created_at')
    search_fields = ('site_name', 'domain')

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_id', 'site_id', 'first_visit', 'last_visit')
    list_filter = ('site_id',)
    search_fields = ('visitor_id',)

@admin.register(session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_id', 'visitor_id', 'country', 'start_time', 'duration', 'is_bot')
    list_filter = ('site_id', 'is_bot', 'country')
    search_fields = ('id', 'ip_address')

@admin.register(pageview)
class PageviewAdmin(admin.ModelAdmin):
    list_display = ('page_url', 'session_id', 'site_id', 'timestamp', 'duration')
    list_filter = ('site_id', 'session_id')
    search_fields = ('page_url',)
