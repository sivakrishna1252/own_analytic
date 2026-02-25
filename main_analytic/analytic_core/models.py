from django.db import models
import uuid





class Trackedsite(models.Model):
    site_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    site_name=models.CharField(max_length=100)
    domain=models.CharField(max_length=100)
    api_key=models.UUIDField(unique=True,db_index=True, default=uuid.uuid4)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.site_name




class Visitor(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    site_id=models.ForeignKey(Trackedsite,on_delete=models.CASCADE)
    visitor_id=models.CharField(max_length=100)
    first_visit=models.DateTimeField(auto_now_add=True)
    last_visit=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.visitor_id





class session(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    site_id=models.ForeignKey(Trackedsite,on_delete=models.CASCADE)
    visitor_id=models.ForeignKey(Visitor,on_delete=models.CASCADE)
    ip_address=models.GenericIPAddressField
    country=models.CharField(max_length=100)
    user_agent=models.TextField()
    start_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField(auto_now=True)
    duration=models.IntegerField()
    browser=models.CharField(max_length=100)
    device=models.CharField(max_length=100)
    os=models.CharField(max_length=100)
    is_bot=models.BooleanField(default=False)
    def __str__(self):
        return self.session_id



class pageview(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    session_id=models.ForeignKey(session,on_delete=models.CASCADE)
    page_url=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.page_url

