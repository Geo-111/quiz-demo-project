from django.urls import path
from .views import exam_list


urlpatterns = [
    path('exam-list', view=exam_list, name='exam_list')
]
