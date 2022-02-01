from django.db import models
from ...models import FrontInfo, FrontInfoScreenshots
from django.contrib import admin


class FrontInfoScreenshotsAdmin(admin.TabularInline):
    model = FrontInfoScreenshots


@admin.register(FrontInfo)
class FrontInfoAdmin(admin.ModelAdmin):
    inlines = [FrontInfoScreenshotsAdmin]
