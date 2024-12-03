from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from blog import views as BlogsView

urlpatterns = [
    path('',views.home, name='home'),
    path('category/<int:category_id>',views.posts_by_category, name='posts_by_category'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('blogs/<slug:slug>/', BlogsView.blogPage, name='blogPage'),
    path('blogPage/search/',BlogsView.search, name='search')
   
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)