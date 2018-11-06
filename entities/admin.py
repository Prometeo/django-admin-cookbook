from django.contrib import admin
from .models import Category, Hero, Villain
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass


@admin.register(Villain)
class VillainAdmin(admin.ModelAdmin):
    pass
