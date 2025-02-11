from random import choice, choices, randint
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Order, Product
from .utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        "group_fixtures.json",  # dumpdata auth.Group
        "user_fixtures.json",  # dumpdata auth.User
        "product_fixtures.json",
    ]

    def test_get_products(self):
        response = self.client.get(reverse("shop_app:product_list"))

        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)

        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=[p.pk for p in response.context["products"]],
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shop_app/products-list.html")


class ProductCreateViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user.user_permissions.add(Permission.objects.get(codename="add_product"))
        self.client.login(username="testuser", password="testpassword")
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def tearDown(self):
        self.user.delete()

    @override_settings(
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
            "requestdataapp.middlewares.set_useragent_on_request_middleware",
            "requestdataapp.middlewares.CountRequestsMiddleware",
            # "requestdataapp.middlewares.ThrottlingMiddleware",
        ]
    )
    def test_create_product(self) -> None:
        response = self.client.post(
            reverse("shop_app:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            },
        )
        self.assertRedirects(response, reverse("shop_app:product_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name="".join(choices(ascii_letters, k=10)))

    # def tearDown(self):
    #     self.product.delete()

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name="".join(choices(ascii_letters, k=10)))

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shop_app:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shop_app:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


# TDD
class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "user_fixtures.json",
        "group_fixtures.json",
        "product_fixtures.json",
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shop_app:product_export"))
        products_data = response.json()
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products_data["products"], expected_data)


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.credentials = {"username": "bob-test", "password": "qwerty"}
        # cls.user = User.objects.create_user(**cls.credentials)
        cls.user = User.objects.create_user(username="bob-test", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shop_app:order_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authentication(self):
        self.client.logout()
        url_redirect = str(settings.LOGIN_URL) + "?next=/shop/orders/"
        response = self.client.get(reverse("shop_app:order_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url_redirect)
        # self.assertIn(str(settings.LOGIN_URL), response)


class OrdersDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="Jon-test", password="qwerty123")
        cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product_data = {
            "name": "".join(choices(ascii_letters, k=10)),
            "price": "123.45",
            "description": "A good product",
            "discount": f"{randint(0, 5) or None}",
        }

        self.product = Product.objects.create(**self.product_data)
        self.order_data = {
            "user": self.user,
            "promocode": choice(["".join(choices(ascii_letters, k=5)), " "]),
            "delivery_address": "c.Moscow, st.Lermontov, h.6",
        }
        self.order = Order.objects.create(**self.order_data)
        self.order.products.set([self.product])

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_get_order_details(self):
        response = self.client.get(reverse("shop_app:order_details", kwargs={"pk": self.order.pk}))
        order_data = response.context["order"]

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Order # {self.order.pk} details")
        self.assertTemplateUsed(response, "shop_app/order_detail.html")
        self.assertEqual(order_data.pk, self.order.pk)
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, self.order.delivery_address)


# TDD
class OrdersExportViewTestCase(TestCase):
    fixtures = [
        "group_fixtures.json",
        "user_fixtures.json",
        "product_fixtures.json",
        "order_fixtures.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="Joni", password="qwerty123", is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse("shop_app:order_export"))
        orders = Order.objects.order_by("pk").all()
        expected_data = {
            "orders": [
                {
                    "pk": order.pk,
                    "user": order.user.pk,
                    "products": [product.pk for product in order.products.all()],
                    "promocode": order.promocode,
                    "delivery_address": order.delivery_address,
                }
                for order in orders
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_data)
