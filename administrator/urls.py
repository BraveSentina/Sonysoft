from django.urls import path
from .views import *

app_name = 'administrator'

urlpatterns = [
    path('',dashboard_page,name='dashboard_page'),
    path('logs/',logs_page,name='logs_page'),
    path('view_all_tests/',view_all_tests_page,name='view_all_tests_page'),
    path('test_creator/',test_creator_page,name='test_creator_page'),
    path('monitor/',monitor_page,name='monitor_page'),
    # path('add_candidate/',add_candidate_page,name='add_candidate_page'),
    # path('view_candidates/',view_candidates_page,name='view_candidates_page'),
    path('results/<str:test_id>/',results_page,name='results_page'),
    path('test_editor/<str:test_id>/<str:q_id>/',test_editor_page,name='test_editor_page'),
    path('test_permission/',test_permission,name='test_permission_page'),


    path('delete_test/<str:id>/',delete_test,name='delete_test'),
    path('delete_all_question_images/<str:test_id>/<str:q_id>/',delete_all_question_images,name='delete_all_question_images'),
    path('delete_option/<str:test_id>/<str:q_id>/<str:option_id>/',delete_option,name='delete_option'),
    path('delete_question/<str:q_id>/',delete_question,name='delete_question'),
    path('set_is_ongoing_to_true/<str:test_id>/',set_is_ongoing_to_true,name='set_is_ongoing_to_true'),
    path('is_test_ongoing/<str:test_id>/',is_test_ongoing,name='is_test_ongoing'),
    path('is_any_test_ongoing',is_any_test_ongoing,name='is_any_test_ongoing'),
    path('reset_is_ongoing_to_false',reset_is_ongoing_to_false,name='reset_is_ongoing_to_false'),
    path('allow_registeration/<str:test_id>/',allow_registeration,name='allow_registeration'),
    path('grant_or_revoke_test_permission/<str:username>/',grant_or_revoke_test_permission,name='grant_or_revoke_test_permission'),
    # path('ban_user/<str:user_id>/',ban_user,name='ban_user'),
    path('remove_ban/<str:user_id>/',remove_ban,name='remove_ban'),
    path('is_any_test_ongoing_json/',is_any_test_ongoing_json,name='is_any_test_ongoing_json'),

]