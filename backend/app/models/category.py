from django.conf import settings
from garpix_page.models import BasePage
from .post import Post


class Category(BasePage):
    template = 'pages/category.html'

    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = Post.on_site.filter(is_active=True, parent=kwargs['object'])
        context.update({
            'posts': posts
        })
        return context

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"
        ordering = ('-created_at',)
