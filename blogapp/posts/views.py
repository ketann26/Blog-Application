from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm

# Create your views here.

def posts_create(request):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully Created")

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form
    }

    return render(request,"post_form.html",context)

def posts_detail(request,slug=None):

    instance = get_object_or_404(Post,slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        
    context = {
        'instance': instance,
        'title': instance.title,
    }

    return render(request,"post_detail.html",context)

def posts_list(request):

    queryset_list = Post.objects.active().order_by('-timestamp')
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by('-timestamp')

    search_query = request.GET.get('q')
    if search_query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(user__first_name__icontains=search_query)
            ).distinct()
        
    paginator = Paginator(queryset_list, 2)

    page_req_var = "page"
    page_number = request.GET.get(page_req_var)
    queryset = paginator.get_page(page_number)

    context = {
        "object_list":queryset,
        "title":"List",
        "page_req_var": page_req_var,
    }

    return render(request,"post_list.html",context)


def posts_update(request,slug=None):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Saved")

        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        'instance': instance,
        'title': "Detail",
        'form': form
    }

    return render(request,"post_form.html",context)

def posts_delete(request,slug=None):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request,"Successfully Deleted")

    return redirect('list')