from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Tags, News

admin.site.register(Category)
admin.site.register(Tags)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'views', 'category', 'is_active', 'is_banner', 'is_weekly', 'get_image')
    list_display_links = ('pk', 'name',)
    list_editable = ('category', 'is_active', 'is_banner', 'is_weekly',)

    def get_image(self, news):
        if news.image:
            return mark_safe(f'<img src="{news.image.url}" width="100px">')
        else:
            return mark_safe(f'<img src="https://answers-afd.microsoft.com/static/images/image-not-found.jpg" width="75px">')

    get_image.short_description = "Rasmi"

    prepopulated_fields = {"slug": ("name", )}