from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-post/', views.add_post, name='add_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('photos/', views.photo_gallery, name='photo_gallery'),
    path('blog/', views.blog_list, name='blog_list'),
    path('stories/', views.blog_list, {'heading': 'Stories'}, name='stories_list'),
    path('videos/', views.blog_list, {'heading': 'Videos'}, name='videos_list'),
    path('comments/', views.all_comments, name='all_comments'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('profile/', views.user_profile, name='user_profile'),
]