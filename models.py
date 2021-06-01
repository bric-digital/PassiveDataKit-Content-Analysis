# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class SentimentTokenSource(models.Model):
    source_name = models.CharField(max_length=4096)
    source_id = models.SlugField(max_length=4096, unique=True)
    source_description = models.TextField()
    
    min_score = models.FloatField(null=True, blank=True)
    max_score = models.FloatField(null=True, blank=True)

class SentimentToken(models.Model):
    source = models.SlugField(max_length=4096)
    token = models.CharField(max_length=4096)
    label = models.CharField(max_length=4096, default='no-label')
    score = models.FloatField()

    size = models.IntegerField(default=1)
