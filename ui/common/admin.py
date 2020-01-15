from django.contrib import admin

# Register your models here.
from .models import Query, FreqMapEntry, StaticWeight, StatTechnique

class StaticWeightInline(admin.TabularInline):
    model = StaticWeight

class QueryAdmin(admin.ModelAdmin):
    inlines = (StaticWeightInline, )

admin.site.register(Query, QueryAdmin)
