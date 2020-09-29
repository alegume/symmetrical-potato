from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from accounts.models import CustomUser
from .models import Post, Opinion
from .forms import PostForm, ContatoForm
from .serializers import PostSerializer

@csrf_exempt
def rest_post_list(request):
    if request.method == 'GET':
        posts = Post.objects.filter().order_by('-created_date')
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def rest_post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    # post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)

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
		messages.success(request, 'Post criado com sucesso', extra_tags='alert')
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
			messages.success(request, 'Post editado com sucesso')
			return redirect('post_detail', pk=post.pk)
		else:
			messages.warning(request, 'Problemas ao editar o Post')
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

	## Pra converter uma lista simples
	# return JsonResponse([1, 2, 3, 4], safe=False)
	return JsonResponse(data)

def contato(request):
	if request.method == 'GET':
		email_form = ContatoForm()
	else:
		email_form = ContatoForm(request.POST)
		if email_form.is_valid():
			emissor = email_form.cleaned_data['emissor']
			assunto = email_form.cleaned_data['assunto']
			msg = email_form.cleaned_data['msg']

			try:
				send_mail(assunto, msg, emissor, ['alexandreabreu@comp.ufla.br'])
			except BadHeaderError:
				return HttpResponse("Erro =/")
			return redirect('obg')
	return render(request, 'blog/contato.html', {'form': email_form})

def obg(request):
	return HttpResponse("<h2>Obrigado pela mensagem!!!</h2>")
