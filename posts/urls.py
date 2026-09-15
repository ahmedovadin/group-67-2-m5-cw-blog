from django.urls import path
from . import views
from .constants import LIST_CREATE, RETRIEVE_UPDATE_DESTROY


urlpatterns = [
    # Posts
    path('', views.PostViewSet.as_view(LIST_CREATE)),
    path('<int:id>/', views.PostViewSet.as_view(RETRIEVE_UPDATE_DESTROY)),

    # Comments
    path('<int:id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('comments/<int:id>/', views.CommentDetailAPIView.as_view()),
]