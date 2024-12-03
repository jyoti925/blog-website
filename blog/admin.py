from django.contrib import admin
from .models import Category, blogs, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display=('id', 'category_name', 'created_at', 'updated_at')
    search_fields=('id', 'category_name')

class blogAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'author', 'blog_image', 'short_discription', 'status', 'created_at', 'updated_at')
    # prepopulated_fields={'slug',('title')}
    search_fields=('id','title','category__category_name', 'status')
    # list_editable = ('is_feacherd',)
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(blogs, blogAdmin )
admin.site.register(Comment)