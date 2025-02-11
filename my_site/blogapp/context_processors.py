from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _


def urls_and_name(request: HttpRequest) -> dict[str, tuple[str, str, str]]:
    return {
        "urls_blog_path": [
            ("shop_app:index", _("Home page"), reverse("shop_app:index")),
            ("blogapp:article_list", _("Articles"), reverse("blogapp:article_list")),
        ]
    }
