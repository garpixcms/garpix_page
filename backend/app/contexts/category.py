from ..models import Post


def context(request, *args, **kwargs):
    posts = Post.on_site.filter(is_active=True, parent=kwargs['object'])
    return {
        'posts': posts
    }
