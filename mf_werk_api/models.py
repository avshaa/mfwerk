from django.db import models
from django.contrib.auth.models import User

class Part(models.Model):
    name = models.CharField(max_length = 180)
    mf_id = models.CharField(max_length = 180)
    org_file = models.FileField(upload_to='media/', default = '', blank = True)
    branded_file = models.FileField(upload_to='media/', default = '', blank = True)
    branded_file_url = models.CharField(max_length = 180, default = '', blank = True)
    drawing_id = models.JSONField(default = dict)
    material = models.JSONField(default = dict)
    part_ids = models.JSONField(default = dict)
    weight = models.JSONField(default = dict)
    designation = models.JSONField(default = dict)
    general_tolerances = models.JSONField(default = dict)
    completed = models.BooleanField(default = False, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.name
