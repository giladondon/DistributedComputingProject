from django.contrib import admin
from .models import Feature
from django.forms import TextInput, Textarea
from django.db import models


class FeatureAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':70})},
    }

admin.site.register(Feature, FeatureAdmin)
