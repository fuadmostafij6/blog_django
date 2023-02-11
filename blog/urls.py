from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/posts/', PostView.as_view()),

    path('api/v1/addlike/', AddALike.as_view()),
    path('api/v1/addcomment/', AddComment.as_view()),
    path('api/v1/addreply/', AddReply.as_view()),

]