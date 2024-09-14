from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Kategoriya')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def get_newses(self):
        return News.objects.filter(category=self, is_active=True).order_by('-update')

class Tags(models.Model):
    name = models.CharField(max_length=50, verbose_name='Teg nomi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"

class News(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nomi')
    slug = models.SlugField(max_length=255, verbose_name="Sluglar")
    description = models.TextField(blank=True, null=True, verbose_name="Matni")
    image = models.ImageField(upload_to="news/images/", null=True, blank=True, verbose_name="Rasmi")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    views = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Maqola kategoriyasi")
    tags = models.ManyToManyField(Tags, verbose_name="Teglar")
    is_active = models.BooleanField(default=True, verbose_name="Saytga chiqarish")
    is_banner = models.BooleanField(default=True, verbose_name="Bannerga chiqarish")
    is_weekly = models.BooleanField(default=True, verbose_name="Haftalik yangiliklar")
    update = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "https://answers-afd.microsoft.com/static/images/image-not-found.jpg"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"