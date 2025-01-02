from django.urls import path
from oauth2_provider.views import TokenView, RevokeTokenView

from . import views

app_name = 'chatbot'

urlpatterns = [
    path("token", TokenView.as_view(), name="token"),
    path('revoke-token', RevokeTokenView.as_view(), name="revoke_token"),

    path('whoami', views.WhoAmI.as_view(), name="who_am_i"),

    path('topics', views.TopicList.as_view(), name="topic_list"),
    path('topics/<slug:slug>', views.TopicDetail.as_view(), name="topic_detail"),

    path('topics/<slug:slug>/datasets', views.DatasetList.as_view(), name="dataset_list"),

    path('topics/<slug:slug>/query', views.Query.as_view(), name="query"),

    path('topics/<slug:slug>/history', views.HistoryList.as_view(), name="history"),

    path('tasks', views.TaskList.as_view(), name="task_list"),
    path('tasks/<uuid:task_id>', views.TaskDetail.as_view(), name="task_detail"),
]
