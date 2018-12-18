import csv
from django import forms
from django.db.models import Count
from django.contrib import admin
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe
from .models import Category, Hero, Villain, Origin, HeroAcquaintance
# Register your models here.


@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("name", "hero_count", "villain_count")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _hero_count=Count("hero", distinct=True),
            _villain_count=Count("villain", distinct=True),
        )
        return queryset

    def hero_count(self, obj):
        return obj._hero_count

    def villain_count(self, obj):
        return obj._villain_count

    hero_count.admin_order_field = '_hero_count'
    villain_count.admin_order_field = '_villain_count'


class VillainInline(admin.StackedInline):
    model = Villain


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [VillainInline]


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class HeroAcquaintanceInline(admin.TabularInline):
    model = HeroAcquaintance


class HeroForm(forms.ModelForm):
    category_name = forms.CharField()

    class Meta:
        model = Hero
        exclude = ["category"]


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "Category: {}".format(obj.name)


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
    change_list_template = "entities/heroes_changelist.html"
    form = HeroForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(
                name__in=['God', 'Demi God'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        category_name = form.cleaned_data["category_name"]
        category, _ = Category.objects.get_or_create(name=category_name)
        obj.category = category
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal),
            path('mortal/', self.set_mortal),
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    def set_immortal(self, request):
        self.model.objects.all().update(is_immortal=True)
        self.message_user(request, "All heroes are now immortal")
        return HttpResponseRedirect("../")

    def set_mortal(self, request):
        self.model.objects.all().update(is_immortal=False)
        self.message_user(request, "All heroes are now mortal")
        return HttpResponseRedirect("../")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return CategoryChoiceField(queryset=Category.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class IsVeryBenevolentFilter(admin.SimpleListFilter):
        title = 'is_very_benevolent'
        parameter_name = 'is_very_benevolent'

        def lookups(self, request, model_admin):
            return (
                ('Yes', 'Yes'),
                ('No', 'No'),
            )

        def queryset(self, request, queryset):
            value = self.value()
            if value == 'Yes':
                return queryset.filter(benevolence_factor__gt=75)
            elif value == 'No':
                return queryset.exclude(benevolence_factor__gt=75)
            return queryset

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            return actions

    inlines = [HeroAcquaintanceInline]
    list_display = ("name", "is_immortal", "category",
                    "origin", "is_very_benevolent", "children_display",)
    list_filter = ("is_immortal", "category", "origin", IsVeryBenevolentFilter)
    actions = ["mark_immortal", "export_as_csv"]
<<<<<<< HEAD
    readonly_fields = ["headshot_image"]

    def headshot_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.headshot.url,
            width=obj.headshot.width,
            height=obj.headshot.height,
        )
=======
    readonly_fields = ["headshot_image", ]
    exclude = ['added_by']
    # raw_id_fields = ["category"] manage a model with a FK with a large
    # number of objects

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["name", "category"]
        else:
            return []

    def headshot_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.headshot.url,
                width=obj.headshot.width,
                height=obj.headshot.height,
            )
>>>>>>> 9dd497419ac9dc3e272a99a99945595fe2285b02
        )

    def mark_immortal(self, request, queryset):
        queryset.update(is_immortal=True)

    def is_very_benevolent(self, obj):
        return obj.benevolence_factor > 75

    def children_display(self, obj):
        return ", ".join([
            child.name for child in obj.children.all()
        ])
    children_display.short_description = "Children"

    is_very_benevolent.boolean = True
    list_per_page = 250
    # list_per_page = sys.maxsize
    # date_hierarchy = 'added_on'


@admin.register(Villain)
class VillainAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("name", "category", "origin")
    actions = ["export_as_csv"]
    # readonly_fields = ["added_on"]
