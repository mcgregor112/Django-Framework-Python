from django.urls import path
from app.views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('register/', register_view , name='register_view'),
    path('', login_view , name='login_view'),
    path('forgot_password/', forgot_password_view, name='forgot_password_view'),
    path('profile/', profile_view , name='profile_view'),
    path('update_Profile/', update_profile , name='update_profile'),
    path('logout/', logout_view , name='logout_view'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    # path('library/', library_view, name='library_view'),
    # path('student/', student_view , name='student_view'),
    
]