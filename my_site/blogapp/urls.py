from django.urls import path

from .views import ArticleDetailView, ArticleListView, LatestArticlesFeed

app_name: str = "blogapp"

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article_details"),
    path("articles/latest/feed/", LatestArticlesFeed(), name="articles_feed"),
]
