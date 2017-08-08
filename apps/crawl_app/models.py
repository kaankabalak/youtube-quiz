# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    views = models.FloatField()
    release_date = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'id: '+str(self.id)+', title: '+str(self.title)