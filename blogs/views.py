from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag, Series
from .forms import CommentForm, CategoryForm, SeriesForm, TagForm, PostForm, PostImageForm, PicturesForm
from blogs import utils as blogs_utils


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 6
    ordering = ['-updated_at']
    context_object_name = "object_list"

    def get_queryset(self):
        obj_list = Post.objects.all()

        if self.request.GET.get('category'):
            filtered = self.request.GET.get('category')
            obj_list = obj_list.filter(category__name=filtered)
        if self.request.GET.get('tag'):
            filtered = self.request.GET.get('tag')
            obj_list = obj_list.filter(tag__name=filtered)

        return obj_list.filter(is_public=True).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = blogs_utils.get_category_all()
        tags = blogs_utils.get_tag_all()
        context["categories"] = categories
        context["tags"] = tags
        return context


class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):  # The LoginRequired mixin
    model = Post
    success_url = reverse_lazy('blogs:index')
    template_name = 'blogs/post_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete.')

        return super(DeleteView, self).dispatch(request, *args, **kwargs)


class EditListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 25
    template_name = 'blogs/post_editlist.html'

    def get_queryset(self):
        obj_list = Post.objects.all()
        user = self.request.user
        obj_list = obj_list.filter(author=user)
        return obj_list.order_by('-created_at')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        post_list = Post.objects.all().filter(is_public=True)
        current = Post.objects.get(pk=post_pk)

        if current.series:  # Series化されている場合はそちらでpaginate
            post_list = post_list.filter(series__name=current.series)
        try:
            context["prev_obj"] = post_list.filter(pk__lt=post_pk).order_by('-pk').first()
        except IndexError:
            context["prev_obj"] = False
        try:
            context["next_obj"] = post_list.filter(pk__gt=post_pk).order_by('pk').first()
        except IndexError:
            context["next_obj"] = False

        categories = blogs_utils.get_category_all()
        tags = blogs_utils.get_tag_all()
        context["categories"] = categories
        context["tags"] = tags

        return context


class PostDetailFormView(DetailView, FormMixin):

    model = Post  # shorthand for setting queryset = Post.objects.all()
    template_name = "blogs/post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):  # 有効か否かチェックする
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):  # foreignkeyのひもづけ
        post_pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = Post.objects.get(pk=post_pk)
        self.object.save()
        return redirect('blogs:detail', pk=post_pk)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        # obj = self.get_object()
        # if obj.author != self.request.user:
        #     raise PermissionDenied('You do not have permission.')

        return super().dispatch(request, *args, **kwargs)


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Post
    fields = []
    template_name = 'blogs/post_create.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):  # make autherized post
        post = Post.objects.create(author=self.request.user, is_public=False)
        return_url = reverse('blogs:update', args=[post.id, ])
        return HttpResponseRedirect(return_url)


class AjaxMixin(LoginRequiredMixin):  # to be available at ajax
    ajax = None

    def __init__(self, **kwargs):
        self.ajax = kwargs.get('ajax', None)
        super(AjaxMixin, self).__init__()

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
        return super(AjaxMixin, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        if self.ajax:
            response = super(AjaxMixin, self).form_invalid(form)
            if self.request.is_ajax():
                return JsonResponse(form.errors, status=400)
            else:
                return response
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.object = form.save()
        if self.ajax:
            response = super(AjaxMixin, self).form_valid(form)
            if self.request.is_ajax():
                data = {
                    "comment": "Success!",
                }
                return JsonResponse(data)
            else:
                return response
        else:
            return redirect('blogs:index')


class PostUpdateView(generic.edit.UpdateView, AjaxMixin):
    model = Post
    ajax = True
    template_name = 'blogs/post_update.html'
    form_class = PostForm
    success_url = reverse_lazy('blogs:index')


class PostImageView(generic.edit.UpdateView, AjaxMixin):  # save image asyncronizingly
    model = Post
    ajax = True
    form_class = PostImageForm
    template_name = 'blogs/post_update.html'

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.is_ajax():
            data = {
                # "output_url": self.object.image.url(),
            }
            return JsonResponse(data)


class AddCategoryView(generic.edit.CreateView, AjaxMixin):  # The LoginRequired mixin
    model = Category
    ajax = True
    form_class = CategoryForm
    template_name = 'blogs/post_add.html'


class AddSeriesView(generic.edit.CreateView, AjaxMixin):  # The LoginRequired mixin
    model = Series
    ajax = True
    form_class = SeriesForm
    template_name = 'blogs/post_add.html'


class AddTagView(generic.edit.CreateView, AjaxMixin):  # The LoginRequired mixin
    model = Tag
    ajax = True
    form_class = TagForm
    template_name = 'blogs/post_add.html'


class AddPicturesView(generic.edit.CreateView, AjaxMixin):  # The LoginRequired mixin
    model = Tag
    ajax = True
    form_class = PicturesForm
    template_name = 'blogs/post_add.html'

    # def form_valid(self,form):
    #     super().form_valid(form)
    #     if self.request.is_ajax():
    #         data = {
    #         # "output_url": self.object.image.url(),
    #         }
    #         return JsonResponse(data)
