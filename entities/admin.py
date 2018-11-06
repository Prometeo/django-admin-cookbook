from django.contrib import admin
from .models import Category, Hero, Villain, Origin
# Register your models here.


@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("name", "hero_count", "villain_count")

    def hero_count(self, obj):
        return obj.hero_set.count()

    def villain_count(self, obj):
        return obj.villain_set.count()

    hero_count.admin_order_field = 'hero_count'
    villain_count.admin_order_field = 'villain_count'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass


@admin.register(Villain)
class VillainAdmin(admin.ModelAdmin):
    pass
