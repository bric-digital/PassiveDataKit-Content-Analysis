# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import SentimentToken, SentimentTokenSource

@admin.register(SentimentToken)
class SentimentTokenAdmin(admin.ModelAdmin):
    list_display = ('source', 'token', 'label', 'score', 'size')
    search_fields = ['source', 'token', 'label']
    list_filter = ('source', 'size',)

@admin.register(SentimentTokenSource)
class SentimentTokenSourceAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'source_id',)
    search_fields = ['source_name', 'source_id', 'description']
