from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.utils import timezone

from blog.models import Post


def index(request):
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[0:5]
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id_post):
    post = get_object_or_404(
        Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ),
        pk=id_post
    )
    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    post_list = get_list_or_404(
        Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            category__slug=category_slug,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
    )
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
