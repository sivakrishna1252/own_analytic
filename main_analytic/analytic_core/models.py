from django.db import models
import secrets
import uuid



class TrackedSite(models.Model):
    site_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, unique=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.site_name







class Visitor(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    site_id=models.ForeignKey(TrackedSite,on_delete=models.CASCADE)
    visitor_id=models.CharField(max_length=100)
    first_visit=models.DateTimeField(auto_now_add=True)
    last_visit=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.visitor_id









class session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site_id = models.ForeignKey(TrackedSite, on_delete=models.CASCADE)
    visitor_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)
    browser = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    is_bot = models.BooleanField(default=False)

    def __str__(self):
        return f"Session {self.id}"










class pageview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.ForeignKey(session, on_delete=models.CASCADE)
    page_url = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.page_url} ({self.session_id.id})"

