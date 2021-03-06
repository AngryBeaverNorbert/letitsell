from django.contrib import admin
from .models import Category, Product, Order, OrderItem
from ckeditor.widgets import CKEditorWidget
from django import forms


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'


def make_available(modeladmin, request, queryset):
    queryset.update(status='available')
    make_available.short_description = "Mark selected products as available"


class ProductAdmin(admin.ModelAdmin):

    def make_not_available(self, request, queryset):
        queryset.update(status=DRAFT)

    make_not_available.short_description = "Mark selected products as not available"

    def make_for_sale(self, request, queryset):
        rows_updated = queryset.update(status='sale')
        if rows_updated == 1:
            message_bit = "1 product was"
        else:
            message_bit = "%s products were" % rows_updated
            self.message_user(request, "%s successfully marked as for sale." % message_bit)

    make_for_sale.short_description = "Mark selected stories as for sale"

    list_display = ('name', 'updated', 'was_updated_recently')
    list_filter = ['updated']
    search_fields = ['name']
    ordering = ['updated']
    readonly_fields = ('created', 'updated')
    fieldsets = [
        ('Item', {'fields': [('name', 'slug'), 'category']}),
        ('Date information', {'fields': [('created', 'updated')], 'classes': ['collapse']}),
        ('Description', {'fields': ['description']}),
        ('Medias', {'fields': ['image']}),
        ('Metas', {'fields': ['status', 'price', 'stock']}),
    ]
    prepopulated_fields = {"slug": ("name",)}

    actions = [make_available, 'make_not_available', 'make_for_sale']

    form = ProductAdminForm
    date_hierarchy = 'updated'


admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)






# from django.contrib import admin
# from .models import Category, Product, Order, OrderItem
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     list_display_links = ('name',)
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ['name']
#
#
# admin.site.register(Category, CategoryAdmin)
#
#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}
#     fieldsets = [('Item', {'fields': [('name', 'slug'), 'category', 'description']}),
#                  ('Date information', {'fields': [('created', 'updated')], 'classes': ['collapse']}),
#                  ('Medias', {'fields': ['image']}),
#                  ('Metas', {'fields': [('status', 'price', 'stock')]}),
#                  ]
#     readonly_fields = ('created', 'updated')
#     search_fields = ['name']
#
#
# admin.site.register(Product, ProductAdmin)
#
#
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']
#
#
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
#                     'updated']
#     list_filter = ['paid', 'created', 'updated']
#     inline = [OrderItemInline]
#
#
# admin.site.register(Order, OrderAdmin)
