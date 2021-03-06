from django.http import Http404
from django.utils.translation import ugettext as _
from itertools import chain
from el_pagination.views import AjaxListView
from django.views.generic import DetailView, ListView
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from blog.models import Post
from projects.models import Project
from taggit.models import TaggedItem, Tag

class PostListView(AjaxListView):
    model = Post
    queryset = Post.objects.published()
    #queryset = Post.objects.all()
    context_object_name = 'posts'


class ArchiveListView(ListView):
    context_object_name = 'archiveditems'
    template_name = 'archive_list.html'

    def get_queryset(self):
        posts = Post.objects.published()
        projects = Project.objects.published()
        items = sorted(
            chain(posts, projects),
            key=lambda instance: instance.publish,
            reverse=True)
        return items

class PostListViewByTags(AjaxListView):
    context_object_name = 'taggeditems'
    template_name = 'taggeditem_list.html'
    page_template = 'taggeditem_list_page.html'

    def get_queryset(self):
        project_type = ContentType.objects.get(app_label="projects", model="project")
        post_type = ContentType.objects.get(app_label="blog", model="post")
        tag = Tag.objects.get(name=self.args[0])
        items = TaggedItem.objects.filter(Q(tag=tag, content_type=project_type) | Q(tag=tag, content_type=post_type))
        items = sorted(items, key=lambda x: x.content_object.publish, reverse=True)
        return items

    def get_context_data(self, **kwargs):
        context = super(PostListViewByTags, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        tag = Tag.objects.get(name__in=[self.args[0]])
        context['tag'] = tag
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context


