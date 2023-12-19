from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import index, register, login_view, profile, edit_profile, confirm_delete_account, create_post, delete_post, \
    edit_comment, delete_comment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('confirm_delete_account/', confirm_delete_account, name='confirm_delete_account'),
    path('create_post/', create_post, name = 'create_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)