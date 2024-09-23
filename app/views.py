from django.http import HttpResponse

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, NewsForm
from .models import News, Category

@login_required
def home(request):

    newses = News.objects.filter(is_active=True)
    order_newses = newses.order_by('-update')
    news_banner = newses.filter(is_banner=True).last()
    news_top_story = newses.order_by("-views").first()
    latest_news = newses.order_by("-created")[:8]
    categories = Category.objects.all()
    newses_all = order_newses[:8]
    context = {
        "news_banner": news_banner,
        "news_top_story": news_top_story,
        "latest_newses": latest_news,
        "categories": categories,
        'newses_all': newses_all,

    }

    return render(request, "index.html", context)

@login_required
@permission_required("app.view_news")
def detail(request, pk):
    news = News.objects.get(pk=pk)
    context = {
        "news": news,
    }
    return render(request, "detail.html", context)

def register(request: WSGIRequest):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Saytdan muaffaqiyatli ro'yxatdan o'tdingiz {user.username} \n"
                                      f"Login parolni terib saytga krishingiz mumkin!")
            return redirect("login")
        else:
            print(form.error_messages, "**********")
    else:
        form = RegisterForm()
    context = {
        "form": form,
    }
    return render(request, "register.html", context)

def user_login(request: WSGIRequest):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Saytga xush kelibsiz {user.username}!")
            return redirect("home_page")
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, "login.html", context)

@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "Siz saytdan chiqib ketdingiz!!!")
    return redirect("login")

@login_required
@permission_required("app.change_news", "home_page", raise_exception=True)
def change_news(request):
    return HttpResponse("O'zgartirish")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


@login_required
@permission_required("app.add_news")
def create_news(request: WSGIRequest):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, "Yangilik muvaffaqiyatli qo'shildi!")
            return redirect("home_page")
    else:
        form = NewsForm()
    context = {
        "form": form,
    }
    return render(request, "create.html", context)

# Yangilikni tahrirlash
@login_required
@permission_required("app.change_news")
def update_news(request: WSGIRequest, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangilik muvaffaqiyatli yangilandi!")
            return redirect("detail", pk=news.pk)
    else:
        form = NewsForm(instance=news)
    context = {
        "form": form,
        "news": news,
    }
    return render(request, "create.html", context)

# Yangilikni o'chirish
@login_required
@permission_required("app.delete_news")
def delete_news(request: WSGIRequest, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == "POST":
        news.delete()
        messages.success(request, "Yangilik muvaffaqiyatli o'chirildi!")
        return redirect("home_page")
    context = {
        "news": news,
    }
    return render(request, "delete_form.html", context)

