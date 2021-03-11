from ..models.post import Post
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(Post)
class PostAdmin(BasePageAdmin):
    pass
