from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from accounts.models import CustomUser

from .models import Post, Opinion
from .forms import PostForm

def post_list(request):
	posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def posts_author(request, author_name):
	author = User.objects.filter(username=author_name).first()
	posts = Post.objects.filter(author=author)
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.visits += 1
	post.save()
	return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = None
			post.save()
		return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')

def num_users(request):
	num = CustomUser.objects.count()
	return HttpResponse(num, content_type="text/html")

def opinion_up(request, pk):
	post = get_object_or_404(Post, pk=pk)
	opinion, created = Opinion.objects.get_or_create(user=request.user)
	opinion.value = 1
	opinion.save()
	post.opinion.add(opinion)
	post.save()
	return redirect('post_detail', pk=pk)

def opinion_down(request, pk):
	post = get_object_or_404(Post, pk=pk)
	opinion, created = Opinion.objects.get_or_create(user=request.user)
	opinion.value = -1
	opinion.save()
	post.opinion.add(opinion)
	post.save()
	return redirect('post_detail', pk=pk)

def love(request, pk):
	try:
		post = Post.objects.get(pk=pk)
		post.love += 1
		post.save()
		data = {
			'loves': post.love,
			'status': 1
		}
	except:
		data = {
			'status': 0
		}

	return JsonResponse(data)
