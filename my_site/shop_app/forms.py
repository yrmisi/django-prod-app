from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _, pgettext_lazy

from .models import Order, Product

# from django.core import validators


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"cols": 5, "rows": "30"}),
#         validators=[
#             validators.RegexValidator(regex="great", message="Field must contain word 'great'")
#         ],
#     )


# If you want to upload multiple files using one form field, create a subclass of the field’s widget
# and set its allow_multiple_selected class attribute to True.
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount", "preview"]
        widgets = {
            "description": forms.Textarea(attrs={"cols": 30, "rows": 5}),
        }
        labels = {
            "name": pgettext_lazy("product name", "Name"),
            "price": _("Price"),
            "description": _("Product description"),
            "discount": _("Discount"),
            "preview": _("Preview"),
        }

    # устарело ClearableFileInput и multiple
    # images = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}))
    images = MultipleFileField(required=False, label=_("Images"))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user",
            "products",
            "promocode",
            "delivery_address",
            "receipt",
        ]
        widgets = {
            "delivery_address": forms.Textarea(attrs={"cols": 30, "rows": 5}),
        }
        labels = {
            "user": _("Customer"),
            "products": _("List of products"),
            "promocode": _("Promocode"),
            "delivery_address": _("Delivery address"),
        }
        error_messages = {
            "promocode": {
                "max_length": ("The promo code is too long."),
            }
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ["name"]
        labels = {"name": pgettext_lazy("group name", "Name")}


class FileImportForm(forms.Form):
    uploaded_file = forms.FileField(label=_("file"))
