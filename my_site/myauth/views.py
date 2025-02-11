import random
from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AvatarUpdateForm, ProfileForm, UserForm
from .models import Profile


class HelloView(View):
    message = _("welcome hello word")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext("one product", "{count} products", items)
        products_line = products_line.format(count=items)

        return HttpResponse(f"<h1>{self.message}</h1> \n<h2>{products_line}</h2>")


class MyLoginView(LoginView):
    template_name = "myauth/login.html"

    def get_success_url(self) -> str:
        return reverse("myauth:about_me", kwargs={"pk": self.request.user.pk})


class MyLogoutPage(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        logout(request)
        return redirect("myauth:login")


class AboutMeView(UpdateView):  # type: ignore
    # model = User
    form_class = AvatarUpdateForm
    template_name = "myauth/about_me.html"
    queryset = User.objects.select_related("profile")

    def get_object(self, queryset=None):
        """Get the current user."""
        return self.request.user

    def get_context_data(
        self, **kwargs: dict[str, Any]
    ) -> dict[str, AvatarUpdateForm | dict[str, Any]]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.get_object()
            profile = getattr(user, "profile", None)
            context["form"] = self.form_class(instance=user.profile if profile else None)
            context["user_info"] = {
                _("Avatar"): self.is_there_avatar_from_profile(profile),
                _("User"): user.username,
                _("First name"): user.first_name,
                _("Last name"): user.last_name,
                _("E-mail"): user.email,
                _("Biography"): self.get_user_bio(profile),
                _("Agreement"): self.signing_of_the_agreement(profile),
            }
        return context

    def is_there_avatar_from_profile(self, profile) -> Any | str:
        """Get images for avatars, and if there is none, then a message about it"""
        if profile.avatar:
            return profile.avatar
        return str(_("no image"))

    def get_user_bio(self, profile) -> str | None:
        """Safely get the user's bio, returning a default message if no profile exists."""
        if hasattr(profile, "bio"):
            return profile.bio
        return None

    def signing_of_the_agreement(self, profile) -> str:
        """Gets information about the user's agreement with the terms, returns a string about it."""
        if profile.agreement_accepted:
            return str(_("I agree"))
        return str(_("I don't agree"))

    def get_success_url(self) -> str:
        return reverse("myauth:about_me", kwargs={"pk": self.request.user.pk})


class AboutMeUpdateView(UpdateView):  # type: ignore
    model = User
    form_class = UserForm
    template_name = "myauth/about_me_update.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, ProfileForm]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile, *_ = Profile.objects.get_or_create(user=self.request.user)
            context["profile_form"] = ProfileForm(instance=profile)

        return context

    def form_valid(self, form: UserForm) -> HttpResponse:
        if self.request.user.is_authenticated:
            profile_form = ProfileForm(
                self.request.POST, self.request.FILES, instance=self.request.user.profile
            )
            if form.is_valid() and profile_form.is_valid():
                form.save()
                profile_form.save()
                return super().form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self) -> str:
        return reverse("myauth:about_me", kwargs={"pk": self.request.user.pk})


class RegisterView(CreateView):  # type: ignore
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    # success_url = reverse_lazy("myauth:about_me")

    def form_valid(self, form: UserCreationForm) -> HttpResponse:  # type: ignore
        response = super().form_valid(form)
        user = self.object
        if user is not None:
            Profile.objects.create(user=user)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response

    def get_success_url(self) -> str:
        if self.object is None:
            raise Http404("Object not found")

        return reverse("myauth:about_me", kwargs={"pk": self.object.pk})


class ProfilesListView(LoginRequiredMixin, ListView):  # type: ignore
    context_object_name = "profiles"
    queryset = Profile.objects.select_related("user").all()


class ProfileDetailView(UserPassesTestMixin, DetailView):  # type: ignore
    context_object_name = "profile"
    queryset = Profile.objects.select_related("user")

    def test_func(self) -> bool:
        profile = self.get_object()
        return self.request.user.is_staff or self.request.user == profile.user

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, AvatarUpdateForm]:
        context = super().get_context_data(**kwargs)
        context["form"] = AvatarUpdateForm()
        return context

    def post(
        self, request: HttpRequest, *args: list[str], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        user_id = request.POST.get("user_id")
        profile = get_object_or_404(Profile, user=user_id)

        form = AvatarUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print(self.template_name)
            form.save()
            return redirect(self.request.path)

        return render(request, "myauth/profile_detail.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/admin/")

        return render(request, "myauth/login.html")

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("/admin/")

    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "Not value")
    return HttpResponse(f"Cookie value: {value!r} {random.random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "Not value")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "span": "eggs"})
