from django.shortcuts import render
from .models import News, Category

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

    return render(request, 'index.html', context)


def detail(request, pk):
    news = News.objects.get(pk=pk)
    context = {
        "news": news,
    }
    return render(request, 'detail.html', context)