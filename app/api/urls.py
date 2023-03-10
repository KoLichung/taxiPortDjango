from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('user_cases', views.UserCaseViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('get_current_address', views.GetCurrentAddressView.as_view()),
    path('post_new_case', views.PostNewCaseView.as_view()),
    path('get_current_case_state', views.GetCurrentCaseStateView.as_view()),
    path('put_case_feedback', views.PutCaseFeedbackView.as_view()),
]