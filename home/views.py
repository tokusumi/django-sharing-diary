from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.models import Post
from webmapping.models import Marker


class HomeView(LoginRequiredMixin, generic.base.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(is_public=True).order_by('-updated_at')[:4]
        context["marker_lists"] = Marker.objects.all()
        return context
