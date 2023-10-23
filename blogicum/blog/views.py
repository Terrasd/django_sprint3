from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Post, Category
from blog.constants import COUNT_OF_POSTS_ON_HOMEPAGE


# функция для получения постов (запроса к бд)
def get_queryset_posts():
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    post_list = get_queryset_posts()[:COUNT_OF_POSTS_ON_HOMEPAGE]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id_post):
    post = get_object_or_404(get_queryset_posts(), pk=id_post)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_queryset_posts().filter(category=category)
    return render(request, 'blog/category.html', {'post_list': post_list})
