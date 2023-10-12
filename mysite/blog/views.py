from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views.decorators.http import require_POST


# пресдставление на основе функции
def post_list(request):
    post_list = Post.published.all()
    # Постраничная разбивака - 3 поста на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number - не число, выдать первую страницу blog/?page=notint
        posts = paginator.page(1)
    except EmptyPage:
        # если страницы пагинатора не существует, выдать последнюю существующую
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список  активных комментариев к посту
    comments = post.comments.filter(active=True)
    # Форма для комментариев пользоавтелями
    form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # комментарий был отправлен
    form = CommentForm(data = request.POST)
    if form.is_valid():
        # Создание объекта клаасса Comment, не сохраяняя его в БД
        # Объект создается, но его можно видоизменить перед сохранением в БД
        comment = form.save(commit=False)
        # назначение поста комментарию
        comment.post = post
        # сохраниение комментария в БД
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})

