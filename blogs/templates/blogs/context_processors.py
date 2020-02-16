from blogs.models import Post, Tag, Category, Series

def recent(request):
    result = Post.objects.filter(is_public=True).order_by('-created_at')[:5]
    context = {
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "series": Series.objects.all(),
        "posts": result,
    }
    return context
