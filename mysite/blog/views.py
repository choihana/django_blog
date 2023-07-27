from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from blog.models import Post
from blog.forms import EmailPostForm,CommentForm



# Create your views here.
class PostLV(ListView):
    model = Post
    template_name = 'blog/post/post_all.html'
    context_object_name = 'posts'
    paginate_by = 3

class PostDV(DetailView):
    model = Post
    template_name = 'blog/post/post_detail.html'

def post_detail(request, pk):
    post = get_object_or_404(Post, id = pk)
    form = CommentForm()
    comments = post.comments.filter(active = True)
    return render(request, 'blog/post/post_detail.html', {'post':post, 'form':form, 'comments':comments})

def post_share(request, pk):
    post = get_object_or_404(Post, id= pk)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} 님이 {post.title}을 추천합니다."
            message = f"{post.title}을 {post_url}에서 읽어보세요.\n"\
                    f"{data['name']}님의 의견: {data['comments']}"
            send_mail(subject,message, 'hanazzang999@gmail.com', [data['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})

@require_POST
def comment(request,pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.post = post
        comment.save()
        return redirect(post)
    comments = post.comments.filter(active=True)
    return render(request, 'blog/post/post_detail.html',{'post':post, 'form':form , 'comments':comments})