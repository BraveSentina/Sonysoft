from django.urls import path
from .views import *

app_name = 'student'

urlpatterns = [
    path('assessment/',assessment_page,name='assessment_page'),
    path('check_compatibility/',check_compatibility_page,name='check_compatibility_page'),
    path('rules/',rules_page,name='rules_page'),
    path('end/',end_page,name='end_page'),

    # Json handlers
    path('save_option/',saveOption,name='save_option'),
    path('get_remaining_duration',get_remaining_duration,name='get_remaining_duration'),
    path('enable_submit/',enableSubmit,name='enable_submit'),
    path('is_user_banned/',is_user_banned,name='is_user_banned'),
    path('ban_user/',ban_user,name='ban_user'),
]   