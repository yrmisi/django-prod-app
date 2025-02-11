import json
from csv import DictReader
from io import TextIOWrapper
from typing import Iterator

from django.contrib.auth.models import User
from django.db import transaction

from .models import Order, Product


def filter_dict(row_dict: dict[str, str], key_name: str | None) -> dict[str, User | str]:
    """Returns a filtered dictionary by key, if there is no key then the original one."""
    if key_name is None:
        return row_dict

    filtered_row_dict: dict[str, User | str] = {}
    key_user: str = "user"

    for key, val in row_dict.items():
        if key == key_user:
            filtered_row_dict[key] = User.objects.get(username=val)
        elif key != key_name:
            filtered_row_dict[key] = val

    return filtered_row_dict


def save_csv_file(
    obj: Product | Order, file, encoding: str, exclude_key=None
) -> list[Product | Order]:
    """Function for save .csv file with products or orders data."""
    csv_file: TextIOWrapper = TextIOWrapper(file, encoding=encoding)
    reader: Iterator[dict[str, str]] = DictReader(csv_file)
    rows: list[dict[str, str]] = list(reader)

    objects_list: list[Product | Order] = [obj(**filter_dict(row, exclude_key)) for row in rows]
    obj.objects.bulk_create(objects_list)

    if isinstance(obj, type(Order)):
        for idx, row in enumerate(rows):
            product_names: list[str] = [name.strip() for name in row["products"].split(",")]

            with transaction.atomic():
                product_objs: list[Product] = Product.objects.filter(name__in=product_names).all()

            objects_list[idx].products.add(*product_objs)

    return objects_list


def save_json_file(obj: Product | Order, file: bytes, encoding: str, exclude_key=None) -> None:
    """Function for save .json file with products or orders data."""
    csv_file: TextIOWrapper = TextIOWrapper(file, encoding=encoding)
    data: dict[str, dict[str, str]] = json.load(csv_file)

    for val in data.values():
        filtered_dict: dict[str, User | str] = filter_dict(val, exclude_key)
        create_obj: Product | Order = obj.objects.create(**filtered_dict)

        if isinstance(obj, type(Order)):
            with transaction.atomic():
                product_objs = Product.objects.filter(name__in=val[exclude_key])
                create_obj.products.set(product_objs)
