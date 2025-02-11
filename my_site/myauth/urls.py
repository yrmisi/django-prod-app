from django.urls import path

from .views import (
    AboutMeUpdateView,
    AboutMeView,
    FooBarView,
    HelloView,
    MyLoginView,
    MyLogoutPage,
    ProfileDetailView,
    ProfilesListView,
    RegisterView,
    get_cookie_view,
    get_session_view,
    set_cookie_view,
    set_session_view,
)

app_name: str = "myauth"

urlpatterns = [
    # path("login/", login_view, name="login"),
    # path(
    #     "login/",
    #     LoginView.as_view(template_name="myauth/login.html", redirect_authenticated_user=True),
    #     name="login",
    # ),
    path("hello/", HelloView.as_view(), name="hello"),
    path("login/", MyLoginView.as_view(), name="login"),
    # path("logout/", logout_view, name="logout"),
    path("logout/", MyLogoutPage.as_view(), name="logout"),
    path("aboutme/<int:pk>/", AboutMeView.as_view(), name="about_me"),
    path("aboutme/<int:pk>/update/", AboutMeUpdateView.as_view(), name="about_me_update"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profiles/", ProfilesListView.as_view(), name="profiles_list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profiles_detail"),
    path(
        "cookie/set/",
        set_cookie_view,
        name="set_cookie",
    ),
    path(
        "cookie/get/",
        get_cookie_view,
        name="get_cookie",
    ),
    path(
        "session/set/",
        set_session_view,
        name="set_session",
    ),
    path(
        "session/get/",
        get_session_view,
        name="get_session",
    ),
    path("foobar/", FooBarView.as_view(), name="foo_bar"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
