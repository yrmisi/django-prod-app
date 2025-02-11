from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _


def urls_and_name(request: HttpRequest) -> dict[str, tuple[str, str, str]]:
    return {
        "urls_page_path": [
            ("shop_app:index", _("Home page"), reverse("shop_app:index")),
            ("shop_app:group_list", _("Groups"), reverse("shop_app:group_list")),
            ("shop_app:product_list", _("Products"), reverse("shop_app:product_list")),
            ("shop_app:order_list", _("Orders"), reverse("shop_app:order_list")),
            ("myauth:profiles_list", _("Profiles"), reverse("myauth:profiles_list")),
            ("blogapp:article_list", _("Articles"), reverse("blogapp:article_list")),
        ]
    }
